''' execute code '''
from Build_Model import (format_dataset, split_train_test, create_random_forest, predict_test_data, 
evaluate_fit, list_top_features, plot_top_features, plot_predicted_actual, plot_tree)
from Test_Model import (main_test_model)
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
import numpy as np
import pydot
import csv
import sys
import argparse

parser = argparse.ArgumentParser() 
parser.add_argument('-nd', action='store', dest='num_devices', nargs='*', type=int, required=True)
parser.add_argument('-nq', action='store', dest='num_questions', nargs='*', type=int, required=True)
args = parser.parse_args()
print(args.num_devices)


# Build or Test

##if input == "Build":
## 	main()
## else:
##	main_test_model
	

	
# Choose file
## Please choose file to build model
'''window = tk.Tk()
label = tk.Label(text="Please choose csv file to build model", fg = 'white', bg = 'purple', width = 30, height = 5)
label.pack()
window.mainloop()'''
#root = tk.Tk()
#root.filename = tk.filedialog.askopenfilename(initialdir="C:\Documents", title="Select File",  filetype=(("csv", "*.csv"),("all files","*.*")))
#filename = root.filename

## Please choose file to test model
'''window = tk.Tk()
label = tk.Label(text="Now, please choose csv file to test the model", fg = 'white', bg = 'purple', width = 40, height = 5)
label.pack()
window.mainloop()'''
#root = tk.Tk()
#root.filename = tk.filedialog.askopenfilename(initialdir="C:\Documents", title="Select File",  filetype=(("csv", "*.csv"),("all files","*.*")))
#filename = root.filename

# Magpi or Qualtrics
# if input == 'Magpi':
	# number of devices
'''window = tk.Tk()
label = tk.Label(text="please enter number of devices in dataset")
entry = tk.Entry()
label.pack()
entry.pack()
num_devices = entry.get()
window.mainloop()'''

'''
def show_entry_close():
	print("Number of devices = %s" % e1.get())
	num_devices = e1.get()
	master.destroy()
	return  e1.get()

	
	
master = tk.Tk()
tk.Label(master,text="Please enter number of devices in dataset")
e1 = tk.Entry(master)
e1.grid(row=0, column=1)
tk.Button(master,text='Enter', command=show_entry_close).grid(row=3,column=0, sticky=tk.W, pady=4)
#num_devices = e1.get()
tk.mainloop()


#print('Number of devices = %s' % e1.get())'''

	# number of questions
'''window = tk.Tk()
label = tk.Label(text="please enter number of questions asked per device")
entry = tk.Entry()
label.pack()
entry.pack()
window.mainloop()'''
	
	#df_new = format_magpi(filename,num_devices,num_questions)
# else:
	# number of participants
	
	#df_new = format_qualtrics(filename, num_participants)

