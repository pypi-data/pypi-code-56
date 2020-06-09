'''
The script produces a summary of London Business School's Tech & Media Club's financial position
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Aux:
	'''Auxiliary module to streamline the code'''
	def __init__(self):
		pass

	def preprocess_bal(self, df):
		'''Preprocess club balance sheet'''
		df = df.loc[(df['Accounting Period —>'] == 'Month Ending —>') | (df['Accounting Period —>'] == 'TECH & MEDIA CLUB'), :]
		df = df.iloc[:, 3:]
		df.reset_index(drop = True, inplace = True)
		df = df.T
		df.rename(columns = {0: 'date', 1: 'balance'}, inplace = True)
		df.set_index('date', drop = True, inplace = True)
		df.dropna(axis = 0, inplace = True)
		df['balance'] = df['balance'].str.strip('£\ ()').str.replace(',', '').astype('float64')
		df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
		df.sort_index(inplace = True)
		df.reset_index(inplace = True)
		df.rename(columns = {'index': 'date'}, inplace = True)
		return df

	def preprocess_txn(self, df):
		'''Preprocess transaction sheet'''
		df = df.loc[df['Club Name'] == 'TECH & MEDIA CLUB', ['Amount', 'Debits/Credits', 'Transaction Reference', 'Description', 'Period', 'Transaction Date', 'Finance Code']]
		df['Transaction Date'] = pd.to_datetime(df['Transaction Date']).dt.strftime('%Y-%m-%d')
		df['Finance Code'] = df['Finance Code'].astype('int64')
		df['Amount'] = df['Amount'].str.replace(',', '').astype('float64')
		df.set_index('Transaction Date', inplace = True)
		df.sort_index(inplace = True)
		df.reset_index(inplace = True)
		return df

	def preprocess_fnc(self, df, df_aux):
		'''Preprocess finance code sheet'''
		df = df.loc[df['SA Finance\nFinance Code Directory'] == 'Tech & Media Club', ['Unnamed: 0', 'Unnamed: 2', 'Unnamed: 3']]
		df.rename(columns = {'Unnamed: 0': 'Finance Code', 'Unnamed: 2': 'Event Name', 'Unnamed: 3': 'Start Date'}, inplace = True)
		df['Finance Code'] = df['Finance Code'].astype('int64')
		df.reset_index(drop = True, inplace = True)
		df = pd.merge(df, df_aux[['Finance Code', 'Designated Team']], how = 'left', on = ['Finance Code'])
		return df

	def preprocess_ros(self, df):
		'''Preprocess staff roster sheet'''
		return df

	def merge_data(self, df_bal, df_txn, df_fnc):
		'''Merge processed dataframes into one matrix'''
		self.df_merged = pd.merge(df_txn, df_fnc, how = 'left', on = ['Finance Code'])
		self.df_merged.loc[(self.df_merged['Transaction Date'] < '2020-01-01') & (self.df_merged['Transaction Date'] > '2019-07-31'), 'Term'] = 1
		self.df_merged.loc[(self.df_merged['Transaction Date'] < '2020-04-01') & (self.df_merged['Transaction Date'] > '2019-12-31'), 'Term'] = 2
		self.df_merged.loc[(self.df_merged['Transaction Date'] < '2020-06-30') & (self.df_merged['Transaction Date'] > '2020-03-31'), 'Term'] = 3
		self.df_merged['Term'] = self.df_merged['Term'].astype('Int64')
		self.df_merged['Finance Code'] = self.df_merged['Finance Code'].astype('category')

	def vis_bal(self, df):
		fig, ax = plt.subplots(figsize = (16, 9))
		ax.plot(pd.to_datetime(df['date']), df['balance'])
		ax.set(xlabel = 'Date', ylabel = 'Amount (£)', title = 'TMC Club Balance History')
		ax.grid()
		fig.savefig(self.output_dir_path + '/Club_Balance_History.png', dpi = 300)

	def vis_ros(self, df):
		fig, ax = plt.subplots(figsize = (16, 9))
		ax.bar(df.index, df['Amount'])
		ax.set(xlabel = 'Team', ylabel = 'Amount (£)', title = 'TMC Net Balance Team Breakdown')
		fig.savefig(self.output_dir_path + '/Team_Breakdown.png', dpi = 300)

	def vis_fnc(self, df):
		fig, ax = plt.subplots(figsize = (16, 9))
		ax.bar(df.index, df['Amount'])
		ax.set(xlabel = 'Event Name', ylabel = 'Amount (£)', title = 'TMC Net Balance Finance Code Breakdown')
		ax.tick_params(axis = 'x', labelrotation = 30)
		fig.savefig(self.output_dir_path + '/Finance_Code_Breakdown.png', dpi = 300)

class Analyse(Aux):
	'''Main module'''
	def __init__(self, input_bal_path, input_txn_path, input_fnc_path, input_ros_path, input_ros_fnc_path, output_dir_path):
		super().__init__()
		self.config()
		ros_headers = ['Student ID', 'First Name', 'Last Name', 'Email', 'Team', 'Senority', 'Programme']
		ros_fnc_headers = ['Finance Code', 'Event Name', 'Designated Team']
		self.input_txn_path, self.input_bal_path, self.input_fnc_path, self.input_ros_path, self.input_ros_fnc_path, self.output_dir_path = input_txn_path, input_bal_path, input_fnc_path, input_ros_path, input_ros_fnc_path, output_dir_path
		self.df_bal, self.df_txn, self.df_fnc, self.df_ros, self.df_ros_fnc = pd.read_csv(self.input_bal_path), pd.read_csv(self.input_txn_path), pd.read_csv(input_fnc_path), pd.read_csv(self.input_ros_path, names = ros_headers), pd.read_csv(self.input_ros_fnc_path, names = ros_fnc_headers)

	def config(self):
		from pandas.plotting import register_matplotlib_converters
		register_matplotlib_converters()
			
	def preprocess(self):
		self.df_bal = self.preprocess_bal(self.df_bal)
		self.df_txn = self.preprocess_txn(self.df_txn)
		self.df_fnc = self.preprocess_fnc(self.df_fnc, self.df_ros_fnc)
		self.df_ros = self.preprocess_ros(self.df_ros)
		self.merge_data(self.df_bal, self.df_txn, self.df_fnc)

	def vis(self):
		'''Create visualisations based on preprocessed data'''
		self.vis_bal(self.df_bal)
		self.vis_ros(self.df_merged.groupby(['Designated Team']).agg({'Amount': 'sum'}))
		self.vis_fnc(self.df_merged.groupby(['Event Name']).agg({'Amount': 'sum'}))

	def export(self):
		'''Export constructed dataframes'''
		with pd.ExcelWriter(self.output_dir_path + '/tmc_finance_summary.xlsx') as writer:
			self.df_bal.to_excel(writer, sheet_name = 'Balance History', index = False)
			self.df_merged.groupby(['Designated Team']).agg({'Amount': 'sum'}).to_excel(writer, sheet_name = 'Team Breakdown')
			self.df_merged.groupby(['Term']).agg({'Amount': 'sum'}).to_excel(writer, sheet_name = 'Term Breakdown')
			self.df_merged.groupby(['Finance Code', 'Designated Team', 'Event Name']).agg({'Amount': 'sum'}).to_excel(writer, sheet_name = 'Code Ledger')
			self.df_merged.groupby(['Finance Code', 'Designated Team', 'Event Name', 'Description']).agg({'Amount': 'sum'}).to_excel(writer, sheet_name = 'Code Journal')
			self.df_merged.to_excel(writer, sheet_name = 'General Journal', index = False)

	def exec(self):
		self.preprocess()
		self.vis()
		#print(self.df_merged)
		#print(self.df_merged.groupby(['Finance Code', 'Designated Team', 'Event Name', 'Description']).agg({'Amount': 'sum'}))
		#print(self.df_merged.groupby(['Finance Code', 'Designated Team', 'Event Name']).agg({'Amount': 'sum'}))
		#print(self.df_merged.groupby(['Designated Team']).agg({'Amount': 'sum'}))
		#print(self.df_merged.groupby(['Term']).agg({'Amount': 'sum'}))
		self.export()
