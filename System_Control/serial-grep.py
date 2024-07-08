import time
import serial
import os, datetime
from influxdb import InfluxDBClient

##PROGRAM RUNS CLIENT SIDE CODE TO COMMUNICATE WITH ARDUINO // UPLOAD TO SERVER---

#Function which sends measurements from Arduino to server-
def send_to_influxdb(measurement, location, timestamp, temperature, humidity):
	payload = [
	{"measurement": measurement,
	"tags": {
		"location": location
	},
	"time": timestamp,
	"fields": {
		"temperature": temperature,
		"humidity": humidity,
	},	
	}
	]
	return payload


#Setting up influxdb data <-> for specific database

host = '137.165.107.243'
port = '8086'
	
username='admin'
password='password'
db='darkmatter1'

#setting up client

client = InfluxDBClient(host, port, username, password, db)
print(client)
print("Client Setup Success")

while True:
	#GOAL: read serial from arduino to pi - upload data to server--

	#initiate serial read. note commnd, dmesg | grep tty used to find port
	ser = serial.Serial('/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
	print(ser)
	print("Serial Connection Success")

	data = str(ser.read(15))

	temploc = int(data.find('.'))

	#variables temp & humidity

	temp = float(data[temploc - 2: temploc + 3])
	humidity = float(data[temploc + 4: temploc + 9])

	print("Found Temp (C):" + str(temp))
	print("Found Humidity (C):" + str(humidity))
	
	payload = send_to_influxdb('Lab Sensor Data','Williams College',datetime.datetime.utcnow(), temp, humidity)

	print("Executed Payload")

	client.write_points(payload)
	
	time.sleep(5)
	

