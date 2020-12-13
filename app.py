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

    if v.verPass(password)==False:#VERIFICAR CONTRASEÑA VALIDA
        flash('Contraseña invalida... Intentelo de nuevo...', 'danger')
        return redirect(request.url)
    if email=='' or password=='':#VERIFICAR CAMPOS VACIOS
        flash('No pueden quedar campos vacios... Intentelo de nuevo...', 'danger')
        return redirect(request.url)

    usuario=db.execute('select * from usuarios where email=? and password= ?',(email,v.verPass(password),)).fetchone()  
    print(usuario)
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

    return render_template('enseccion/admin/categorias.html')

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
    print(session['usuario'][0],nombre)
    try:
        cursor=db.cursor()
        cursor.execute(""" insert into categorias(
            id_usuario,
            nombre
        )values(?,?)
        """,(session['usuario'][0] ,nombre)) 
        db.commit()
    except:
        flash('No se pudo guardar la categoria', 'danger')
        return redirect(request.url)  
    return redirect(url_for('categorias'))

#------PRODUCTOS--------
@app.route('/productos')
def productos():
    if not 'usuario' in session:
        return redirect(url_for('index'))

    return render_template('enseccion/admin/productos.html')
@app.route('/productos/crear')
def crear_producto():
    if not 'usuario' in session:
        return redirect(url_for('index'))

    return render_template('enseccion/admin/crearpro.html')






app.run(debug=True, port='5100')