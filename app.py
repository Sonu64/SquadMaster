from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import EqualTo, InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

# print("All imported properly !")


app = Flask(__name__)


# Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_BINDS'] = {'football':'sqlite:///allFootball.db',
                                'cricket':'sqlite:///allCricket.db',
                                'volley':'sqlite:///allVolley.db',
                                'chess':'sqlite:///allChess.db',
                                'badminton':'sqlite:///allBadminton.db',
                                'kabaddi':'sqlite:///allKabaddi.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "thisisasecretkey"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.app_context().push()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Schema Setup for Admins
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    sport = db.Column(db.String(80), nullable=False, unique=True)
    roll = db.Column(db.Integer(), nullable=False, unique=True)
    phno = db.Column(db.Integer(), nullable=False)
# Schema Setup for Players
# Football
class AllFootball(db.Model):
    __bind_key__='football'
    name = db.Column(db.String(200))
    roll = db.Column(db.String(200), nullable = False, unique=True, primary_key = True)
# Cricket
class AllCricket(db.Model):
    __bind_key__='cricket'
    name = db.Column(db.String(200))
    roll = db.Column(db.String(200), nullable = False, unique=True, primary_key = True)
# Volleyball
class AllVolley(db.Model):
    __bind_key__='volley'
    name = db.Column(db.String(200))
    roll = db.Column(db.String(200), nullable = False, unique=True, primary_key = True)
# Chess
class AllChess(db.Model):
    __bind_key__='chess'
    name = db.Column(db.String(200))
    roll = db.Column(db.String(200), nullable = False, unique=True, primary_key = True)

#Badminton
class AllBadminton(db.Model):
    __bind_key__='badminton'
    name = db.Column(db.String(200))
    roll = db.Column(db.String(200), nullable = False, unique=True, primary_key = True)
# Kabaddi
class AllKabaddi(db.Model):
    __bind_key__='kabaddi'
    name = db.Column(db.String(200))
    roll = db.Column(db.String(200), nullable = False, unique=True, primary_key = True)



class RegisterForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Full Name", "class":"text"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username", "class":"text"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password", "class":"password"})
    sport = SelectField(choices=["Football", "Cricket", "Volleyball", "Chess", "Badminton", "Kabaddi"], render_kw={"class":"text"})
    roll = IntegerField(validators=[InputRequired()], render_kw={"placeholder":"Your Roll number (only numeric part)", "class":"text"})
    phno = IntegerField(validators=[InputRequired()], render_kw={"placeholder":"Your Phone number", "class":"text"})
    submit = SubmitField("Register")
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username = username.data).first()
        if existing_user_username:
            flash("Username already exists !")
            raise ValidationError("Username already exists !")
    def validate_sport(self, sport):
        existing_user_sport = User.query.filter_by(sport = sport.data).first()
        if existing_user_sport:
            flash("Coordinator of this sport already exists !")
            raise ValidationError("Sport already Exists !")    
    def validate_roll(self, roll):
        existing_user_roll = User.query.filter_by(roll = roll.data).first()
        if existing_user_roll:
            flash("You are entering someones else's Roll number :( ")
            raise ValidationError("You are entering someones else's Roll number :( ") 
   


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username", "class":"text", "id":"username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password", "class":"password"})
    submit = SubmitField("Login", render_kw={"id":"submit","class":"submitButton" })


@app.route("/")
def home():
    return render_template("index.html")




# All Dashboards
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method=='POST' and current_user.sport == 'Football':
        name = request.form['name']
        roll = request.form['roll']
        player = AllFootball(name=name, roll=roll)
        db.session.add(player)
        db.session.commit()
    elif request.method=='POST' and current_user.sport == 'Cricket':
        name = request.form['name']
        roll = request.form['roll']
        player = AllCricket(name=name, roll=roll)
        db.session.add(player)
        db.session.commit()
    elif request.method=='POST' and current_user.sport == 'Volleyball':
        name = request.form['name']
        roll = request.form['roll']
        player = AllVolley(name=name, roll=roll)
        db.session.add(player)
        db.session.commit()
    elif request.method=='POST' and current_user.sport == 'Chess':
        name = request.form['name']
        roll = request.form['roll']
        player = AllChess(name=name, roll=roll)
        db.session.add(player)
        db.session.commit()
    elif request.method=='POST' and current_user.sport == 'Badminton':
        name = request.form['name']
        roll = request.form['roll']
        player = AllBadminton(name=name, roll=roll)
        db.session.add(player)
        db.session.commit()
    elif request.method=='POST' and current_user.sport == 'Kabaddi':
        name = request.form['name']
        roll = request.form['roll']
        player = AllKabaddi(name=name, roll=roll)
        db.session.add(player)
        db.session.commit()

    

    return render_template("dashboard.html", AllFootball = AllFootball.query.all(),  AllCricket = AllCricket.query.all(),
                            AllVolleyball = AllVolley.query.all(),  AllChess = AllChess.query.all(), AllBadminton = AllBadminton.query.all(), AllKabaddi = AllKabaddi.query.all(),  sport=current_user.sport)



@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
            else:
                error = "Wrong password !"
        else:
            error = "Username doesn't exist !"
    return render_template("login.html", form = form, error = error)



@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/reg", methods=["GET", "POST"])
def reg():
    error = ""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        sport = User.query.filter_by(sport=form.sport.data).first()
 
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, username=form.username.data, password=hashed_password, sport=form.sport.data, roll=form.roll.data, phno=form.phno.data);
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("reg.html", form = form, error = error)







#Delete player
@app.route('/dashboard/delete/<int:roll>')
def delete(roll):
    if current_user.sport == "Football":
        toDelete = AllFootball.query.filter_by(roll=roll).first()
    if current_user.sport == "Cricket":
        toDelete = AllCricket.query.filter_by(roll=roll).first() 
    if current_user.sport == "Volleyball":
        toDelete = AllVolley.query.filter_by(roll=roll).first() 
    if current_user.sport == "Chess":
        toDelete = AllChess.query.filter_by(roll=roll).first()   
    if current_user.sport == "Kabaddi":
        toDelete = AllKabaddi.query.filter_by(roll=roll).first() 
    if current_user.sport == "Badminton":
        toDelete = AllBadminton.query.filter_by(roll=roll).first() 
    db.session.delete(toDelete)
    db.session.commit()
    return redirect("/dashboard")



@app.route("/sports")
def sports():
    return render_template("sports.html")




@app.route("/allPlayersBadminton")
def allplayersBadminton():
    return render_template("allPlayersBadminton.html", AllPlayers = AllBadminton.query.all())

@app.route("/allPlayersFootball")
def allPlayersFootball():
    return render_template("allPlayersFootball.html", AllPlayers = AllFootball.query.all())

@app.route("/allPlayersCricket")
def allPlayersCricket():
    return render_template("allPlayersCricket.html", AllPlayers = AllCricket.query.all())

@app.route("/allPlayersChess")
def allPlayersChess():
    return render_template("allPlayersChess.html", AllPlayers = AllChess.query.all())

@app.route("/allPlayersKabaddi")
def allPlayersKabaddi():
    return render_template("allPlayersKabaddi.html", AllPlayers = AllKabaddi.query.all())

@app.route("/allPlayersVolleyball")
def allPlayersVolleyball():
    return render_template("allPlayersVolleyball.html", AllPlayers = AllVolley.query.all())

















if __name__ == "__main__":
    app.run(debug=True, port=8000)