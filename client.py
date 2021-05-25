#!/home/simple/anaconda3/envs/StriveSchool/bin/python 

import socket
import pickle
import time
import pandas as pd
import PySimpleGUI as sg


sg.theme('Dark Blue 3')    # Keep things interesting for your users

layout = [[sg.Text('Allow Server To Read Data')],      
		  [sg.Button('send')]]      
#Allow Server To Read Data
window = sg.Window('Newton Fitness Client', layout,size=(250, 75), icon='logo.png')      


df = pd.read_csv('userdata_3.csv')
# df_input = pd.read_csv('input3.csv')
# no_col = df_input.shape

X = df.copy()
target = X.pop('target')
#user = X3.pop('user')
list_cols = list(X.columns)
print(len(list_cols))
no_rows = X.shape[0]

HEADERSIZE = 10
PORT = 5555#5551#

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), PORT))


while True:                             # The Event Loop
	event, values = window.read() 
	print(event, values)       
	if event == sg.WIN_CLOSED:
		break
	if event == 'send':
		for row in range(no_rows):
			d = X.iloc[row, :]
			print(d)
			msg = pickle.dumps(d)
			msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
			s.send(msg)
			time.sleep(5)
		

window.close()

