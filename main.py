##### Webremote #####

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import os
import sklad_functions as skl


### Loging test ###
# from datetime import date

# Initial logfile test for logDisplay
# l = open("logFile.txt", "a")

# def write_log(): # Add message for log functionality
#    now = datetime.datetime.now()
#    l.write(now," - ",message)
   

# write_log("Starting")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "4GShz7"
db = SQLAlchemy()

# write_log("Configured database")

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
	return render_template("home.html")			# serving home page, which includes Menu.html with buttons, etc.
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
        from sklad import tv_power_toggle
        tv_power_toggle()
        return redirect(url_for("home"))
    except:
        return redirect(url_for("home"))        # probably device timed out, just returning home screen. Will need to find a way to leave feedback to user that the function failed, but without creating a whole new page for it.


# TV LED toggle
@app.route("/tv_led_toggle")
def tv_led_toggle():
	try:
		f = open("status", 'r')
		data = f.read()
		f.close()
		from sklad import tv_led_off, tv_led_default
		tv_led_off()
		with open("status", "w") as file:
			if data == "1":
				print("LED is ON, turning OFF")
				tv_led_off()
				file.write("0")
				return redirect(url_for("home"))
			elif data =="0":
				print("LED is OFF, turning ON")
				tv_led_default()
				file.write("1")
				return redirect(url_for("home"))
			else:
				# print("Oops")
				file.write("0")
				return redirect(url_for("home"))
	except:
		return "tv_led_toggle Function Failed!"


# TV LED color shuffle 
@app.route("/tv_led_shuffle")
def tv_led_shuffle():
	from sklad import tv_led_blue, tv_led_yellow, tv_led_green, tv_led_pink, tv_led_default
	f = open("color", 'r')
	data = f.read()
	f.close()
	with open("color", "w") as file:
		if data == "DEFAULT":
			print("LED is Default")
			tv_led_default()
			file.write("BLUE")					# WRITE WHAT NEXT COLOR SHOULD BE
			return redirect(url_for("home"))
		elif data =="BLUE":
			print("LED is BLUE")
			tv_led_yellow()
			file.write("YELLOW")
			return redirect(url_for("home"))
		elif data =="YELLOW":
			print("LED is YELLOW")
			tv_led_yellow()
			file.write("GREEN")
			return redirect(url_for("home"))
		elif data =="GREEN":
			print("LED is GREEN")
			tv_led_green()
			file.write("PINK")
			return redirect(url_for("home"))
		elif data =="PINK":
			print("LED is PINK")
			tv_led_pink()
			file.write("DEFAULT")
			return redirect(url_for("home"))
		# else:
		# 	print("LED is Default (Force)")
		# 	tv_led_default()
		# 	file.write("DEFAULT")
		# 	return redirect(url_for("home"))


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


# Running server
if __name__ == "__main__":
	app.run(host="127.0.0.1", port=8080, debug=True)	
	# app.run(host="{INTERFACE IP}", port=8080, debug=False)	# define IP and port
    # app.run(host="100.79.200.135", port=8080, debug=False)	# alternative interface for VPN (either/or)
