#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, re-authenticate by deleting the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

ROOT_COL_INDEX = ord('A')

class Handler(object):
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """

  def __init__(self, **kwargs):
    self.__ref = {}
    self.__presets = {}
    self.initialize(**kwargs)
    pass

  def initialize(self, **kwargs):
    for field_name in ['spreadsheet_id', 'credentials_file', 'token_file']:
      if type(kwargs[field_name]) == str:
        self.__ref[field_name] = kwargs[field_name]
    pass

  def authorize(self):
    credentials_file = self.__ref['credentials_file']
    token_file = self.__ref['token_file']
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
      with open(token_file, 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)
        pass
      # Save the credentials for the next run
      with open(token_file, 'wb') as token:
        pickle.dump(creds, token)
    return creds

  def view_token(self):
    creds = self.authorize()
    return {
      'refresh_token': creds.refresh_token,
      'client_id': creds.client_id,
      'client_secret': creds.client_secret,
      'id_token': creds.id_token,
      'token_uri': creds.token_uri,
      'expired': creds.expired,
      'scopes': creds.scopes,
      'valid': creds.valid,
    }

  def query(self, sheet_name, cell_range, field_mappings, projection, skip, limit):
    begin_col = cell_range['begin_col']
    begin_col_index = lookup_number_of_colname(begin_col)
    begin_row = cell_range['begin_row']

    end_col = cell_range['end_col']
    end_col_index = lookup_number_of_colname(end_col)
    end_row = cell_range['end_row']

    rangeSpec = sheet_name + '!' + begin_col + str(begin_row) + ':' + end_col
    if end_row is not None:
      rangeSpec = rangeSpec + str(end_row)

    # create the mappings from the field_mappings dictionary
    colnames = []
    colalias = []
    for number in range(begin_col_index, end_col_index + 1):
      colname = lookup_colname_by_number(number)
      colnames.append(colname)
      colalias.append(loopup_fieldname_from_mappings(colname, field_mappings))

    # determine the projection is available or not
    projection_available = (projection is not None) and (len(projection) > 0)

    spreadsheetId = self.__ref['spreadsheet_id']

    # create the service object
    service = build('sheets', 'v4', credentials=self.authorize())

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = spreadsheetId, range = rangeSpec).execute()

    values = result.get('values', [])

    datalist = []
    if values is not None:
      for row in values:
        record = dict()
        for ind in range(end_col_index - begin_col_index + 1):
          fieldname = colalias[ind]
          if projection_available and (fieldname in projection):
            record[fieldname] = row[ind]
        datalist.append(record)

    return dict(data=datalist)

def lookup_number_of_colname(col_name):
  if type(col_name) != str:
    raise TypeError("The name of a column must be a string")

  len_col_name = len(col_name)
  if len_col_name == 1:
    return ord(col_name.upper()) - ROOT_COL_INDEX

  return -1


def lookup_colname_by_number(col_index):
  if col_index < 0:
    raise TypeError("The number of a column must be not negative")

  if col_index >= 26:
    raise TypeError("The number exceeds the maximum columns")

  return chr(ROOT_COL_INDEX + col_index)

def loopup_fieldname_from_mappings(colname, mappings=dict()):
  if colname in mappings:
    return mappings[colname]
  return colname
