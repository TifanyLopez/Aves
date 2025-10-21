from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from pprint import pprint   

app = Flask(__name__)
app.secret_key = 'appsecretkey'  # Clave para sesiones

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'informacion1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# LOGIN
@app.route('/accesologin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['logueado'] = True
            session['id'] = user['id']
            session['id_rol'] = user['id_rol']
            if user['id_rol'] == 1:
                return render_template('admin.html')
            else:
                return render_template('usuario.html')
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/listarUsuario', methods=['GET', 'POST'])
def listarUsuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre, email, password, id_rol) VALUES (%s, %s, %s, '2')",
            (nombre, email, password)
        )
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('listarUsuario'))

    # GET: mostrar lista de usuarios
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, email, password FROM usuario ORDER BY id ASC")
    listarUsuarios = cursor.fetchall()
    cursor.close()

    return render_template('listarUsuario.html', usuarios=listarUsuarios)

@app.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'success': True, 'message': 'Usuario eliminado correctamente'})

@app.route('/updateUsuario', methods=['POST'])
def updateUsuario():
    try:
        id = request.form['id']
        nombre = request.form['nombre'] 
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE usuario SET nombre = %s, email = %s, password = %s WHERE id = %s",
            (nombre, email, password, id)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'success': True,
            'message': 'Usuario actualizado correctamente'
        })

    except Exception as e:
        print("Error al actualizar:", e)

        return jsonify({
            'success': False,
            'message': 'Error interno al actualizar'
        })

#/////////////////////////////////
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        tipo = request.form.get('contraseña')

        if not nombre or not email or not tipo:
            flash("Todos los campos son obligatorios")
            return redirect(url_for('registro'))

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO personas (nombre, email, contraseña) VALUES (%s, %s, %s)",
            (nombre, email, contraseña)
        )
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('registro'))

    # Mostrar lista de registros
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_personas, nombre, email, contraseña FROM personas ORDER BY id_personas ASC")
    listarUsuarios = cursor.fetchall()
    cursor.close()

    return render_template('registro.html', usuarios=listarUsuarios)

# CREAR USUARIO - Procesa el formulario
@app.route('/crearusuario', methods=['POST'])
def crearusuario():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO usuario (nombre, email, password, id_rol) VALUES (%s, %s, %s, '2')",
                   (nombre, email, password))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('login'))

# PÁGINAS DE INFORMACIÓN
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/listarusuario')
def listaregistro():
    return render_template('listaregistro.html')

# Lista  formulario-------o
@app.route('/listar_agregados')
def listar_agregados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM vista")
    datos = cur.fetchall()
    cur.close()
    return render_template('listar_agregados.html', datos=datos)

# Listar informacion con tabla (solo lista)
@app.route('/listar_informacion')
def listar_informacion():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM vista")
    datos = cur.fetchall()
    cur.close()
    return render_template('listar_informacion.html', datos=datos)

# Agregar 
@app.route('/agregar_datos', methods=['POST'])
def agregar_datos():
    nombre = request.form['nombre']
    correo = request.form['correo']
    descripcion = request.form['descripcion']
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO vista (nombre, correo, descripcion) VALUES (%s, %s, %s)",
        (nombre, correo, descripcion)
    )
    mysql.connection.commit()
    cur.close()
    flash("agregado correctamente", "success")
    return redirect(url_for('listar_agregados'))

# Editar
@app.route('/editar_datos', methods=['POST'])
def editar_datos():
    id = request.form['id']
    nombre = request.form['nombre']
    correo = request.form['correo']
    descripcion = request.form['descripcion']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE datos
        SET nombre=%s, correo=%s, descripcion=%s
        WHERE id=%s
    """, (nombre, correo, descripcion, id))
    mysql.connection.commit()
    cur.close()
    flash("actualizado correctamente", "success")
    return redirect(url_for('listar_informacion'))

# Eliminar

@app.route('/eliminar_datos/<int:id>')
def eliminar_datos(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM datos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash("Eliminado correctamente", "success")
    return redirect(url_for('listar_informacion'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
