# TV LED color shuffle 
@app.route("/tv_led_shuffle")
def tv_led_shuffle():
	from sklad import tv_led_blue, tv_led_yellow, tv_led_green, tv_led_pink, tv_led_default
	f = open("color", 'r')
	data = f.read()
	f.close()
    with open("color", "w") as file:
		if data == "DEFAULT":
			# print("LED is BLUE")
			tv_led_default()
			file.write("BLUE")
			return redirect(url_for("home"))
		elif data =="BLUE":
			# print("LED is YELLOW")
			tv_led_yellow()
			file.write("YELLOW")
			return redirect(url_for("home"))
		elif data =="YELLOW":
			# print("LED is BLUE")
			tv_led_default()
			file.write("GREEN")
			return redirect(url_for("home"))
		elif data =="GREEN":
			# print("LED is BLUE")
			tv_led_default()
			file.write("PINK")
			return redirect(url_for("home"))
		elif data =="PINK":
			# print("LED is BLUE")
			tv_led_default()
			file.write("DEFAULT")
			return redirect(url_for("home"))
		else:
			# print("Oops")
			file.write("DEFAULT")
			return redirect(url_for("home"))
 
 
 