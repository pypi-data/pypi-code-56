import os

'''
	Problem: Find out max and avg delay of execution of each function and print it
into a new file.
'''

def file_Read(filename):
	f = open(filename, "r")
	data = f.read()
	return data

def check_for_function_name_match(function_names,linecontents):

	for function_name in function_names:
		if function_name in linecontents :
			print("{} detected".format(function_name))
			return function_name

if __name__=="__main__":
	log_filename="log.txt"
	filedata=file_Read(log_filename)
	filedata=filedata.split("\n")
	
	function_names=["read_data","write_data","toggle_data","send_data","recv_data"]

	read_data_time_list=[]
	write_data_time_list=[]
	toggle_data_time_list=[]
	send_data_time_list=[]
	recv_datav_time_list=[]

	function_dict={"read_data":read_data_time_list, "write_data":write_data_time_list,"toggle_data":toggle_data_time_list,"send_data":send_data_time_list,"recv_data":recv_datav_time_list }
	count=0
	for line in filedata:
	   if line.strip():
		   count+=1
		   print("count",count)
		   print(line)
		   # line=list(map(float, line))
		   linecontents=line.split()
		   function_name_returned=check_for_function_name_match(function_names,linecontents)

		   # function_name=line.split()[5] 
		   time_taken=line.split()[-2] 
		   function_dict[function_name_returned].append(time_taken)
	   else:
	   	   break

	# print("read_data list: ",function_dict["read_data"])
	# print("write_data list: ",function_dict["write_data"])
	# print("toggle_data list: ",function_dict["toggle_data"])
	# print("send_data list: ",function_dict["send_data"])
	# print("recv_data list: ",function_dict["recv_data"])

	outfile= open("function_delay_time.txt", "w")
	for function_name in function_names:
		print("****function name",function_name)
		function_dict[function_name]=list(map(float, function_dict[function_name]))
		avg_delay_time=0
		max_delay_time=max(function_dict[function_name])
		print("max_delay_time",max_delay_time)
		
		# print("sum(function_dict[function_name])",sum(function_dict[function_name]))
		avg_delay_time=sum(function_dict[function_name])/len(function_dict[function_name])
		print("avg_delay_time",avg_delay_time)
		out_string= "{}'s average delay time is {} and max delay time is {} \n".format(function_name,avg_delay_time,max_delay_time)

	
		outfile.write(out_string)
	outfile.close()


		   