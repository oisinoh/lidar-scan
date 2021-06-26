'''
Interface with scanner and store data
'''

import serial,time
import argparse

#setup filename argument parser
parser = argparse.ArgumentParser()                                               

parser.add_argument("--port", "-p", type=str, required=True)
parser.add_argument("--output", "-o", type=str, required=True)
args = parser.parse_args()

#create class for serial connection
class Conn():
    def __init__(self,port):
        #open new serial port connection
        self.ser = serial.Serial(port)
        self.ser.baudrate = 115200
        print("opened |" + str(self.ser.name) + "|")
    
    def close(self):
        self.ser.close()

scanner = Conn(args.port)

file = open(args.output,'w')
inp = ""
#send start scanning message
scanner.ser.write(b"s")
#read each message
while True:
    inp = scanner.ser.readline() #get message
    formout = inp.decode("utf-8")[:-2] #trim \r\n
    file.write(formout + "\n") #write to file
    print(formout) 
    #if end message recieved
    if formout == "end":
        break #end scan

#close scanner serial connection
scanner.close()
#close file
file.close()