from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import json
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from website import auth  # assuming auth is the name of your authentication blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__, template_folder='website/templates', static_folder='website/static', static_url_path='/website/static')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30 MB
ALLOWED_EXTENSIONS = {'webm', 'mp4', 'avi', 'mov', 'mkv'}

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'upload')

PROPERTY_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'properties.json')

try:
    with open(PROPERTY_FILE, 'r') as f:
        try:
            property_list = json.load(f)
        except json.JSONDecodeError:
            property_list = []
except FileNotFoundError:
    property_list = []

def create_upload_folder():
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

def generate_unique_filename():
    return str(uuid.uuid4())

create_upload_folder()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    from website.models import User
    # Handle login logic here
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            new_user = User(email=email, phone_number=phone_number, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            try:
                db.session.add(new_user)
                db.session.commit()  # Commit changes to the database

                login_user(new_user, remember=True)
                flash('Account created! Please log in.', category='success')
                return redirect(url_for('login'))  # Assuming 'login' is the name of your login route
            except Exception as e:
                db.session.rollback()  # Rollback changes in case of an exception
                flash('Error creating account. Please try again.', category='error')
                print(e)

    return render_template('signup.html')


       

@app.route('/account')
@login_required
def account():
    from website.models import User
    # Display user account information
    return render_template('account.html')

@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_file():
    from website.models import User
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            create_upload_folder()
            unique_filename = generate_unique_filename()
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            location = request.form.get('location', '')
            title = request.form.get('title', '')
            bedrooms = int(request.form.get('bedrooms', 0))
            price = float(request.form.get('price', 0.0))

            property_info = {
                'id': unique_filename,
                'filename': filename,
                'location': location,
                'title': title,
                'bedrooms': bedrooms,
                'price': price
            }
            property_list.append(property_info)

            # Save the updated property_list to the file
            with open(PROPERTY_FILE, 'w') as f:
                json.dump(property_list, f, indent=2)

            print(f"Saved file: {filename} at path: {file_path}")

            return redirect(url_for('display_properties'))

    return render_template('1.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/properties')
def display_properties():
    from website.models import User
    if not property_list:
        return render_template('2.html', properties=property_list, no_properties=True)
    else:
        return render_template('2.html', properties=property_list)
        
@app.route('/link_to_2_html')
def link_to_2_html():
    return render_template('2.html', properties=property_list)


@app.errorhandler(413)
def too_large(e):
    return make_response(jsonify(message="File is too large"), 413)


@app.route('/reset_uploads', methods=['POST'])
def reset_uploads():
    # Delete all uploaded files and reset property_list
    for property_info in property_list:
        filename = property_info['filename']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(file_path)

    # Reset property list
    property_list.clear()

    # Save the updated property_list to the file
    with open(PROPERTY_FILE, 'w') as f:
        json.dump(property_list, f, indent=2)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
