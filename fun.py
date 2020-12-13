from hashlib import md5
class ver:
   
    def verEmail(self,correo):
        a=False
        b=False
        cont=0
        for i in correo:
           if i=="@":
              cont=cont+1
              a=True
           if i==".":
              b=True 
        j=0  
        lis=[]
        if a and cont==1:

           if correo.index("@")>0:
              while(j<len(correo)):
                 if correo[j]=="@":
                    aux=j
                 if correo[j]==".":
                    lis.append(j)
                 j=j+1      

              if b:

                 if lis[len(lis)-1]-aux>1:


                    if correo[len(correo)-1]==".":

                       a=False
                       #print(a)
                 else:
                    b=False
                    #print(b)
              else:
                 b=False  
           else: 
              a=False
              #print(a)   

        else:
           if cont>1:
              a=False
           #print(a)
        if b==False:
           return(b)
        else:
           return(a)

    def verPass(self,contra):
   
        b=False
        b1=False
        c=False
        c1=False
    
    
    
        l=[]
        #n=[]     
        if(len(contra)>=8):
           for i in contra:
              if i.isdigit():#verificar dijitos
                 #n.append(i)
                 b=True
              if i.isalpha():#verificar letras
                 l.append(i)
                 b1=True

           if b and b1:
              for i in l:
                 if i.isupper():#verificar mayusculas
                    c=True
                 if i.islower():#verificar minusculas
                    c1=True   
              if c and c1:
                 contra=md5(contra.encode("utf-8")).hexdigest()
                 return contra
              else:
                 return(False)   
           else:
              return(False)      
        else:
           return(False)      