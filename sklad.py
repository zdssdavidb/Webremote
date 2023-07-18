import datetime, requests, time, os, json, re
from subprocess import check_output

# TV LED Control
def led_on():
    import RPi.GPIO as gpio
    gpio.setwarnings(False)                         #set warnings off
    gpio.setmode(gpio.BOARD)
    gpio.setup(11, gpio.OUT)                        #Blue LED 1
    gpio.setup(12, gpio.OUT)                        #Blue LED 2
    gpio.setup(13, gpio.OUT)                        #Blue LED 3

    gpio.output(11, gpio.HIGH)                      #turn on LED 1
    gpio.output(12, gpio.HIGH)                      #turn on LED 2
    gpio.output(13, gpio.HIGH)                      #turn on LED 3
    x = datetime.datetime.now()
    hour2 = str(x.strftime("%H:%M:%S"))
    #print("Mood LED On at {}".format(hour2))

def led_off():
    import RPi.GPIO as gpio
    gpio.setwarnings(False)                         #set warnings off
    gpio.setmode(gpio.BOARD)
    gpio.setup(11, gpio.OUT)                        #Blue LED 1
    gpio.setup(12, gpio.OUT)                        #Blue LED 2
    gpio.setup(13, gpio.OUT)                        #Blue LED 3

    gpio.output(11, gpio.LOW)                       #turn off LED 1
    gpio.output(12, gpio.LOW)                       #turn off LED 2
    gpio.output(13, gpio.LOW)                       #turn off LED 3
    x = datetime.datetime.now()
    hour2 = str(x.strftime("%H:%M:%S"))
    #print("Mood LED OFF at {}".format(hour2))

def tv_led_default():
    os.system("pigs p 23 100")  #red
    os.system("pigs p 22 100")  #green
    os.system("pigs p 24 150")  #blue
    os.system("echo '1'>/var/www/html/webremote/status")

def tv_led_blue():
    os.system("pigs p 23 0")  #red
    os.system("pigs p 22 0")  #green
    os.system("pigs p 24 255")  #blue

def tv_led_yellow():
    os.system("pigs p 23 250")  #red
    os.system("pigs p 22 100")  #green
    os.system("pigs p 24 0")  #blue
    
def tv_led_green():
    os.system("pigs p 23 0")  #red
    os.system("pigs p 22 255")  #green
    os.system("pigs p 24 70")  #blue

def tv_led_pink():
    os.system("pigs p 23 196")  #red
    os.system("pigs p 22 0")  #green
    os.system("pigs p 24 183")  #blue
        
def tv_led_off():
    os.system("pigs p 23 0")  #red
    os.system("pigs p 22 0")  #green
    os.system("pigs p 24 0")  #blue
    os.system("echo '0'>/var/www/html/webremote/status")

# Misc TV LED functions        
def DoubleBlueFlash():
    tv_led_off()
    time.sleep(0.5)
    for x in range(2):
        os.system("pigs p 23 0")  #red
        os.system("pigs p 22 0")  #green
        os.system("pigs p 24 255")  #blue
        time.sleep(0.3)
        tv_led_off()
        time.sleep(0.2)

def DoubleRedFlash():
    tv_led_off()
    time.sleep(0.5)
    for x in range(2):
        os.system("pigs p 23 255")  #red
        os.system("pigs p 22 0")  #green
        os.system("pigs p 24 0")  #blue
        time.sleep(0.3)
        tv_led_off()
        time.sleep(0.2)

def DoubleGreenFlash():
    tv_led_off()
    time.sleep(0.5)
    for x in range(2):
        os.system("pigs p 23 0")  #red
        os.system("pigs p 22 255")  #green
        os.system("pigs p 24 0")  #blue
        time.sleep(0.3)
        tv_led_off()
        time.sleep(0.2)

# Smart sockets (Sonoff/Tasmota)
def bed_light_toggle():
    import requests
    r=requests.get('http://{DEVICE IP]/cm?cmnd=Power%20toggle', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power toggle

def tv_power_toggle():
    import requests
    r=requests.get('http://{DEVICE IP]/cm?cmnd=Power%20toggle', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power toggle

def tv_power_off():
    import requests
    r=requests.get('http://{DEVICE IP]/cm?cmnd=Power%20Off', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power OFF
    
def tv_power_on():
    import requests
    r=requests.get('http://{DEVICE IP]/cm?cmnd=Power%20On', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power ON

def table_toggle():
    import requests
    r=requests.get('http://{DEVICE IP]/cm?cmnd=Power%20toggle', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power to$

def table_power_off():
    import requests
    r=requests.get('http://{DEVICE IP]/cm?cmnd=Power%20Off', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power to$

def table_power_on():
    import requests
    r=requests.get('http://{DEVICE IP]/cm?cmnd=Power%20On', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power to$
    
def cube_power_toggle():
    requests.get('http://{DEVICE IP]/cm?cmnd=Power%20toggle', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power OFF

# Misc
def Get_weather_forecast1():
    from bs4 import BeautifulSoup
    import requests, re
    data = requests.get("https://www.bbc.co.uk/weather/2648579")
    soup = BeautifulSoup(data.text, 'html.parser')
    temp_description = soup.find('div', {'class':'wr-day__weather-type-description'})
    temps_raw = soup.find_all('span', {'class':'wr-value--temperature--c'})[:2]
    temps_high_low=[]
    try:
        for x in temps_raw:
            x = re.findall("(?:>[\d]+|>-[\d]+)", str(x))[0][1:]
            temps_high_low.append(x)
        return f"Weather: {temp_description.text}.\nTemperatures, Max: {temps_high_low[0]}, Min: {temps_high_low[1]}"
    except:
        return "Weather function failed!"

def Get_weather_forecast2():                    # AccuWeather API
    api_key="KdHB4JVWyEGmPzBoG0oBDJpzxBUGnf6b"
    weather_data=requests.get(f"http://weather_dataservice.accuweather.com/currentconditions/v1/328226?apikey={api_key}")           # get weather using location key ("328226" = Glasgow)
    weather_data=json.loads(weather_data.text)     # get weather text
    weather_text=weather_data[0]['Temperature']
    temperature=weather_data[0]['Temperature']['Metric']['Value']

def get_news():
    try:
        from bs4 import BeautifulSoup
        import re, requests
        news_data = requests.get("https://techcrunch.com/category/security/")
        soup = BeautifulSoup(news_data.text, 'html.parser')
        all_news=soup.find_all('div')         # get all <div's
        news=[]
        for row in all_news:                  # for all lines in all_news
            headers=row.find_all('div')         # find deeper <div's
            for article in headers:             # iterate through above
                if article.attrs == {'class': ['post-block__content']}:   # if <div has the right class attribute
                    x=re.sub('\n','', article.text)
                    x=re.sub('\t','', x)
                    x=re.sub('“','', x)
                    x=re.sub('’','', x)
                    x=re.sub('”','', x)
                    x=re.sub('&','', x)
                    if len(x)>3:
                        if len(x)>130:
                            x=x[:130]                    
                        news.append(x)     # add to news list
        news=news[:10]        # keep only 10 news
        return(news)
    except:
        return("News function failed!")
    
def keyboard_shortcut():
    from pyautogui import press, hotkey
    import os, time
    os.system('DISPLAY=:0.0')
    press('up')
    #time.sleep(1)
    #hotkey('up') 

def WebScraping():
    #get specific data
    while True:
        from bs4 import BeautifulSoup
        #get the data
        data = requests.get("http://{DEVICE IP]/{USERNAME}/")
        #load data into bs4
        soup = BeautifulSoup(data.text, 'html.parser')
        temp = soup.find('span', {'id':'rawtemp'})
        os.system("cls")
        print(temp.text)
        time.sleep(5)

# Sending email to me, need to supply subject and message when calling function
def send_mail(subject, email_body):
    import os,datetime, smtplib

    sender="{EMAIL ADDRESS}"
    password="{APP PASSWORD}"
    recipient="{EMAIL ADDRESS}"
    
    x = datetime.datetime.now()         # date/time
    date=x.strftime("%d %B %Y")

    message = "Subject: {}\n\n".format(subject)
    message += email_body   
    message += "."
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender,recipient, message)
    server.quit()

# Checking VPN status, returns 1 if connected, 0 if not connected.
def get_vpn_status():
    try:
      vpn_status = check_output(["sudo", "nordvpn","status"])
      vpn_status=str(vpn_status)          # needs to be this way
      vpn_status2=str(re.findall("Status:\s[\w]+",vpn_status[2:-1]))
      vpn_status2=vpn_status2.split(' ')[1][:-2]
      
      if vpn_status2 == 'Connected':
          return 1
      elif vpn_status2 == 'Disconnected':
          return 0
      else:
          return "FAILED!"
    except:
      return "FAILED!"

def get_uptime():
  try:
    os.system("uptime >uptime")
    f=open('uptime')
    uptime=f.readlines()
    f.close()
    uptime=' '.join(uptime)
    uptime=str(re.findall("up\s[\d]+",uptime)).split(' ')[1][:-2]
    if len(uptime)>4:
        return "0"
    else:
        return uptime
  except:
    return "0"

# Getting 10 day forecast (high/low temps + descriptions, saving to/generating weather.html file)
def get_weather_full():
    import requests
    from bs4 import BeautifulSoup

    response = requests.get("https://www.bbc.co.uk/weather/2648579")
    # response.status_code
    soup = BeautifulSoup(response.content, "html.parser")
    # Collecting weather descriptions
    temp = soup.find("div", class_="wr-day-summary")
    dirty_weather_descriptions = temp.find_all("span", class_="wr-hide")
    clean_weather_descriptions = []
    clean_weather_descriptions.append(soup.find("div",class_="wr-day__weather-type-description wr-js-day-content-weather-type-description wr-day__content__weather-type-description--opaque").text)
    for entry in dirty_weather_descriptions:
        clean_weather_descriptions.append(entry.text)
    # print("Weather descriptions:", clean_weather_descriptions)            # checking so far

    # Collecting all dates
    temp = soup.find_all("div", class_="wr-day__title wr-js-day-content-title")
    dates = []
    for entry in temp:
        x = entry.text.split('\xa0')[0]       # keeping only the day name
        dates.append(x)
    # print("Dates:", dates)          # checking so far

    # Collecting temperatures (high and low)
    all_temps_dirty = soup.find_all("div", class_="wr-day__temperature")
    weather_data = []
    for index, entry in enumerate(all_temps_dirty):
        high_temps = entry.find("span", class_="wr-day-temperature__high-value")
        try:
            high_temp = high_temps.select('.wr-value--temperature--c')[0].get_text()
        except:
            high_temp = "NONE"
        low_temps = entry.find("span", class_="wr-day-temperature__low-value")
        low_temp = low_temps.select('.wr-value--temperature--c')[0].get_text()
        weather_data.append({"date": dates[index], "high_temp": high_temp, "low_temp": low_temp, "description": clean_weather_descriptions[index]})

   # Generating HTML page with weather forecast.
    html_str = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>10 days Weather Forecast</title>
    </head>
    <body style="background-color:Black;">
    <div style="color:White;", align='center'>
    <dl>
    """
   
    for entry in weather_data:
        html_str += "<dt>" +  entry['date'].encode('ascii', 'ignore').decode('ascii') + "</dt>"
        html_str += "<dd>" +  entry['description'].encode('ascii', 'ignore').decode('ascii') + ".</dd>"
        html_str += "<dd>Max temp: " +  entry['high_temp'].encode('ascii', 'ignore').decode('ascii') + "</dd>"
        html_str += "<dd>Min temp: " +  entry['low_temp'].encode('ascii', 'ignore').decode('ascii') + "</dd><br>"

    html_str += """
    </dl>
    </div>
    </body>
    </html>
    """
    # Saving HTML page
    os.chdir("/var/www/html/webremote/templates")
    Html_file= open("weather.html","w")
    Html_file.write(html_str)
    Html_file.close()

# pulling temp/humidity data from table sensor
def get_table_temp():
    import os, requests, json
    r = requests.get('http://{DEVICE IP]/cm?cmnd=status%208', auth=('{USERNAME}','{PASSWORD}'))
    # print("Collected data: ",r.text)
    if r.status_code==200:
        response = r.json()['StatusSNS']['DHT11']
        os.chdir("/home/pi/logs")
        now = datetime.datetime.now()
        os.system(f"echo {now.strftime('%x %X')},{response['Temperature']},{response['Humidity']},{ response['DewPoint']} >>table_log.csv")
    else:
        print("Couldn't get data")


# Testing stuff
def tv_led_toggle123():
	f = open("/var/www/html/webremote/status", 'r')
	data = f.read()
	f.close()
	from sklad import tv_led_off, tv_led_default
	with open("/var/www/html/webremote/status", "w") as file:
		if data == "1":
			print("LED is ON, turning OFF")
			tv_led_off()
			print(data)
			file.write("0")
			return "hello"
		elif data =="0":
			print("LED is OFF, turning ON")
			tv_led_default()
			print(data)
			file.write("1")
			return "hello"
		else:
			print("Oops\n")
			print(data)
			file.write("0")
			return "hello"
