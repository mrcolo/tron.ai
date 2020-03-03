import serial
import random
BAUDRATE = 115200
PARITY=serial.PARITY_NONE
STOPBITS=1
DATABITS=16

def readwrite(ser, data_in='0'):
    '''
    ser: Serial port
    data: data string to send
    '''
    #ser.write(1)
    return ser.read(size=1)

if __name__=='__main__':
    data_in = random.randrange(0, 4)
    data_out = str(readwrite(ser,data_in))
    print(':'.join(hex(ord(x))[2:] for x in data_out)
)
