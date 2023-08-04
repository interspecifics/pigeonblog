import i2c
import time
import gps
import cellular
import machine

global flag
flag = 1

def sms_handler(evt):
    global flag
    if evt == cellular.SMS_SENT:
        print("[SMS], sent")
    else:
        print("[SMS]: ")
        ls = cellular.SMS.list()
        print(ls[-1])
        flag = 0

def receive_bytes(nbytes = 8):
    #for i in range(12):
    led.value(1)
    time.sleep_ms(10)
    rec_bytes = i2c.receive(2, 0x77, nbytes, 1)
    rec_ints = [by for by in rec_bytes]
    led.value(0)
    return rec_ints
    #in_data.append(rec_int)
    #

# --- --- --- --- --- --- --- --- --- SETUP
# --- init gps
gps.on()
# --- init sms handler
cellular.on_sms(sms_handler)
# --- init i2c
i2c.init(2, 400)
time.sleep(5)
# --- pins
led = machine.Pin(27, machine.Pin.OUT, 0)
led_val  = 0
# --- set config to bmp388
print("[+-+], bmp388.iir_32")
i2c.transmit(2, 0x77, b'\x1F\x03', 1) 		#-- BMP388_CONFIG
time.sleep(1)
i2c.transmit(2, 0x77, b'\x1C\x03', 1) 		#-- BMP388_OSR 
time.sleep(1)
i2c.transmit(2, 0x77, b'\x1D\x02', 1) 		#-- BMP388_ODR 
time.sleep(1)
i2c.transmit(2, 0x77, b'\x1B\x02', 1) 		#-- BMP388_PWR_CTRL 
time.sleep(1)
#
in_data = receive_bytes(12)
print(in_data, end="\t")
print("")
time.sleep(1)



# --- --- --- --- --- --- --- --- --- LOOP
while(1):
    try:
        # --- Temperature readings
        data_temp = []
        str_temp = ""
        #
        i2c.transmit(2, 0x77, b'\x09', 1)
        in_data = receive_bytes(12)
        data_temp.append(in_data[3:6])
        print("TMSB,", end="\t")
        print(in_data[3:6], end="\t")
        str_temp = str_temp + "TMSB," + str(in_data[3:6]) + "\n"
        print("")
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x08', 1)
        in_data = receive_bytes(12)
        data_temp.append(in_data[4:7])
        print("TLSB,", end="\t")
        print(in_data[4:7], end="\t")
        str_temp = str_temp + "TLSB," + str(in_data[4:7]) + "\n"
        print("")
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x07', 1)
        in_data = receive_bytes(12)
        data_temp.append(in_data[5:8])
        print("TXSB,", end="\t")
        print(in_data[5:8], end="\t")
        str_temp = str_temp + "TXSB," + str(in_data[5:8]) + "\n"
        print("")
        #print(data_temp)
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
        print("PMSB,", end="\t")
        print(in_data[6:9], end="\t")
        str_press = str_press + "PMSB," + str(in_data[6:9]) + "\n"
        print("")
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x05', 1)
        in_data = receive_bytes(12)
        data_press.append(in_data[7:10])
        print("PLSB,", end="\t")
        print(in_data[7:10], end="\t")
        str_press = str_press + "PLSB," + str(in_data[7:10]) + "\n"
        print("")
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x04', 1)
        in_data = receive_bytes(12)
        data_press.append(in_data[8:11])
        print("PXSB,", end="\t")
        print(in_data[8:11], end="\t")
        str_press = str_press + "PXSB," + str(in_data[8:11]) + "\n"
        print("")
        #print(data_press)
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
        print("T2,", end="\t")
        print(in_data[:3], end="\t")
        str_time = str_time + "T2," + str(in_data[:3]) + "\n"
        print("")
        time.sleep_ms(100)
        #
        i2c.transmit(2, 0x77, b'\x0D', 1)
        in_data = receive_bytes(12)
        data_time.append(in_data[:3])
        print("T1,", end="\t")
        print(in_data[:3], end="\t")
        str_time = str_time + "T1," + str(in_data[:3]) + "\n"
        print("")
        time.sleep(1)
        #
        i2c.transmit(2, 0x77, b'\x0C', 1)
        in_data = receive_bytes(12)
        data_time.append(in_data[:3])
        print("T0,", end="\t")
        print(in_data[:3], end="\t")
        str_time = str_time + "T0," + str(in_data[:3]) + "\n"
        print("")
        
        # --- GPS readings
        led.value(1)
        locloc = gps.get_location()
        locsat = gps.get_satellites()
        print("LOC, {}".format(locloc), end=",")
        print("{}".format(locsat))
        led.value(0)
        
        # --- report sms
        print("")
        msg = str(list(locloc)) + " " + str(list(locsat)) + " " + str_temp
        msg2 = str(time.localtime()) + "\n" + str_press + str_time
        print(msg)
        print(msg2)
        #cellular.SMS("+522222048162", msg[:100]).send()
        #time.sleep(5)
        #cellular.SMS("+522222048162", msg2[:100]).send()  
        # --- pause
        for i in range(5):
            led.value(1)
            time.sleep_ms(50)
            led.value(0)     
            time.sleep(1)
    except:
        i2c.close(2)
        print("[x.X] algo fue mal, reestableciendo comunicaciones_...")
        i2c.init(2, 400)
        time.sleep(5)
        

i2c.close(2)
gps.off()
