##### Webremote #####

from configparser import ConfigParser
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import os
from sklad_functions import sklad as skl
import webbrowser

parser = ConfigParser()
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
# @app.route('/register', methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         user = Users(username=request.form.get("username"),
#                     password=request.form.get("password"))
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for("login"))

#     return render_template("sections/sign_up.html")


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
        return render_template("error.html")        # probably device timed out, just returning home screen. Will need to find a way to leave feedback to user that the function failed, but without creating a whole new page for it.


# TV LED toggle
@app.route("/tv_led_toggle")
def tv_led_toggle():
    try:
        data = parser.get('TV_LIGHTS', 'status')
        skl.tv_led_off()
        with open("config.ini", "w") as configfile:
            if data == "1":
                print("LED is ON, turning OFF")
                skl.tv_led_off()
                parser.set('TV_LIGHTS','status',str(0))
                parser.write(configfile)
                configfile.close()
                return redirect(url_for("home"))
            elif data =="0":
                print("LED is OFF, turning ON")
                skl.tv_led_default()
                parser.set('TV_LIGHTS','status',str(1))
                parser.write(configfile)
                configfile.close()
                return redirect(url_for("home"))
            else:
                parser.set('TV_LIGHTS','status',str(0))     # scenario 3, forcing lights off.
                parser.write(configfile)
                configfile.close()
                return redirect(url_for("home"))
    except:
        return render_template("error.html")


# TV LED color shuffle 
@app.route("/tv_led_shuffle")
def tv_led_shuffle():
    data = parser.get('TV_LIGHTS', 'colour')
    with open("colour", "w") as configfile:
        if data == "DEFAULT":
            print("LED is Default")
            skl.tv_led_default()
            parser.set('TV_LIGHTS','colour','BLUE')     # write the value of next colour in the line (sklad functions)
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        elif data =="BLUE":
            print("LED is BLUE")
            skl.tv_led_blue()
            parser.set('TV_LIGHTS','colour','YELLOW')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        elif data =="YELLOW":
            print("LED is YELLOW")
            skl.tv_led_yellow()
            parser.set('TV_LIGHTS','colour','GREEN1')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        elif data =="GREEN1":
            print("LED is GREEN1")
            skl.tv_led_green1()
            parser.set('TV_LIGHTS','colour','GREEN2')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        elif data =="GREEN2":
            print("LED is GREEN2")
            skl.tv_led_green2()
            parser.set('TV_LIGHTS','colour','PINK')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        elif data =="PINK":
            print("LED is PINK")
            skl.tv_led_pink()
            parser.set('TV_LIGHTS','colour','DEFAULT')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))
        else:
            print("LED is Default (Force)")
            skl.tv_led_default()
            parser.set('TV_LIGHTS','colour','DEFAULT')
            parser.write(configfile)
            configfile.close()
            return redirect(url_for("home"))

# Cube power toggle
@app.route("/cube_power_toggle")
def cube_pw_toggle():
	try:
		skl.cube_power_toggle()
		return redirect(url_for("home"))
	except:
		return render_template("error.html")

# get weather data (serve static page, it gets updated using crontab entries OR a sklad function)
@app.route('/get_weather', methods = ['GET', 'POST'])
def get_weather():
    try:
        return render_template("weather.html")
    except:
        return render_template("error.html")

# Grafana Dashboard inside iframe (static html page)
@app.route('/get_temp', methods = ['GET', 'POST'])
def get_temp():
    try:
        return render_template("grafana.html")
    except:
        return render_template("error.html")

# Reset XRDP service (when stuck, on demand)
@app.route('/res_xrdp', methods = ['GET', 'POST'])
def res_xrdp():
    try:
        os.system("sudo systemctl restart xrdp.service")
        return redirect(url_for("home"))
    except:
        return render_template("error.html")

# Table power toggle
@app.route("/table_power_toggle")
def table_pw_toggle():
	try:
		skl.table_toggle()
		return redirect(url_for("home"))
	except ConnectionError:
		return "Unable to connect to Table Sensor."
	except:
		return render_template("error.html")


host = parser.get('WEB','ip')
port = parser.getint('WEB','port')
debug = parser.getboolean('WEB','debug')

url = f"http://{host}:{port}"


# Running server
if __name__ == "__main__":
    if parser.getint('MISC','launch') == 1:
        webbrowser.open(url,new=2)
    app.run(host=host, port=port, debug=debug)	
