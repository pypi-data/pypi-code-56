import datetime as dt

# Error classes
class NotValidObject(Exception):
	"""Error raises when passed object is invalid."""
	pass

class InvalidComparison(Exception):
	"""Error raises when given time given as past is actually future or current time"""
	pass

class Formatter:
	def __init__(self):
		pass
	
	def delta_to_string(self,delta, as_dict=False):
		"""
		Convert a timedelta object to string.
		
		Parameters 
		- delta		A time delta object
		- as_dict	Whether it should return a dictionary or a string. Default False
		
		return		String or dictionary according to as_dict kwarg
		"""
		
		if not isinstance(delta, dt.timedelta):
			raise NotValidObject(f"delta must be a object of 'datetime.timedelta' given '{type(delta).__name__}'")
		
		dur = ""
		days = abs(delta.days)
		seconds = abs(delta.seconds)
			
		year = 0
		month = 0
		day = 0
		hour = 0
		minute = 0
		second = 0
		
		if days == 0 and seconds == 0:
			if as_dict:
				return {'years': year, 'months': month, 'days' : day, 'hours': hour, 'minutes': minute, 'seconds': second}
			dur = "Just now"
			return dur
			
		if days >= 365:
			year = days//365	
			days = days%365
				
			
		if days >=30:
			month = days//30
				
			if month >= 12:
				year += month // 12
					
				month = month % 12
				
			days = days %30
					
		if days >= 0:
			day = days
				
		if seconds >= 3600:
			hour = seconds//3600	
			seconds = seconds%3600
			
		if seconds >= 60:
			minute = seconds//60
				
			seconds = seconds%60
			
		if seconds > 0:
			second = seconds
			
		if as_dict:
			return {'years': year, 'months': month, 'days' : day, 'hours': hour, 'minutes': minute, 'seconds': second}
		dur = f"{f'{year} Years ' if year > 0 else ''}{f'{month} Months ' if month > 0 else ''}{f'{day} Days ' if day > 0 else ''}{f'{hour} Hours ' if hour > 0 else ''}{f'{minute} Minutes ' if minute > 0 else ''}{f'{second} Seconds' if second > 0 else ''}"
		
		dur_list = [item for item in dur.split(" ") if not item == ""]
		
		if len(dur_list) > 2:
		
			first_part = dur_list[:len(dur_list)-2]
			last_part = [item for item in dur_list if item not in first_part]
			
			part1 = " ".join(first_part)
			part2 = " ".join(last_part)
			
			final_output = part1 + " and " + part2
			
			return final_output
		else:
			return dur
	
	def datetime_to_string(self,now, past, as_dict=False):
		"""Past date difference compared to current time
		
		Parameters 
		- now		A datetime.date or datetime.datetime object represents current time
		- past		A datetime.date or datetime.datetime object represents a past date. Giving future date will raise an error.
		- as_dict	Whether it should return a dictionary or a string. Default False
		
		return		String or dictionary according to as_dict kwarg
		"""
		valids = [dt.date, dt.datetime]
		
		if type(now) not in valids or type(past) not in valids:
			raise InvalidComparison("now and past should be either object of 'datetime.date', or 'datetime.datetime'")
		
		if isinstance(now, dt.date):
			now = dt.datetime.combine(now, dt.datetime.min.time())
			
		if isinstance(past, dt.date):
			past = dt.datetime.combine(past, dt.datetime.min.time())
		
		dur = ""
		
		delta = now - past
		
		days = abs(delta.days)
		seconds = abs(delta.seconds)
			
		year = 0
		month = 0
		day = 0
		hour = 0
		minute = 0
		second = 0
		
		if now == past:
			if as_dict:
				return {'years': year, 'months': month, 'days' : day, 'hours': hour, 'minutes': minute, 'seconds': second}
			dur = "Just now"
			return dur
		
		if now < past:
			raise InvalidComparison("past cant be greater then now")
			
		if days >= 365:
			year = days//365	
			days = days%365
				
			
		if days >=30:
			month = days//30
				
			if month >= 12:
				year += month // 12
					
				month = month % 12
				
			days = days %30
					
		if days >= 0:
			day = days
				
		if seconds >= 3600:
			hour = seconds//3600	
			seconds = seconds%3600
			
		if seconds >= 60:
			minute = seconds//60
				
			seconds = seconds%60
			
		if seconds > 0:
			second = seconds
			
		if as_dict:
			return {'years': year, 'months': month, 'days' : day, 'hours': hour, 'minutes': minute, 'seconds': second}
		
		dur = f"{f'{year} Years ' if year > 0 else ''}{f'{month} Months ' if month > 0 else ''}{f'{day} Days ' if day > 0 else ''}{f'{hour} Hours ' if hour > 0 else ''}{f'{minute} Minutes ' if minute > 0 else ''}{f'{second} Seconds' if second > 0 else ''}"
		
		dur_list = [item for item in dur.split(" ") if not item == ""]
		
		if len(dur_list) > 2:
		
			first_part = dur_list[:len(dur_list)-2]
			last_part = [item for item in dur_list if item not in first_part]
			
			part1 = " ".join(first_part)
			part2 = " ".join(last_part)
			
			final_output = part1 + " and " + part2
			
			return final_output
		else:
			return dur
	
	def get_difference(self, datetime1, datetime2, as_dict=False):
		"""Past date difference compared to current time
		
		Parameters 
		- datetime1	A datetime.date or datetime.datetime object
		- datetime2	A datetime.date or datetime.datetime object
		- as_dict	 	Whether it should return a dictionary or a string. Default False
		
		return		String or dictionary according to as_dict kwarg
		"""
		valids = [dt.date, dt.datetime]
		
		if type(datetime1) not in valids or type(datetime2) not in valids:
			raise InvalidComparison("datetime1 and datetime2 should be either object of 'datetime.date', or 'datetime.datetime'")
		
		if isinstance(datetime1, dt.date):
			datetime1 = dt.datetime.combine(datetime1, dt.datetime.min.time())
			
		if isinstance(datetime2, dt.date):
			datetime2 = dt.datetime.combine(datetime2, dt.datetime.min.time())
		
		if datetime1 < datetime2:
			datetime1, datetime2 = datetime2, datetime1
		
		data = self.datetime_to_string(datetime1, datetime2, as_dict)
		return data
		
		
		