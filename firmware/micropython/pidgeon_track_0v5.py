"""

0v3:
    well formed json POST http requests
0v4:
    energy management with gprs
0v5:
    post data to firebase

"""



# Get online
import time
import i2c
import machine
import cellular
import gps
import socket
import json
import urequests as requests


# ---------------------- functions
def sms_handler(evt):
    global flag
    if evt == cellular.SMS_SENT:
        #print("[SMS], sent")
        a=1
    else:
        #print("[SMS]: ")
        ls = cellular.SMS.list()
        print(ls)

def receive_bytes(nbytes = 8):
    #for i in range(12):
    led.value(1)
    time.sleep_ms(10)
    rec_bytes = i2c.receive(2, 0x77, nbytes, 1)
    rec_ints = [by for by in rec_bytes]
    led.value(0)
    #print(rec_ints)
    return rec_ints

def pmap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def f_it(ffnn=1):
    global led
    for k in range(ffnn):
        led.value(1)
        time.sleep_ms(50)
        led.value(0)     
        time.sleep_ms(50)
    return

# ---------------------- end functions



# ---------------------- strings
#
#API_KEY = "AAAAAAAAABBBBBBBBDDDDDDDDD$$$$$$$$$$HH"
API_KEY = "AIzaSyD7PKf4dyLQv0QeR_VuB6nNZBBecSZWPzw"
#
DB_URL = "https://pigeonblog-db-default-rtdb.firebaseio.com"
AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"



# --- --- --- --- --- --- --- --- --- SETUP
# --- pins
led = machine.Pin(27, machine.Pin.OUT, 0)
led_val  = 0
time.sleep(1)
f_it(1)

# --- init sms handler
cellular.on_sms(sms_handler)

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
        f_it(4)
        print("[GPRS] on")
        # get session token
        post_url = "{}?key={}".format(AUTH_URL, API_KEY)
        res = requests.post(post_url, json={"returnSecureToken": True})
        if res.status_code == 200:
          token = json.loads(res.text)["idToken"]
          print("[FB]: token OK")
          f_it(5)
        #turn off gprs
        conn = cellular.gprs(False)
        print("[GPRS] off")
        authed = True
    except:
        print("[x.X] cant connect to server")
        f_it(2)
        time.sleep_ms(200)
        f_it(2)
        time.sleep(2)


# --- init i2c
i2c.init(2, 400)
time.sleep(5)
print("[I2C] on")
f_it(2)
# --- set config to bmp388
print("[+-+], bmp388.iir_32")
f_it()
i2c.transmit(2, 0x77, b'\x1F\x03', 1) 		#-- BMP388_CONFIG
time.sleep(1)
i2c.transmit(2, 0x77, b'\x1C\x03', 1) 		#-- BMP388_OSR 
time.sleep(1)
i2c.transmit(2, 0x77, b'\x1D\x02', 1) 		#-- BMP388_ODR 
time.sleep(1)
i2c.transmit(2, 0x77, b'\x1B\x02', 1) 		#-- BMP388_PWR_CTRL 
time.sleep(1)
in_data = receive_bytes(12)
print(in_data)
time.sleep(1)
f_it()
#

# --- --- --- --- --- --- --- --- --- LOOP
while(1):
    try:
        # start the GPS
        gps.on()
        f_it(3)
        locloc = gps.get_location()
        locsat = gps.get_satellites()
        print("[GPS] on")
        # --- Temperature readings
        data_temp = []
        str_temp = ""
        #
        i2c.transmit(2, 0x77, b'\x09', 1)
        in_data = receive_bytes(12)
        data_temp.append(in_data[3:6])
        str_temp = str_temp + "TMSB," + str(in_data[3:6]) + "\n"
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x08', 1)
        in_data = receive_bytes(12)
        data_temp.append(in_data[4:7])
        str_temp = str_temp + "TLSB," + str(in_data[4:7]) + "\n"
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x07', 1)
        in_data = receive_bytes(12)
        data_temp.append(in_data[5:8])
        str_temp = str_temp + "TXSB," + str(in_data[5:8]) + "\n"

        #adcTemp = (data_temp[0][0] << 16) | (data_temp[1][0] << 8) | (data_temp[2][0])    
        #adcTemp1 = (data_temp[0][1] << 16) | (data_temp[1][1] << 8) | (data_temp[2][1])    
        adcTemp = (data_temp[0][0] << 8) | (data_temp[1][0] )
        adcTemp1 = (data_temp[0][1] << 8) | (data_temp[1][1] )
        time.sleep_ms(100)
        
        # --- Pressure readings
        data_press = []
        str_press = ""
        #
        i2c.transmit(2, 0x77, b'\x06', 1)
        in_data = receive_bytes(12)
        data_press.append(in_data[6:9])
        str_press = str_press + "PMSB," + str(in_data[6:9]) + "\n"
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x05', 1)
        in_data = receive_bytes(12)
        data_press.append(in_data[7:10])
        str_press = str_press + "PLSB," + str(in_data[7:10]) + "\n"
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x04', 1)
        in_data = receive_bytes(12)
        data_press.append(in_data[8:11])
        str_press = str_press + "PXSB," + str(in_data[8:11]) + "\n"

        adcPress = (data_press[0][0] << 8) | (data_press[1][0])
        adcPress1 = (data_press[0][1] << 8) | (data_press[1][1])
        time.sleep_ms(100)
     
        # --- time readings
        data_time = []
        str_time = ""
        # 
        i2c.transmit(2, 0x77, b'\x0E', 1)
        in_data = receive_bytes(12)
        data_time.append(in_data[:3])
        str_time = str_time + "T2," + str(in_data[:3]) + "\n"
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x0D', 1)
        in_data = receive_bytes(12)
        data_time.append(in_data[:3])
        str_time = str_time + "T1," + str(in_data[:3]) + "\n"
        time.sleep(1)
        #
        i2c.transmit(2, 0x77, b'\x0C', 1)
        in_data = receive_bytes(12)
        data_time.append(in_data[:3])
        str_time = str_time + "T0," + str(in_data[:3]) + "\n"
        
        # --- GPS readings
        led.value(1)
        locloc = gps.get_location()
        locsat = gps.get_satellites()
        ##print("LOC, {}".format(locloc), end=",")
        ##print("{}".format(locsat))
        gps.off()
        led.value(0)
        print("[GPS] off")

        # --- report sms
        msg = str(list(locloc)) + " " + str(list(locsat)) + "\n" + str_temp
        msg2 = str(time.localtime()) + "\n" + str_press + str_time
        #print("")
        print(msg)
        print(msg2)
        #cellular.SMS("+522222048162", msg[:100]).send()
        #time.sleep(5)
        #cellular.SMS("+522222048162", msg2[:100]).send()  
        
        # --- send to server
        try:
            #flat schema
            pigeon_id = 1010
            sensors = { "sen{}".format(i): 6.6 for i in range(8) }
            datapack = {
              "timestamp": {".sv": "timestamp"},
              "pigeon": pigeon_id,
              "lat": locloc[0],
              "lon": locloc[1],
              "sata": locsat[0],
              "satb": locsat[1],
              "temp": sum([sum(data_temp[i]) for i in range(len(data_temp))])/3,
              "pres": sum([sum(data_press[i]) for i in range(len(data_press))])/3,
              "alti": sum([sum(data_time[i]) for i in range(len(data_time))])/3,
              "NH3": 19.99,
              "OXI": 20.01,
              "RED": 20.03,
              "local": time.time(),
              #sensors.items(),
            }
            # comms on
                        # --- init gprs + gps comms
            there_net = False
            while(there_net==False):
                try:
                    conn = cellular.gprs("internet", "", "")
                    if (conn): there_net = True
                except:
                    conn = cellular.gprs(False)
            f_it(4)
            print("[GPRS] on")
            #conn = cellular.gprs("internet", "", "")
            #print("[GPRS] on")
            post_url = "{}/measurements.json?auth={}".format(DB_URL, token)
            res = requests.post(post_url, json=datapack)
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
        for i in range(15):
            led.value(1)
            time.sleep_ms(50)
            led.value(0)     
            time.sleep(1)
        # end of try

    except:
        i2c.close(2)
        gps.off()
        conn = cellular.gprs(False)
        #print("[x.X] restarting hardware devices")
        i2c.init(2, 400)
        time.sleep(5)
        

i2c.close(2)






#assert rsp == b'HTTP/1.1 200 OK\r\ncontent-length: 0\r\n\r\n'