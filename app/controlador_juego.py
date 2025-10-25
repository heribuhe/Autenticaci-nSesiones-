from flask import render_template, request, redirect, url_for, Blueprint
from app.models import db, Juego
from flask_login import login_required, current_user


def init_routes(app):
    main = Blueprint('main', __name__)

    @main.route('/')
    def home():
        return redirect(url_for('auth.login'))  # ✅ Redirige al login del blueprint 'auth'

    app.register_blueprint(main)
    

    @app.route('/juegos')
    @login_required
    def juegos():
        juegos = Juego.query.all()
        return render_template('juegos.html', juegos=juegos)
    
    @app.route('/guardar_juego', methods=['GET', 'POST'])
    def guardar_juego():
        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio = float(request.form['precio'])
            
            nuevo_juego = Juego(nombre=nombre, descripcion=descripcion, precio=precio)
            db.session.add(nuevo_juego)
            db.session.commit()
            
            return redirect('/')
        
        return render_template('agregar_juego.html')
    
    @app.route('/eliminar/<int:id>')
    def eliminar_juego(id):
        juego = Juego.query.get_or_404(id)
        db.session.delete(juego)
        db.session.commit()
        return redirect('/')
    
    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        juego = Juego.query.get_or_404(id)
        
        if request.method == 'POST':
            juego.nombre = request.form['nombre']
            juego.descripcion = request.form['descripcion']
            juego.precio = float(request.form['precio'])
            
            db.session.commit()
            return redirect('/')
        
            return direct(url_for('juegos'))    
        
        return render_template('editar_juego.html', juego=juego)

            
