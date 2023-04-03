from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

# print("All imported properly !")


app = Flask(__name__)


# Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_BINDS'] = {'football':'sqlite:///allFootball.db',
                                'cricket':'sqlite:///allCricket.db',
                                'volley':'sqlite:///allVolley.db',
                                'chess':'sqlite:///allChess.db',
                                'tt':'sqlite:///allTT.db',
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
    roll = db.Column(db.String(), nullable=False, unique=True)
    phno = db.Column(db.String(), nullable=False)


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
# Table Tennis
class AllTableTennis(db.Model):
    __bind_key__='tt'
    name = db.Column(db.String(200))
    roll = db.Column(db.String(200), nullable = False, unique=True, primary_key = True)
# Badminton
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
    name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Full Name"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    sport = SelectField(choices=["Football", "Cricket", "Volleyball", "Chess", "Badminton", "Table Tennis", "Kabaddi"])
    roll = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder":"Your Roll number"})
    phno = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder":"Your Phone number"})
    submit = SubmitField("Register")
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username = username.data).first()
        if existing_user_username:
            flash("Username already exists !")
            raise ValidationError("Username already exists !")
    def validate_sport(self, sport):
        existing_user_sport = User.query.filter_by(sport = sport.data).first()
        if existing_user_sport:
            flash("Sport already exists !")
            raise ValidationError("Sport already Exists !")    
    def validate_roll(self, roll):
        existing_user_roll = User.query.filter_by(roll = roll.data).first()
        if existing_user_roll:
            flash("You are entering someones else's Roll number :( ")
            raise ValidationError("You are entering someones else's Roll number :( ") 
   


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")


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
    elif request.method=='POST' and current_user.sport == 'Table Tennis':
        name = request.form['name']
        roll = request.form['roll']
        player = AllTableTennis(name=name, roll=roll)
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
                            AllVolleyball = AllVolley.query.all(),  AllChess = AllChess.query.all(),
                            AllTableTennis = AllTableTennis.query.all(),  AllKabaddi = AllKabaddi.query.all())



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




# All Players View Page
@app.route("/allPlayersFootball", methods = ["GET", "POST"])
def allPlayersFootball():
    return render_template("allPlayersFootball.html")

@app.route("/allPlayersCricket", methods = ["GET", "POST"])
def allPlayersCricket():
    return render_template("allPlayersCricket.html")

@app.route("/allPlayersVolleyball", methods = ["GET", "POST"])
def allPlayersVolleyball():
    return render_template("allPlayersVolleyball.html")

@app.route("/allPlayersChess", methods = ["GET", "POST"])
def allPlayersChess():
    return render_template("allPlayersChess.html")

@app.route("/allPlayersTableTennis", methods = ["GET", "POST"])
def allPlayersTableTennis():
    return render_template("allPlayersTableTennis.html")

@app.route("/allPlayersKabaddi", methods = ["GET", "POST"])
def allPlayersKabaddi():
    return render_template("allPlayersKabaddi.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)