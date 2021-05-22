#!/home/simple/anaconda3/envs/StriveSchool/bin/python 


from socket import socket, AF_INET, SOCK_STREAM
import pickle
import pandas as pd
from collections import Counter
from datetime import datetime
import numpy as np
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import os
import glob
import warnings
import chime

warnings.filterwarnings("ignore", category=UserWarning)

print("I am into the program")
def time_series(last_preds):
	dict_freq = Counter(last_preds)
	max_key = max(dict_freq, key=lambda k: dict_freq[k])
	return max_key

class Kalories:
	def __init__(self, status='Still'):
		self.calories_burnt = 0.4861
		self.status = status

	def get_status(self, preds_list):
		self.status = time_series(preds_list[-3:])



calories = 0
file_name = 'model_1.sav'
cleanup_target = {1: "Car", 2: "Still", 3: "Train", 4: "Bus", 5: "Walking"}
pred_list = []

loaded_model = pickle.load(open(file_name, 'rb'))

colomuns = ['time', 'activityrecognition#1', 'android.sensor.accelerometer#mean', 'android.sensor.accelerometer#min', 'android.sensor.accelerometer#max', 'android.sensor.accelerometer#std', 'android.sensor.game_rotation_vector#mean', 'android.sensor.game_rotation_vector#min', 'android.sensor.game_rotation_vector#max', 'android.sensor.game_rotation_vector#std', 'android.sensor.gravity#mean', 'android.sensor.gravity#min', 'android.sensor.gravity#max', 'android.sensor.gravity#std', 'android.sensor.gyroscope#mean', 'android.sensor.gyroscope#min', 'android.sensor.gyroscope#max', 'android.sensor.gyroscope#std', 'android.sensor.gyroscope_uncalibrated#mean', 'android.sensor.gyroscope_uncalibrated#min', 'android.sensor.gyroscope_uncalibrated#max', 'android.sensor.gyroscope_uncalibrated#std', 'android.sensor.light#mean', 'android.sensor.light#min', 'android.sensor.light#max', 'android.sensor.light#std', 'android.sensor.linear_acceleration#mean', 'android.sensor.linear_acceleration#min', 'android.sensor.linear_acceleration#max', 'android.sensor.linear_acceleration#std', 'android.sensor.magnetic_field#mean', 'android.sensor.magnetic_field#min', 'android.sensor.magnetic_field#max', 'android.sensor.magnetic_field#std', 'android.sensor.magnetic_field_uncalibrated#mean', 'android.sensor.magnetic_field_uncalibrated#min', 'android.sensor.magnetic_field_uncalibrated#max', 'android.sensor.magnetic_field_uncalibrated#std', 'android.sensor.orientation#mean', 'android.sensor.orientation#min', 'android.sensor.orientation#max', 'android.sensor.orientation#std', 'android.sensor.pressure#mean', 'android.sensor.pressure#min', 'android.sensor.pressure#max', 'android.sensor.pressure#std', 'android.sensor.proximity#mean', 'android.sensor.proximity#min', 'android.sensor.proximity#max', 'android.sensor.proximity#std', 'android.sensor.rotation_vector#mean', 'android.sensor.rotation_vector#min', 'android.sensor.rotation_vector#max', 'android.sensor.rotation_vector#std', 'android.sensor.step_counter#mean', 'android.sensor.step_counter#min', 'android.sensor.step_counter#max', 'android.sensor.step_counter#std', 'sound#mean', 'sound#min', 'sound#max', 'sound#std', 'speed#mean', 'speed#min', 'speed#max', 'speed#std']
#print(len(colomuns))

HEADERSIZE = 10
print("readched checkpoint 1")
s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 5555))  #socket.gethostname()
s.listen(5)

#while True:
full_msg = b''
row_df = pd.DataFrame(columns=colomuns, index=None)
connection = None
connection, address = s.accept()
print("Connected from", address)
		


sg.theme('Dark Blue 3')      # Add some color to the window


layout = [[sg.Text('Welcome to Newton Fitness',font=('Arial', 10, 'bold')), sg.VSeperator(),sg.Image(r'doctor.png')],
		[sg.Text('I am'), sg.Text(size=(20,1), key='-OUTPUT-')],                  #,font=('Arial', 20, 'bold')
		[sg.Text('colories_burn'), sg.Text(size=(20,1), key='colories_burn')],
		[sg.Text('minutes'), sg.Text(size=(20,1), key='sec_info')],
		[sg.Text('KMs I walked'), sg.Text(size=(20,1), key='dist_info')],
		[sg.Text(size=(8, 2), font=('Helvetica', 20), justification='center', key='text')],
		[sg.Exit()]]      
window = sg.Window('Newton Fitness Interface', layout,size=(600, 575), icon='logo.png')



msg = "No message Received Yet"
new_msg = True

print("readched checkpoint 2")
while True:                             # The Event Loop
	try:
		
		event, values = window.read(timeout=10) 
		#print(event, values)       
		if event == sg.WIN_CLOSED or event == 'Exit':
			break
		msg = connection.recv(16)
		if new_msg:
			#print(f'new message legnth:{msg[:HEADERSIZE]}')
			msg_len = int(msg[:HEADERSIZE])
			new_msg = False
		full_msg += msg
		#print("readched checkpoint 3")
		#print("full_msg")
		print("lenfullmsg",len(full_msg))
		print("Headersize",HEADERSIZE)
		print("msg_len",msg_len)
		if len(full_msg) - HEADERSIZE == msg_len:
			print('Full msg recvd')
			row_df = pickle.loads(full_msg[HEADERSIZE:])
			row_df = row_df.values.reshape(1, 66)
			#print(row_df.shape)
			pred = loaded_model.predict(row_df)
			#print(cleanup_target[pred[0]])
			pred_list.append(cleanup_target[pred[0]])
			#print(pred_list)

			new_msg = True
			full_msg = b''
			row_df = pd.DataFrame()
			if len(pred_list) > 3:
				chime.success()
				print(pred_list[-3:])
				#print(time_series(pred_list[-3:]))
				user_1 = Kalories()
				user_1.get_status(pred_list)
				if user_1.status == 'Walking':
					calories += user_1.calories_burnt
				print(user_1.status, round(calories, 3))
				window['-OUTPUT-'].update(user_1.status)
				window['colories_burn'].update(round(calories, 3))
				window['sec_info'].update(round(((calories/user_1.calories_burnt)*5)/60,0))
				window['dist_info'].update(round(((calories/user_1.calories_burnt)*10)/6000,2))
				print(f"You've been walking for {round(((calories/user_1.calories_burnt)*5)/60,0)} minutes")
				print(f"You've walked {round(((calories/user_1.calories_burnt)*5*2)/6000,2)} KM")
				print('-----***-----')
				#window['text'].update('{:02d}'.format(round(((calories/user_1.calories_burnt)*5*2)/6000,2)))
	except KeyboardInterrupt:
		if connection:
			connection.close()
			print("connection closes")
		window.close()
		print("window closes")
		break
		
		
		
s.shutdown
s.close()
window.close()

