from flask import session, render_template, redirect, request,  flash
from flask_bcrypt import Bcrypt
from login_registro_app import app
from login_registro_app.modelos.modelo_usuarios import Usuario

bcrypt = Bcrypt( app )

@app.route( '/', methods = ['GET'] )
def desplegar_login_registro():
    return render_template( 'login_registro.html')

@app.route( '/crear/usuario', methods = ['POST'] )
def nuevo_usuario():
    data = {
        **request.form
    }
    
    if Usuario.validar_registro( data ) == False:
        return redirect('/')
    
    else:
        passaword_encriptado = bcrypt.generate_passaword_hash( data['password'] )
        data['password'] = passaword_encriptado
        id_usuario = Usuario.crear_uno( data )
        session['nombre'] = data['nombre'] 
        session['apellido'] = data['apellido']
        session['id_usuario'] = id_usuario
        
        return redirect('/deshboard')
    
    @app.route('/deshboard', methods = ['GET'] )
    def desplegar_dashboard():
        return render_template( 'deshboard.html' )
    
    @app.route( '/login', methods = ['POST'] ) 
    def procesa_login():
        data = {
            "email" : request.form['email_login']
        } 
        usuario = Usuario.obtener_uno_con_emai( data )
        if Usuario == None:
            flash( "email invalido", "error login")
            return redirect('/')
        
        else:
            if not bcrypt.check_password_hash( Usuario.password, request.form['password_login'] ):
                flash( "credenciales incorrectas", "error_password_login")
                return redirect('/')
            else:
                session['nombre'] = usuario.nombre
                session['apellido'] = usuario.apellido
                session['id_usuario'] = usuario.id
                return redirect('/dashboard')
        
        
        
                