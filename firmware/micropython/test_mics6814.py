import i2c
import time
    
i2c.init(2, 400)
time.sleep(5)

# ---- poweron sensor heating
print("[+-+]")
j=0
while(j<65):
    #for j in range(64):
    try:
        i2c.transmit(2, 0x18, j.to_bytes(1,"big"), 1)
        in_data = []
        for i in range(64):
            time.sleep_ms(200)
            rec_byte = i2c.receive(2, 0x18, 1, 1)
            rec_int = int.from_bytes(rec_byte, "big")
            in_data.append(rec_int)
        print("[{}],".format(j), end="\t")
        print(in_data, end="\t")
        print("")
        j=j+1
    except:
        i2c.close(2)
        print("[*_*] something's wrong, restarting coms")
        i2c.init(2, 400)
        time.sleep(5)
    time.sleep(1)

#i2c.transmit(2, 0x18, b'\x03\xAA', 1)
"""
while(1):
    # ---- get gas measures
    try:
        i2c.transmit(2, 0x18, b'\x01', 1)
        in_data = []
        for i in range(64):
            time.sleep_ms(200)
            rec_byte = i2c.receive(2, 0x18, 1, 1)
            rec_int = int.from_bytes(rec_byte, "big")
            if(i>=32): in_data.append(rec_int)
        print("CCC,", end="\t")
        print(in_data, end="\t")
        print("")
        time.sleep(1)
        
        i2c.transmit(2, 0x18, b'\x11', 1)
        in_data = []
        for i in range(64):
            time.sleep_ms(200)
            rec_byte = i2c.receive(2, 0x18, 1, 1)
            rec_int = int.from_bytes(rec_byte, "big")
            if(i>=32): in_data.append(rec_int)
        print("NH3,", end="\t")
        print(in_data, end="\t")
        print("")
        time.sleep(1)

        i2c.transmit(2, 0x18, b'\x12', 1)
        in_data = []
        for i in range(64):
            time.sleep_ms(200)
            rec_byte = i2c.receive(2, 0x18, 1, 1)
            rec_int = int.from_bytes(rec_byte, "big")
            if(i>=32): in_data.append(rec_int)
        print("OX,", end="\t")
        print(in_data, end="\t")
        print("")
        time.sleep(1)

        i2c.transmit(2, 0x18, b'\x13', 1)
        in_data = []
        for i in range(64):
            time.sleep_ms(200)
            rec_byte = i2c.receive(2, 0x18, 1, 1)
            rec_int = int.from_bytes(rec_byte, "big")
            if(i>=32): in_data.append(rec_int)
        print("RED,", end="\t")
        print(in_data, end="\t")
        print("")
        time.sleep(1)

        i2c.transmit(2, 0x18, b'\x14', 1)
        in_data = []
        for i in range(64):
            time.sleep_ms(200)
            rec_byte = i2c.receive(2, 0x18, 1, 1)
            rec_int = int.from_bytes(rec_byte, "big")
            if(i>=32): in_data.append(rec_int)
        print("VREF,", end="\t")
        print(in_data, end="\t")
        print("")
    except:
        i2c.close(2)
        print("[*_*] something's wrong, restarting coms")
        i2c.init(2, 400)
    time.sleep(10)
"""
i2c.close(2)
