from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors  # necesario para DictCursor

app = Flask(__name__)
app.secret_key = 'appsecretkey'

# =====================================================
# CONFIGURACIÓN DE MySQL
# =====================================================
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'informacon'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# =====================================================
# RUTAS DE USUARIOS
# =====================================================

# Listar usuarios
@app.route('/listar')
def listar_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario")
    usuarios = cur.fetchall()
    cur.close()
    return render_template("listar.html", usuarios=usuarios)

# Guardar usuario (Agregar)
@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuario (nombre, email, password) VALUES (%s,%s,%s)", (nombre, email, password))
    mysql.connection.commit()
    cur.close()
    flash("Usuario agregado correctamente", "success")
    return redirect(url_for('listar'))

# Actualizar usuario (Editar)
@app.route('/updateUsuario', methods=['POST'])
def updateUsuario():
    id = request.form['id']
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuario SET nombre=%s, email=%s, password=%s WHERE id=%s", (nombre, email, password, id))
    mysql.connection.commit()
    cur.close()
    flash("Usuario actualizado correctamente", "success")
    return redirect(url_for('listar'))

# Eliminar usuario
@app.route('/borrarUser/<int:id>')
def borrarUser(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuario WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for('listar'))


# =====================================================
# LOGIN / LOGOUT
# =====================================================
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
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente ✅', 'success')
    return redirect(url_for('login'))


# =====================================================
# REGISTRO
# =====================================================
@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/crearusuario', methods=['POST'])
def crearusuario():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO usuario (nombre, email, password, id_rol) VALUES (%s, %s, %s, '2')",
        (nombre, email, password)
    )
    mysql.connection.commit()
    cursor.close()
    flash('✅ Usuario registrado correctamente', 'success')
    return redirect(url_for('login'))


# =====================================================
# PÁGINAS INFORMATIVAS
# =====================================================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


# =====================================================
# VISTAS DE INTERFAZ (paneles y formularios)
# =====================================================
@app.route("/perfil")
def perfil():
    return render_template("perfil.html")


@app.route("/registrar")
def registrar():
    return render_template("registrar.html")


@app.route("/visualizar")
def visualizar():
    return render_template("visualizar.html")


# =====================================================
# MAIN
# =====================================================
if __name__ == '__main__':
    app.run(debug=True, port=8000)
