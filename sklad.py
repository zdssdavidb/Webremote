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

# Different colours
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
    r=requests.get('http://{IP ADDRESS}/cm?cmnd=Power%20toggle', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power toggle (On/Off)

def tv_power_toggle():
    import requests
    r=requests.get('http://{IP ADDRESS}/cm?cmnd=Power%20toggle', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power toggle (On/Off)

def tv_power_off():
    import requests
    r=requests.get('http://{IP ADDRESS}/cm?cmnd=Power%20Off', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power OFF
def tv_power_on():
    import requests
    r=requests.get('http://{IP ADDRESS}/cm?cmnd=Power%20On', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power OFF

def humidifier_toggle():
    import requests
    r=requests.get('http://{IP ADDRESS}/cm?cmnd=Power%20toggle', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power Toggle (On/Off)

def cube_power_toggle():
    requests.get('http://{IP ADDRESS}/cm?cmnd=Power%20toggle', auth=('{USERNAME}','{PASSWORD}')) # HTTP Power OFF

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

# returns 10 latest security news (news descriptions)
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

# Not tested
def keyboard_shortcut():
    from pyautogui import press, hotkey
    import os, time
    os.system('DISPLAY=:0.0')
    press('up')
    #time.sleep(1)
    #hotkey('up') 

# get device temperature from PiHole landing page
def WebScraping():
    while True:
        from bs4 import BeautifulSoup
        #get the data
        data = requests.get("http://{IP ADDRESS}/{USERNAME}/")
        #load data into bs4
        soup = BeautifulSoup(data.text, 'html.parser')
        temp = soup.find('span', {'id':'rawtemp'})
        os.system("cls")
        print(temp.text)
        time.sleep(5)

# Sending email to me, need to supply subject and message when calling function (used for daily report and some alerts)
def send_mail(subject, email_body):
    import os,datetime, smtplib
    sender="{SENDER EMAIL}"
    password="{APP PASSWORD for sender email}"
    recipient="{EMAIL ADDRESS of recipient}"
    
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

# Checking VPN status, returns 1 if connected, 0 if not connected (used as a CRON job)
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

# Getting device uptime (for LCD screen)
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
