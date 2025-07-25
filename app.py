from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from bson import ObjectId

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# MongoDB Atlas Configuration
MONGO_URI = "mongodb+srv://mayurr:12345@cluster0.hllwy4r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.godigit

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        # Check if email already exists
        if db.users.find_one({'email': email}):
            return render_template('register.html', error="Email already registered")
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user_data = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'phone': phone,
            'password': hashed_password,
            'created_at': datetime.utcnow()
        }
        result = db.users.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        
        # Automatically log in user after registration
        session['user_id'] = str(result.inserted_id)
        return redirect(url_for('profile'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = db.users.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            # Convert ObjectId to string for session
            session['user_id'] = str(user['_id'])
            return redirect(url_for('profile'))
        
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        # Convert string ID back to ObjectId for query
        user = db.users.find_one({'_id': ObjectId(user_id)})
        
        if user:
            # Convert ObjectId to string and format date
            user['_id'] = str(user['_id'])
            user['created_at'] = user['created_at'].strftime('%d %b %Y')
            return render_template('profile.html', user=user)
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)