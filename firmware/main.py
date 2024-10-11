"""

0v3:
    well formed json POST http requests
0v4:
    energy management with gprs
0v5:
    post data to firebase
0v6:
    gps management
0v9:
    bmp388+ens160 drivers integrated


"""



import time
import machine
import i2c
import cellular
import gps
import socket
import json
import urequests as requests
import urandom
#--
import bmp388
import ens160


# ---------------------- functions
def pmap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def cropmap(x, in_min, in_max, out_min, out_max):
    ress = 0
    if x>=in_min and x<=in_max:
        ress = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    elif x<in_min:
        ress = 0
    elif x>in_max:
        ress = out_max
    return ress


def f_it(ffnn=1):
    global led
    for k in range(ffnn):
        led.value(1)
        time.sleep_ms(50)
        led.value(0)     
        time.sleep_ms(50)
    return

def sms_handler(evt):
    global flag
    if evt == cellular.SMS_SENT:
        print("[SMS], sent")
        a=1
    else:
        #print("[SMS]: ")
        ls = cellular.SMS.list()
        print(ls)
# ---------------------- end functions



# ---------------------- strings
#API_KEY = "AAAAAAAAABBBBBBBBDDDDDDDDD$$$$$$$$$$HH"

#
DB_URL = "https://pigeonblog-db-default-rtdb.firebaseio.com"
AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
XY_URL = "http://rraaddiioo.ddns.net:8081"
#
pigeon_id = 9999
sesion_id = urandom.randint(10, 10000)
# ---------------------- 



# --- --- --- --- --- --- --- --- --- --- --- --- --- | --SETUP-- |
# --- pins
led = machine.Pin(27, machine.Pin.OUT, 0)
led_val  = 0
# --- init sms handler
cellular.on_sms(sms_handler)
time.sleep(1)
f_it(1)         #- init ok
# --- activate gps and wait for it to connect
gps.on()
print("[GPS] on")
sat_conn = False
while sat_conn == False:
    gps_loc = list(gps.get_location())
    gps_sat = list(gps.get_satellites())
    print("[gps_loc]: %s" % str(gps_loc))
    print("[gps_sats]: %s" % str(gps_sat))
    if (gps_sat[0]>=2):
        sat_conn = True
    else:
        f_it(2)
        time.sleep(5)
f_it(3)         #- gps ok
# --- get a session token
authed = False
while(authed==False):
    try:
        # --- init gprs + gps comms
        there_net = False
        while(there_net==False):
            try:
                conn = cellular.gprs("internet", "", "")
                if (conn): there_net = True
            except:
                conn = cellular.gprs(False)
                #time.sleep_ms(100)
        f_it(3)
        print("[GPRS] on")
        # get session token
        post_url = "{}?key={}".format(AUTH_URL, API_KEY)
        res = requests.post(post_url, json={"returnSecureToken": True})
        if res.status_code == 200:
          token = json.loads(res.text)["idToken"]
          print("[FB]: token OK")
          f_it(4)
        #turn off gprs
        conn = cellular.gprs(False)
        print("[GPRS] off")
        authed = True
    except:
        print("[x.X] cant connect to server")
        f_it(1)
        time.sleep_ms(200)
        f_it(1)
        time.sleep(2)


# --- init i2c
i2c.init(2, 100000)
time.sleep(1)
print("[I2C] on")
f_it(2)

# --- objects for the AIR sensors
sensor_bmp388 = bmp388.DFRobot_BMP388_I2C(i2c)
sensor_ens160 = ens160.DFRobot_ENS160_I2C(i2c)

while (sensor_ens160.begin() == False):
    print ('Please check that the device is properly connected')
    time.sleep(3)
sensor_ens160.set_PWR_mode(ens160.ENS160_STANDARD_MODE)
print("[Sensors] ok")
time.sleep(1)
f_it(4)



# --- --- --- --- --- --- --- --- --- --- --- --- --- | --LOOP-- |
while(1):
    try:
        f_it(1)
        # --- BMP388 readings 
        temp = sensor_bmp388.readTemperature()
        print("Temp : %s C" %temp)
        pres = sensor_bmp388.readPressure()
        print("Pres : %s Pa" %pres)
        alti = sensor_bmp388.readAltitude();
        print("Alti : %s m" %alti)
        f_it(2)
        time.sleep(0.5)
        # --- ENS160 readings
        sensor_ens160_status = sensor_ens160.get_ENS160_status()
        print("status : %u" %sensor_ens160_status)
        aqi = sensor_ens160.get_AQI
        print("AQI  : %u" %aqi)
        tvoc = sensor_ens160.get_TVOC_ppb
        print("TVOC : %u ppb" %tvoc)
        co2 = sensor_ens160.get_ECO2_ppm
        print("CO2  : %u ppm" %co2)
        h2 = cropmap(tvoc, 0, 100, 0.7, 11)
        print("H2  : %u ppm" %h2)
        eth = cropmap (tvoc, 0.2, 11, 1.5, 11.5)
        print("ETH  : %u ppm" %eth)
        meth = cropmap(tvoc, 180, 1050, 1, 2.7)
        print("METH  : %u ppm" %meth)
        co = cropmap(tvoc, 0.8, 2000, 0.2, 0.7)
        print("CO  : %u ppm" %co)
        f_it(3)
        time.sleep(0.5)
        # --- GPS readings
        gps_loc = list(gps.get_location())
        gps_sat = list(gps.get_satellites())
        print("[gps_loc]: %s" % str(gps_loc))
        print("[gps_sats]: %s" % str(gps_sat))
        f_it(3)
        # --- report sms
        #cellular.SMS("+522222048162", msg[:100]).send()
        #time.sleep(5)
        #cellular.SMS("+522222048162", msg2[:100]).send()  
        # ---> send to server
        try:
            #flat schema
            #te = urandom.uniform(20.1, 23.2)
            #pr = urandom.uniform(28.9212, 29.9312)
            #alti = urandom.uniform(2120.00, 2220.00)
            #c1 = urandom.uniform(0.01, 2.00)
            #c2 = urandom.uniform(0.10, 2.00)
            #c3 = urandom.uniform(0.01, 2.00)
            sensors = { "sen{}".format(i): 6.6 for i in range(8) }
            datapack = {
              "timestamp": {".sv": "timestamp"},
              "pigeon": pigeon_id,
              "session_id": sesion_id,
              "lat": gps_loc[0],
              "lon": gps_loc[1],
              "sata": gps_sat[0],
              "satb": gps_sat[1],
              "temp": temp,
              "pres": pres,
              "alti": alti,
              "tvocs": tvoc,
              "co2": co2,
              "h2": h2,
              "eth": eth,
              "meth": meth,
              "co": co, 
              "aqi": aqi,
              "local": time.time(),
              #sensors.items(),
            }
            # ---> connect
            there_net = False
            while(there_net==False):
                try:
                    conn = cellular.gprs("internet", "", "")
                    if (conn): there_net = True
                except:
                    conn = cellular.gprs(False)
            f_it(4)
            print("[GPRS] on")
            # ---> send
            post_url = "{}/measurements.json?auth={}".format(DB_URL, token)
            res = requests.post(post_url, json=datapack)
            print(res.text)
            res = requests.post(XY_URL, json=datapack)
            print(res.text)
            conn = cellular.gprs(False)
            f_it(5)
            print("[GPRS] off")
        except:
            print("[x.X] cant connect to server")
            f_it(3)
            time.sleep_ms(200)
            f_it(3)    
        # --- pause
        for i in range(5):
            led.value(1)
            time.sleep_ms(50)
            led.value(0)     
            time.sleep(1)
        # end of try send to server
    except:
        i2c.close(2)
        conn = cellular.gprs(False)
        print("[x.X] restarting hardware devices")
        i2c.init(2, 100000)
        time.sleep(5)
        
gps.off()
i2c.close(2)






#assert rsp == b'HTTP/1.1 200 OK\r\ncontent-length: 0\r\n\r\n'
