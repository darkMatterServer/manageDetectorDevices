import time
import serial
import os, datetime
from influxdb import InfluxDBClient

##PROGRAM RUNS CLIENT SIDE CODE TO COMMUNICATE WITH ARDUINO // UPLOAD TO SERVER---

#Function which sends measurements from Arduino to server-
def send_to_influxdb(measurement, location, timestamp, pressure, setpoint_pressure, pid_output, mfc_output):
	payload = [
	{"measurement": measurement,
	"tags": {
		"location": location
	},
	"time": timestamp,
	"fields": {
		"pressure": pressure,
		"setpoint pressure": setpoint_pressure,
		"PID_output": pid_output,
		"MFC output": mfc_output
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

ser = serial.Serial('/dev/ttyACM1', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
print(ser)
print("Serial Connection Success")


while True:
	#GOAL: read serial from arduino to pi - upload data to server--

	#initiate serial read. note commnd, dmesg | grep tty used to find port
	
	data = str(ser.read(250))
	print(data)

	#find position of output voltage
	output_voltage_loc = int(data.find("Output Voltage: "))

	output_voltage = (data[output_voltage_loc + 20: output_voltage_loc + 24])

	#find position of mfc output voltage
	mfc_output_voltage_loc = int(data.find("MFC Output Voltage: "))

	mfc_output_voltage = (data[mfc_output_voltage_loc + 24: mfc_output_voltage_loc + 28])

	#find position of setpoint pressure
	setpoint_loc = int(data.find("Setpoint Pressure: "))

	setpoint = (data[setpoint_loc + 23: setpoint_loc + 28])

	#find position of pressure

	pressure = (data[setpoint_loc + 46: setpoint_loc + 50])

	try:
		float(pressure)
		print("Success")
	except ValueError:
		pressure = (data[setpoint_loc + 46: setpoint_loc + 51])

	payload = send_to_influxdb('Nitrogen PID Controller','Williams College',datetime.datetime.utcnow(), float(pressure), float(setpoint), float(output_voltage), float(mfc_output_voltage))

	print("Executed Payload")

	client.write_points(payload)
	
	time.sleep(5)
	

