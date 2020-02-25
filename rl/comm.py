import serial

if __name__ == "__main__":    
    ser = serial.Serial ("/dev/ttyAMA0")    #Open named port 
    ser.baudrate = 9600                     #Set baud rate to 9600
    data = ser.read(10)                     #Read ten characters from serial port to data
    ser.write(data)                         #Send back the received data
    ser.close()