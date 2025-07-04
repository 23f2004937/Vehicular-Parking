from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'Our_Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Home route
@app.route('/')
def home_page():
    return render_template("home.html")

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return f"<h2>Welcome, {user.username}!</h2>"
        else:
            return "<h2>Invalid username or password!</h2>"

    return render_template("login.html")

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        dob_str = request.form.get('dob')
        vehicle_number = request.form.get('vehicle_number')

        if not (username and password and dob_str and vehicle_number):
            return "<h2>Missing required fields!</h2>"

        # Check for duplicate username
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "<h2>Username already taken. Please choose another one.</h2>"

        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            return "<h2>Invalid date format! Please use YYYY-MM-DD format.</h2>"

        # Save new user
        user = User(username=username, password=password, dob=dob, vehicle_number=vehicle_number)
        db.session.add(user)
        db.session.commit()

        return f"<h2>User {username} registered successfully!</h2>"

    return render_template("register.html")

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
