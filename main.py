##### Webremote #####

from configparser import SafeConfigParser
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import os
from sklad_functions import sklad as skl

parser = SafeConfigParser()
parser.read('config.ini')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "4GShz7"
db = SQLAlchemy()


login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)


db.init_app(app)


# Home page (for logged in users)
@app.route("/")
def home():
	return render_template("home.html") # serving home page, which includes Menu.html with buttons, etc.
with app.app_context():
	db.create_all()


@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)


# I would recommend commenting this block out after 1 user is registered.
# Register new user
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                    password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("sections/sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            user = Users.query.filter_by(
                username=request.form.get("username")).first()
            if user.password == request.form.get("password"):
                login_user(user)
                return redirect(url_for("home"))
        return render_template("sections/login.html")
    except:
        return render_template("sections/login.html")


# Logout user function
@app.route("/logout")
def logout():
    # write_log("Logging Out")
    logout_user()
    return redirect(url_for("login"))


@app.route("/devices")
def devices():
    return render_template("devices.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


# TV Power toggle
@app.route("/tv_power")
def tv_power():
    try:
        skl.tv_power_toggle()
        return redirect(url_for("home"))
    except:
        return redirect(url_for("home"))        # probably device timed out, just returning home screen. Will need to find a way to leave feedback to user that the function failed, but without creating a whole new page for it.


# TV LED toggle
@app.route("/tv_led_toggle")
def tv_led_toggle():
    try:
        data = parser.get('TV_Lights', 'status')
        skl.tv_led_off()
        with open("config.ini", "w") as configfile:
            if data == "1":
                print("LED is ON, turning OFF")
                skl.tv_led_off()
                parser.set('TV_Lights','status',str(0))
                parser.write(configfile)
                configfile.close()
                return redirect(url_for("home"))
            elif data =="0":
                print("LED is OFF, turning ON")
                skl.tv_led_default()
                parser.set('TV_Lights','status',str(1))
                parser.write(configfile)
                configfile.close()
                return redirect(url_for("home"))
            else:
                # print("Oops")
                parser.set('TV_Lights','status',str(0))
                parser.write(configfile)
                configfile.close()
                return redirect(url_for("home"))
    except:
        return "tv_led_toggle Function Failed!"


# TV LED color shuffle 
@app.route("/tv_led_shuffle")
def tv_led_shuffle():
    data = parser.get('TV_Lights', 'color')
    with open("color", "w") as configfile:
        if data == "DEFAULT":
            print("LED is Default")
            skl.tv_led_default()
            parser.set('TV_Lights','status','BLUE')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        elif data =="BLUE":
            print("LED is BLUE")
            skl.tv_led_yellow()
            parser.set('TV_Lights','status','YELLOW')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        elif data =="YELLOW":
            print("LED is YELLOW")
            skl.tv_led_yellow()
            parser.set('TV_Lights','status','GREEN')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        elif data =="GREEN":
            print("LED is GREEN")
            skl.tv_led_green()
            parser.set('TV_Lights','status','PINK')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        elif data =="PINK":
            print("LED is PINK")
            skl.tv_led_pink()
            parser.set('TV_Lights','status','DEFAULT')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))


# Cube power toggle
@app.route("/Cube_power_toggle")
def cube_pw_toggle():
	try:
		skl.cube_power_toggle()
		return redirect(url_for("home"))
	except:
		return "cube_power_toggle Function Failed!"


# get weather data
@app.route('/get_weather', methods = ['GET', 'POST'])
def get_weather():
	# try:
	import time
	# os.chdir("/home/pi/scripts")
	print("################# PWD Start of Weather function!", os.getcwd())
	skl.get_weather_full()
	time.sleep(1)
	# os.chdir("/var/www/html/webremote/templates")
	print("################# PWD at End of Weather function!", os.getcwd())	
	return redirect(url_for("home")) 
	# except:
	# 	return redirect(url_for("home"))


# Table power toggle
@app.route("/table_power_toggle")
def table_pw_toggle():
	try:
		skl.table_toggle()
		return redirect(url_for("home"))
	except ConnectionError:
		return "Unable to connect to Table Sensor."
	except:
		return "Some error when running function table_toggle."

host = parser.get('Web','ip')
port = parser.getint('Web','port')
debug = parser.getboolean('Web','debug')

# Running server
if __name__ == "__main__":
	app.run(host=host, port=port, debug=debug)	
