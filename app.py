# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# import pymysql

# # Install PyMySQL as MySQLdb
# pymysql.install_as_MySQLdb()

# # Flask constructor takes the name of 
# # current module (__name__) as argument.
# app = Flask(__name__)
# app.secret_key = 'your-secret-key-here'  # Required for flash messages and sessions

# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://karthick1808:Welcome!12345@karthick1808.cnk646w46gc7.ap-south-1.rds.amazonaws.com:3306/flask_app'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize database
# db = SQLAlchemy(app)

# # User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
    
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     def __repr__(self):
#         return f'<User {self.username}>'

# # The route() function of the Flask class is a decorator, 
# # which tells the application which URL should call 
# # the associated function.
# @app.route('/')
# # '/' URL is bound with home() function.
# def home():
#     return render_template('index.html')

# @app.route('/about')
# def about():
#     """About page route"""
#     return render_template('about.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     """Registration page route"""
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
        
#         # Validation
#         if not all([username, email, password, confirm_password, first_name, last_name]):
#             flash('All fields are required!', 'error')
#             return render_template('register.html')
        
#         if password != confirm_password:
#             flash('Passwords do not match!', 'error')
#             return render_template('register.html')
        
#         if len(password) < 6:
#             flash('Password must be at least 6 characters long!', 'error')
#             return render_template('register.html')
        
#         # Check if username or email already exists
#         existing_user = User.query.filter(
#             (User.username == username) | (User.email == email)
#         ).first()
        
#         if existing_user:
#             flash('Username or email already exists!', 'error')
#             return render_template('register.html')
        
#         # Create new user
#         try:
#             new_user = User()
#             new_user.username = username
#             new_user.email = email
#             new_user.first_name = first_name
#             new_user.last_name = last_name
#             new_user.set_password(password)
            
#             db.session.add(new_user)
#             db.session.commit()
            
#             flash('Registration successful! You can now log in.', 'success')
#             return redirect(url_for('login'))
            
#         except Exception as e:
#             db.session.rollback()
#             flash('Registration failed. Please try again.', 'error')
#             print(f"Registration error: {e}")
    
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """Login page route"""
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         if not username or not password:
#             flash('Username and password are required!', 'error')
#             return render_template('login.html')
        
#         # Find user in database
#         user = User.query.filter_by(username=username).first()
        
#         if user and user.check_password(password):
#             session['user_id'] = user.id
#             session['username'] = user.username
#             flash('Login successful!', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid username or password!', 'error')
    
#     return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     """Dashboard page for logged-in users"""
#     if 'user_id' not in session:
#         flash('Please log in to access the dashboard.', 'error')
#         return redirect(url_for('login'))
    
#     user = User.query.get(session['user_id'])
#     return render_template('dashboard.html', user=user)

# @app.route('/logout')
# def logout():
#     """Logout route"""
#     session.clear()
#     flash('You have been logged out.', 'success')
#     return redirect(url_for('home'))

# # Error handler for 404
# @app.errorhandler(404)
# def page_not_found(error):
#     """Custom 404 error page"""
#     return 'This page does not exist', 404

# # Initialize database tables
# def init_db():
#     """Initialize the database tables"""
#     try:
#         # Create database if it doesn't exist
#         from sqlalchemy import create_engine, text
#         engine = create_engine('mysql://karthick1808:Welcome!12345@karthick1808.cnk646w46gc7.ap-south-1.rds.amazonaws.com:3306/')
#         with engine.connect() as connection:
#             connection.execute(text("CREATE DATABASE IF NOT EXISTS flask_app"))
#         engine.dispose()
        
#         # Create all tables
#         with app.app_context():
#             db.create_all()
#             print("Database tables created successfully!")
#     except Exception as e:
#         print(f"Database initialization error: {e}")

# # main driver function
# if __name__ == '__main__':
#     # Initialize database
#     init_db()
    
#     # run() method of Flask class runs the application 
#     # on the local development server.
#     app.run(debug=True)



# app.py
from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

# Define a route for the root URL ("/")
@app.route('/')
def hello_world():
    """Return a simple HTML response."""
    return '<h1>Hello, World!</h1><p>This is a simple Flask app deployed on EC2.</p>'

# This block is useful for running the app locally for development
# Gunicorn will not use this block
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
