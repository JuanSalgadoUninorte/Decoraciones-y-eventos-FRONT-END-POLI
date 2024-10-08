from flask import Flask, render_template, request, redirect, url_for, flash, render_template_string, jsonify
from config import config
from functools import wraps
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from models.ModelUser import ModelUser
from models.entities.User import User
import os

app = Flask(__name__)
csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
os.makedirs(os.path.join('src', 'static', 'uploads'), exist_ok=True)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.perfil != 'Administrador':
            flash('Acceso denegado. Solo los administradores pueden acceder a esta página.')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_dashboard():
    cur = db.connection.cursor()
    cur.execute("SELECT id, fullname, telefono, email, perfil FROM user")
    usuarios = cur.fetchall()
    cur.execute("SELECT * FROM banners")
    banners = cur.fetchall()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.execute("SELECT * FROM categorias")
    categorias = cur.fetchall()
    cur.close()
    return render_template('admin/dashboard.html', usuarios=usuarios, productos=productos, categorias=categorias, banners=banners)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        full_name = request.form['firstName'] + " " + request.form['lastName']
        phone = request.form['phone']
        if password != confirm_password:
            flash("Las contraseñas no coinciden.")
            return render_template('auth/signup.html')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password, fullname=full_name, telefono=phone,
                        perfil="Visualizador")
        if ModelUser.register(db, new_user):
            flash("Usuario registrado con éxito.")
            return redirect(url_for('login'))
        else:
            flash("Error al registrar el usuario.")
            return render_template('auth/signup.html')
    return render_template('auth/signup.html')

@app.route('/add_user', methods=['POST'])
@login_required
@admin_required
def add_user():
    if request.method == "POST":
        email = request.form['usuario-email']
        password = request.form['usuario-password']
        confirm_password = request.form['usuario-confirm-password']
        full_name = request.form['usuario-nombre']
        phone = request.form['usuario-telefono']
        perfil = request.form.get('usuario_perfil')
        if password != confirm_password:
            flash("Las contraseñas no coinciden.")
            return redirect(url_for('admin_dashboard'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password, fullname=full_name, telefono=phone,
                        perfil=perfil)
        if ModelUser.register(db, new_user):
            flash("Usuario registrado con éxito.")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Error al registrar el usuario.")
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == "POST":
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        tamano = request.form['tamano']
        color = request.form['color']
        categoria = request.form['categoria']
        flores = request.form['flores']
        estado = request.form['estado']
        nombre = request.form['producto-nombre']
        foto = request.files['imagen']
        if foto:
            if foto.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                foto_path = os.path.join('src', 'static', 'uploads', foto.filename)
                print("Archivo recibido: ", foto.filename)
                print("Ruta donde se guardará: ", os.path.abspath(foto_path))
                foto.save(foto_path)
                print("Archivo guardado correctamente.")
        try:
            cur = db.connection.cursor()
            cur.execute("INSERT INTO productos (precio, descripcion, tamano, color, categorias, flores, estado, nombre, imagen) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (precio, descripcion, tamano, color, categoria, flores, estado, nombre, foto.filename))
            db.connection.commit()
            flash('Producto registrado con éxito')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash('No fue posible su inserción....', str(e))
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/add_category', methods=['POST'])
@login_required
@admin_required
def add_category():
    if request.method == "POST":
        estado = request.form['estado']
        nombre = request.form['nombre']
        foto = request.files['imagen']
        if foto:
            
            if foto.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                
                foto_path = os.path.join('src', 'static', 'uploads', foto.filename)
                print("Archivo recibido: ", foto.filename) 
                print("Ruta donde se guardará: ", os.path.abspath(foto_path))
                foto.save(foto_path)
                print("Archivo guardado correctamente.") 
        try:
            cur = db.connection.cursor()
            cur.execute("INSERT INTO categorias (nombre, estado, imagen) values (%s, %s, %s)", (nombre,estado,foto.filename))
            db.connection.commit()
            flash('Categoría registrada con éxito')
        except Exception as e:
            flash('No fue posible su inserción....', str(e))
    return redirect(url_for('admin_dashboard'))

@app.route('/add_banner', methods=['GET', 'POST'])
@login_required
@admin_required
def add_banner():
    if request.method == "POST":
        estado = request.form['estado']
        nombre = request.form['nombre']
        foto = request.files['imagen']
        segundo_mensaje = request.form['segundo-mensaje']
        primer_mensaje = request.form['primer-mensaje']
        if foto:
            if foto.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                foto_path = os.path.join('src', 'static', 'uploads', foto.filename)
                print("Archivo recibido: ", foto.filename) 
                print("Ruta donde se guardará: ", os.path.abspath(foto_path))
                foto.save(foto_path)
                print("Archivo guardado correctamente.") 
        try:
            cur = db.connection.cursor()
            cur.execute("INSERT INTO banners (nombre, estado, imagen, primer_mensaje, segundo_mensaje) values (%s, %s, %s, %s, %s)", (nombre,estado,foto.filename, primer_mensaje, segundo_mensaje))
            db.connection.commit()
            flash('Banner registrado con éxito')
        except Exception as e:
            flash('No fue posible su inserción....', str(e))
    return redirect(url_for('admin_dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = User(0, request.form['email'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Credenciales inválidas.")
                return render_template('auth/login.html')
        else:
            flash("Credenciales inválidas")
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/comment_above_us', methods=['GET', 'POST'])
@login_required
def comment_above_us():
    if request.method == "POST":
        comentario = request.form['comentario']
        nombre = request.form['nombre']
        foto = request.files['imagen']
        if foto:
            if foto.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                foto_path = os.path.join('src', 'static', 'uploads', foto.filename)
                print("Archivo recibido: ", foto.filename)
                print("Ruta donde se guardará: ", os.path.abspath(foto_path))
                foto.save(foto_path)
                print("Archivo guardado correctamente.")
        try:
            cur = db.connection.cursor()
            cur.execute("INSERT INTO comentario (nombre, comentario, imagen) values (%s, %s, %s)", (nombre,comentario,foto.filename))
            db.connection.commit()
            flash('Comentario registrado con éxito')
            return redirect(url_for('home'))
        except Exception as e:
            flash('No fue posible su inserción....', str(e))
            return redirect(url_for('home'))
    return render_template('comment_above_us.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/producto/<int:producto_id>')
@login_required
def producto(producto_id):
    cur = db.connection.cursor()
    cur.execute("SELECT id, nombre, descripcion, precio, tamano, color, imagen FROM productos WHERE id = %s", (producto_id,))
    producto = cur.fetchone()

    if producto:
        # Convertir la tupla en un diccionario
        producto_dict = {
            'id': producto[0],
            'nombre': producto[1],
            'descripcion': producto[2],
            'precio': producto[3],
            'tamano': producto[4],
            'color': producto[5],
            'imagen': producto[6],
        }

        # Resto del código para materiales, detalles, etc.
        materiales = ["Madera", "Oasis", "Lirios", "Rosas"]  # Ejemplo estático
        detalles = [
            {"descripcion": "Flores", "cantidad": 5, "precio": 800, "total": 4000},
            {"descripcion": "Transporte", "cantidad": 1, "precio": 50000, "total": 50000},
        ]
        subtotal = sum(item['total'] for item in detalles)
        descuento = subtotal * 0.21
        total = subtotal - descuento

        return render_template('product.html', producto=producto_dict, materiales=materiales, detalles=detalles, subtotal=subtotal, descuento=descuento, total=total)
    else:
        flash("Producto no encontrado.")
        return redirect(url_for('home'))


@app.route('/home')
@login_required
def home():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM banners WHERE estado = 'Activo'")
    banners = cur.fetchall()
    cur.execute("SELECT * FROM productos WHERE estado = 'Activo'")
    productos = cur.fetchall()
    cur.execute("SELECT * FROM categorias WHERE estado = 'Activo'")
    categorias = cur.fetchall()
    cur.execute("SELECT * FROM comentario")
    comentarios = cur.fetchall()
    cur.close()
    return render_template("home.html", categorias=categorias, banners=banners, productos=productos, comentarios=comentarios)

@app.route('/edit_user', methods=['POST'])
@login_required
@admin_required
def edit_user():
    if request.method == "POST":
        id = request.form['id']
        email = request.form['usuario-email']
        password = request.form['usuario-password']
        full_name = request.form['usuario-nombre']
        phone = request.form['usuario-telefono']
        perfil = request.form.get('usuario_perfil')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            cur = db.connection.cursor()
            print("UPDATE user SET fullname = '"+ full_name + "', email = '"+email+"', telefono= '"+phone+"', perfil='"+perfil+"', password='"+hashed_password+"' WHERE id = " +id)
            cur.execute("UPDATE user SET fullname = '"+ full_name + "', email = '"+email+"', telefono= "+phone+", perfil='"+perfil+"', password='"+hashed_password+"' WHERE id = " +id)
            db.connection.commit()
            flash('Usuario actualizado con éxito')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash('No fue posible su actualización....', str(e))
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/update_category', methods=['POST'])
@login_required
@admin_required
def update_category():
    if request.method == "POST":
        id = request.form['id']
        categoria_nombre = request.form['nombre']
        estado = request.form['estado']
        cur = db.connection.cursor()
        foto = request.files['imagen']
        if foto:
            if foto.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                foto_path = os.path.join('src', 'static', 'uploads', foto.filename)
                print("Archivo recibido: ", foto.filename)
                print("Ruta donde se guardará: ", os.path.abspath(foto_path))
                foto.save(foto_path)
                print("Archivo guardado correctamente.")
        try:
            cur.execute("UPDATE categorias SET nombre = '"+ categoria_nombre + "', estado = '"+estado+"', imagen= '"+foto.filename+"'  WHERE id = " +id)
            db.connection.commit()
            flash('Categoría actualizada con éxito')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash('No fue posible su actualización....', str(e))
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
    if request.method == "POST":
        id = request.form['id']
        tabla = request.form['tabla']
        cur = db.connection.cursor()
        try:
            cur.execute("DELETE FROM "+ tabla + " WHERE id = " +id)
            print("DELETE FROM "+ tabla + " WHERE id = " +id)
            db.connection.commit()
            flash('Elemento eliminado con éxito')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash('No fue posible su eliminación....', str(e))
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/edit_product', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product():
    if request.method == "POST":
        id = request.form['id']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        tamano = request.form['tamano']
        color = request.form['color']
        flores = request.form['flores']
        categoria = request.form['categoria']
        estado = request.form['estado']
        nombre = request.form['producto-nombre']
        foto = request.files['imagen']
        if foto:
            if foto.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                foto_path = os.path.join('src', 'static', 'uploads', foto.filename)
                print("Archivo recibido: ", foto.filename)
                print("Ruta donde se guardará: ", os.path.abspath(foto_path))
                foto.save(foto_path)
                print("Archivo guardado correctamente.")
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE productos SET nombre = '"+ nombre + "', estado = '"+estado+"', imagen= '"+foto.filename+"', categorias='"+categoria+"',  precio = '"+precio+"', descripcion = '"+descripcion+"', tamano = '"+tamano+"', color = '"+color+"', flores = '"+flores+"' WHERE id = " +id)
            db.connection.commit()
            flash('Producto actualizado con éxito')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash('No fue posible su actualización....', str(e))
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/edit_banner', methods=['POST'])
@login_required
@admin_required
def edit_banner():
    if request.method == "POST":
        id = request.form['id']
        estado = request.form['estado']
        nombre = request.form['nombre']
        foto = request.files['imagen']
        segundo_mensaje = request.form['segundo-mensaje']
        primer_mensaje = request.form['primer-mensaje']
        if foto:
            if foto.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                foto_path = os.path.join('src', 'static', 'uploads', foto.filename)
                print("Archivo recibido: ", foto.filename)
                print("Ruta donde se guardará: ", os.path.abspath(foto_path))
                foto.save(foto_path)
                print("Archivo guardado correctamente.")
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE banners SET imagen='"+foto.filename+"', estado='"+estado+"', nombre='"+nombre+"', primer_mensaje='"+primer_mensaje+"', segundo_mensaje='"+segundo_mensaje+"' WHERE id = " +id)
            db.connection.commit()
            flash('Banner actualizado con éxito')
        except Exception as e:
            flash('No fue posible su actualización....', str(e))
    return redirect(url_for('admin_dashboard'))

def status_401(error):
    return render_template_string("""<script>alert('Debes estar logueado para acceder a esta ruta.');window.location.href = "{{ url_for('login') }}";</script>""")

def status_404(error):
    return render_template_string("""<script>alert('No existe dicha ruta.....');window.location.href = "{{ url_for('login') }}";</script>""")

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    csrf.init_app(app)
    app.register_error_handler(404, status_404)
    app.run(debug=True, host='127.0.0.1', port=5001)
