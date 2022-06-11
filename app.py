"""Flask Application for Paws Rescue Center."""
from flask import Flask, render_template, abort, redirect, session, url_for
from forms import SignUpForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'

db = SQLAlchemy(app)

"""Model for Pets."""
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.String)
    bio = db.Column(db.String)
    posted_by =  db.Column(db.String, db.ForeignKey('user.id'))


"""Model for Users."""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    pets = db.relationship('Pet', backref = 'user')


db.create_all()

"""Information regarding the Pets in the System."""
pets = [
            {"id": 1, "name": "Nelly", "age": "5 weeks", "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
            {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
            {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
            {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."}, 
        ]

"""Information regarding the Users in the System."""
users = [
            {"id": 1, "full_name": "Pet Rescue Team", "email": "team@pawsrescue.co", "password": "adminpass"},
        ]

"""1. Add a View Function for the Home page."""
@app.route('/')
def home_page():
    return render_template('home.html', pets = pets)

"""2. Add a View Function for the About page."""
@app.route('/about') 
def about_page():
    return render_template('about.html')
    
@app.route("/details/<int:pet_id>")
def pet_details_page(pet_id):
    """View function for Showing Details of Each Pet.""" 
    pet = next((pet for pet in pets if pet["id"] == pet_id), None) 
    if pet is None: 
        abort(404, description="No Pet was Found with the given ID")
    return render_template("details.html", pet = pet)

@app.route("/signup/", methods = ["GET", "POST"])
def signup_page():
    '''Sign up a new User'''
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = {"id": len(users)+1, "full_name": form.full_name.data, "email": form.email.data, "password": form.password.data}
        users.append(new_user) # add new user
        return render_template("signup.html", message = "Successfully signed up!")
    return render_template('signup.html',form = form)

@app.route("/login/", methods = ["GET", "POST"])
def login_page():
    '''Login for existing  users'''
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data), None)
        if existing_user:
            session['user'] = existing_user
            mssg = "Succesfuly Login"
            return render_template('login.html', message=mssg)
        else:
            mssg = "Email "+str(form.email.data)+" does not exist in our records or password is incorrect. Please sign up."
            return render_template('login.html', message=mssg)
    return render_template("login.html",form = form)

@app.route("/logout/")
def logout():
    if 'user' in session:
        session.pop('user')
    # return redirect(url_for('home_page', _scheme='https', _external=True))
    return redirect(url_for('home_page'))
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)