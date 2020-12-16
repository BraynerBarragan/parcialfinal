from flask import Flask, render_template, request, redirect, url_for, flash, session
from fun import ver
 
import sqlite3
app = Flask(__name__)
v=ver()
db=sqlite3.connect('database.db', check_same_thread=False)
app.secret_key ='CBZEkZPmgsPdrA3sVEb2PLu1p'

@app.route('/', methods=('GET','POST'))
def index():
    if request.method == 'GET':
        return render_template('login.html')

    email=request.form.get('email')
    password=request.form.get('password')
    if email=='' or password=='':#VERIFICAR CAMPOS VACIOS
        flash('No pueden quedar campos vacios... Intentelo de nuevo...', 'danger')
        return redirect(request.url)
    if v.verPass(password)==False:#VERIFICAR CONTRASEÑA VALIDA
        flash('Contraseña invalida... Intentelo de nuevo...', 'danger')
        return redirect(request.url)
   

    usuario=db.execute('select * from usuarios where email=? and password= ?',(email,v.verPass(password),)).fetchone()  
    #print(usuario)
    if usuario is None:
        flash('Usuario o contraseña incorrecta... Intentelo de nuevo...', 'danger')
        return redirect(request.url)

    session['usuario'] = usuario
    return redirect(url_for('inicio'))
     


#-------USUARIOS----------    
@app.route('/registrarse', methods=('GET','POST'))
def registro():
    if request.method == 'GET':
        return render_template('registro.html')
    nombre= request.form.get('nombre')
    email= request.form.get('email')
    password= request.form.get('password')

    if nombre=='' or email=='' or password=='':#VERIFICAR CAMPOS VACIOS
        flash('No pueden quedar campos vacios... Intentelo de nuevo...', 'danger')
        return redirect(request.url)
    if v.verEmail(email)==False:#VERIFICAR EMAIL VAILIDO
        flash('Correo invalido... Intentelo de nuevo...', 'danger')
        return redirect(request.url)
    if v.verPass(password)==False:#VERIFICAR CONTRASEÑA VALIDA
        flash('Contraseña invalida... Intentelo de nuevo...', 'danger')
        return redirect(request.url)

    act=db.execute('select * from usuarios where email=?',(email,)).fetchone()
    
    if  act is not None:
        flash('Ya existe un usuario con ese correo... Intentelo de nuevo...','danger')
        return redirect(request.url)   

    try:
        cursor=db.cursor()
        cursor.execute(""" insert into usuarios(
            nombre,
            email,
            password
        )values(?,?,?)
        """,(nombre, email, v.verPass(password))) 
        db.commit()
    except:
        flash('No se pudo guardar el usuario', 'danger')
        return redirect(url_for('registro')) 

    flash('Registrado correctamente...', 'success')
    return redirect(url_for('index'))

@app.route('/perfil', methods=('GET','POST'))
def editar_perfil():

    if not 'usuario' in session:
        return redirect(url_for('index'))
    act=db.execute('select * from usuarios where id=?',(session['usuario'][0],)).fetchone()
    if request.method == 'GET':
        return render_template('enseccion/editarusuario.html', usuario=act)

    nombre= request.form.get('nombre')
    email= request.form.get('email')
    password= request.form.get('password')
    if nombre=='' or email=='':#VERIFICAR CAMPOS VACIOS
        flash('No pueden quedar campos vacios... Intentelo de nuevo...', 'danger')
        return redirect(request.url)
    if v.verEmail(email)==False:#VERIFICAR EMAIL VAILIDO
        flash('Correo invalido... Intentelo de nuevo...', 'danger')
        return redirect(request.url)
    
    if password=='':
        password=session['usuario'][3]
    else:
        if v.verPass(password)==False:#VERIFICAR CONTRASEÑA VALIDA
            flash('Contraseña invalida... Intentelo de nuevo...', 'danger')
            return redirect(request.url)
        password=v.verPass(password)
    
    
    cursor=db.cursor()
    cursor.execute(' UPDATE usuarios SET nombre = ?, email = ?, password=? WHERE id = ?',(nombre, email, password,session['usuario'][0])) 
    db.commit()
    flash('Usuario editado correctamente...', 'success')
    return redirect(url_for('inicio'))



#------PAGINA PRINCIPAL-------
@app.route('/index')
def inicio():
    if not 'usuario' in session:
        return redirect(url_for('index'))
    
    return render_template('enseccion/index.html',nombre=session['usuario'][1])

@app.route('/logout')
def cerrar_seccion():
    session.clear()
    return redirect(url_for('index'))

#------CATEGORIA--------
@app.route('/categorias')
def categorias():
    if not 'usuario' in session:
        return redirect(url_for('index'))
    categorias=db.execute('select * from categorias where id_usuario = ?',(session['usuario'][0],)).fetchall()
    return render_template('enseccion/admin/categorias.html', cat=categorias)

@app.route('/categorias/crear', methods=('GET','POST'))
def crear_categoria():
    if not 'usuario' in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        return render_template('enseccion/admin/crearcat.html')
    nombre=request.form.get('nombre')
    if nombre=='':
        flash('No pueden quedar campos vacios... Intentelo de nuevo...', 'danger')
        return redirect(request.url)
    #print(session['usuario'][0],nombre)
    if db.execute('select * from categorias where id_usuario = ? and nombre=?',(session['usuario'][0],nombre,)).fetchone()!=None:
        flash('Ya existe categoria', 'danger')
        return redirect(request.url)  
    try:
        cursor=db.cursor()
        cursor.execute(""" insert into categorias(
            id_usuario,
            nombre
        )values(?,?)
        """,(session['usuario'][0] ,nombre)) 
        db.commit()
    except:
        
        flash('No se pudo guardar categoria', 'danger')
        return redirect(request.url)  
    flash('Categoria guardada correctamente', 'success')    
    return redirect(url_for('categorias'))

@app.route('/categorias/editar/<id>', methods=('GET','POST'))
def editar_categoria(id):
    if not 'usuario' in session:
        return redirect(url_for('index'))
    cat=db.execute('select * from categorias where id=?',(id,)).fetchone()
    if request.method=='GET':
        
        return render_template('enseccion/admin/editarcat.html',cat=cat)
    nombre=request.form.get('nombre')
    if nombre=='':
        flash('No pueden quedar campos vacios... Intentelo de nuevo...', 'danger')
        return redirect(request.url)
    #print(session['usuario'][0],nombre)
    if db.execute('select * from categorias where id_usuario = ? and nombre=? and id!=?',(session['usuario'][0],nombre,id,)).fetchone()!=None:
        flash('Ya existe categoria', 'danger')
        return redirect(request.url) 
    
    cursor=db.cursor()
    cursor.execute('UPDATE productos SET categoria = ? WHERE id_usuario= ?and categoria=?',(nombre,session['usuario'][0],cat[2]))
    cursor.execute(' UPDATE categorias SET nombre = ? WHERE id = ?',(nombre, id))

    db.commit()
    flash('Categoria editada correctamente...', 'success')
    return redirect(url_for('categorias'))


@app.route('/categorias/eliminar/<id>/<cat>')
def eliminar_categoria(id ,cat):
    if not 'usuario' in session:
        return redirect(url_for('index'))
    categorias=db.execute('select * from productos where id_usuario = ? and categoria= ?',(session['usuario'][0],cat,)).fetchall()
    if len(categorias)>0:
        flash('La categoria se encuentra relacionada con un producto...', 'danger')
        return redirect(url_for('categorias'))
    

    cursor=db.cursor()
    cursor.execute('delete from categorias where id=?',(id,))
    db.commit()
    flash('Categoria eliminada correctamente...','success')
    return redirect(url_for('categorias'))

#------PRODUCTOS--------
@app.route('/productos')
def productos():
    if not 'usuario' in session:
        return redirect(url_for('index'))
    productos=db.execute('select * from productos where id_usuario = ?',(session['usuario'][0],)).fetchall()
    return render_template('enseccion/admin/productos.html', pro=productos)

@app.route('/productos/crear', methods=('GET','POST'))
def crear_producto():
    if not 'usuario' in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        categorias=db.execute('select nombre from categorias where id_usuario = ?',(session['usuario'][0],)).fetchall()
        if len(categorias)== 0:
            flash('No hay categorias registradas...', 'danger')
            return redirect(url_for('productos'))

        return render_template('enseccion/admin/crearpro.html', cat=categorias)
    
    nombre=request.form.get('nombre')
    precio=request.form.get('precio')
    categoria=request.form.get('categoria')


    if nombre=='' or precio=='' or categoria=='':
        flash('No pueden quedar campos vacios... Intentelo de nuevo', 'danger')
        
        return redirect(request.url)
    
    try:
        cursor=db.cursor()
        cursor.execute(""" insert into productos(
            nombre,
            categoria,
            id_usuario,
            precio
        )values(?,?,?,?)
        """,(nombre, categoria, session['usuario'][0], precio)) 
        db.commit()
    except:
        flash('No se pudo guardar el producto... Intentelo de nuevo', 'danger')
        return redirect(request.url)
    flash('Producto guardado correctamente', 'success')
    return redirect(url_for('productos'))

@app.route('/productos/editar/<id>', methods=('GET','POST'))
def editar_producto(id):
    if not 'usuario' in session:
        return redirect(url_for('index'))
    #pro=db.execute('select * from productos where id=?',(id)).fetchone()
    if request.method=='GET':
        categorias=db.execute('select nombre from categorias where id_usuario = ?',(session['usuario'][0],)).fetchall()
        act=db.execute('select * from productos where id=?',(id,)).fetchone()
        return render_template('enseccion/admin/editarpro.html',pro=act,cat=categorias)
    
    nombre=request.form.get('nombre')
    precio=request.form.get('precio')
    categoria=request.form.get('categoria')


    if nombre=='' or precio=='':
        flash('No pueden quedar campos vacios... Intentelo de nuevo', 'danger')
        
        return redirect(request.url)
    
    cursor=db.cursor()
    cursor.execute(' UPDATE productos SET nombre = ?, precio= ?, categoria=? WHERE id = ?',(nombre, precio, categoria, id))
    db.commit()

    flash('Producto editado correctamente', 'success')    
    return redirect(url_for('productos'))


    
    

@app.route('/productos/eliminar/<id>')
def eliminar_productos(id):
    if not 'usuario' in session:
        return redirect(url_for('index'))

    

    cursor=db.cursor()
    cursor.execute('delete from productos where id=?',(id,))
    db.commit()
    flash('Categoria eliminada correctamente...','succes')
    return redirect(url_for('productos'))





app.run(debug=True, port='5100')