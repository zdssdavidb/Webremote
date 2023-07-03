import paho.mqtt.client as mqtt, time, sys
import paho.mqtt.client as mqtt

last_topic = "TABLE"
lasy_payload = ""

# apiKey = "xxxxxxxxxxxxxxxx"  # Put the API key here 
client = mqtt.Client()
client.connect("192.168.0.99",1883,60)

# main
def on_connect(client, userdata, flags, rc):
    print("Connected...\n")
    client.is_connected = True

def on_message(client, userdata, message):
    ''' note: message is a tuple of (topic, payload, qos, retain)'''
    global last_topic, last_payload
    last_topic = message.topic
    last_payload = message.payload
    print("Message with topic: [" + last_topic + "] and payload [" + last_payload + "]")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.is_connected = False
client.loop_start()
client.connect("192.168.0.205")

time.sleep(4)
if not client.is_connected:
    print("problem connecting to the MQTT server; please check your settings")
    sys.exit(1)

# ask for system status
time.sleep(1)
client.subscribe("channels/sonoff/TABLE")
client.publish("cmnd/channels/sonoff/status",None)

# now wait for a time stamp from the sonoff; this could take an hour
client.subscribe("channels/sonoff/TABLE")

while 1:
    if last_topic.startswith("channels/sonoff") and last_topic.endswith("TABLE"):
        Payload_Temp = last_payload.find('"Temperature":')
        Payload_Hum = last_payload.find('"Humidity":')
        Temp = last_payload[Payload_Temp+14:Payload_Temp+14+4]
        Hum = last_payload[Payload_Hum+11:Payload_Hum+11+4]
        print("Temperature is: "+Temp +"C")
        print("Humidity is: "+Hum +"%")
        print("")
        client = mqtt.Client()
        client.connect("mqtt.thingspeak.com",1883,60)
        client.publish("channels/%s/publish/%s" % "field1=" + str(Temp) + "&field2=" + str(Hum))    
#        break
        client.publish()
    time.sleep(32)# Couse Thingspeak accept only every 15 sec new value!

client.loop_stop()
client.disconnect()