# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:34:16 2019

@author: yuanq
"""

import win32com.client
import re
from bs4 import BeautifulSoup as bs

from modUtils3 import get_basic_logger, file_exists
from modGlobal3 import LOG_PRINT_LEVEL

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL)

DIC_ACTION_KEYWORDS = {'EXCEL_RUN_MACRO' : ['FILE_PATH', 'MACRO_NAME', 'PASSWORD', 'UPDATE_LINKS'],
                       'EMAIL_FLAG' : ['COLOUR'],
                       'EMAIL_MOVE' : ['OUTLOOK_FOLDER_NAME'], 
                       'EMAIL_SAVE' : ['FOLDER_PATH']}


class Rules(object):
    def __init__(self, str_rules_file_path):
        self.file_path = str_rules_file_path
        self.__dic_conditions_rules = dict()
        self.__lst_rules = []
        
        with open(self.file_path, 'r') as f:
            str_rules = f.read()            
        
        str_rules = str_rules[str_rules.find('#'):]
        lst_rules = str_rules.split('#')
        for rule in lst_rules:            
            lst_details = rule.split('\n')
            lst_details = [detail.strip() for detail in lst_details if detail.strip()!='']
            if lst_details:
                try:
                    int_num = int(lst_details[0])                    
                except ValueError:
                    continue            
                obj_rule = Rule(int_num)
                for detail in lst_details[1:]:                 
                    __ = detail[0].upper()
                    if __ != 'C' and __!= 'A':
                        logger.debug('please check rule #{rule_num} - only "C|" \
                                     and "A|" are accepted values!'.format(rule_num = int_num))
                    else:
                        lst_key_val = detail[2:].split(':')
                        if len(lst_key_val) == 2:
                            if __ == 'C':
                                processed_conditions = obj_rule.add_condition(lst_key_val[0],lst_key_val[1])
                                if not lst_key_val[0] in self.__dic_conditions_rules:
                                    self.__dic_conditions_rules[lst_key_val[0]] = dict()
                                
                                
                                for cond in processed_conditions:
                                    if cond in self.__dic_conditions_rules[lst_key_val[0]]:
                                        self.__dic_conditions_rules[lst_key_val[0]][cond].append(int_num)
                                    else:                                            
                                        self.__dic_conditions_rules[lst_key_val[0]][cond] = [int_num]
                                
                            else:
                                obj_rule.add_action(lst_key_val[0],lst_key_val[1])
                        else:
                            logger.debug('please check rule #{rule_num} - only \
                                         one key:value pair allowed for each \
                                         condition/action!'. format(rule_num = int_num))
     
                self.__lst_rules.append(obj_rule)
            
            
            
            
    def get_rules(self):
        return self.__lst_rules
                      
    def process_email(self, email):
        pass
    
    def get_conditions_rules(self):
        return self.__dic_conditions_rules
            
            
            

class Rule(object):
    def __init__(self, int_rule_num):
        self.rule_num = int_rule_num
        self.num_of_conditions = 0
        self.num_of_actions = 0
        self.__dic_conditions = dict()
        self.__lst_actions = []
        
    def check(self):
        pass
    
    def get_conditions(self):
        return self.__dic_conditions
    
    def get_actions(self):
        return self.__lst_actions
    
    def add_action(self, key, value):
        key_new = key.strip().upper()
        self.num_of_actions += 1
        if key_new in DIC_ACTION_KEYWORDS:            
            lst_supported_kwargs = DIC_ACTION_KEYWORDS[key_new]
            self.num_of_actions += 1
        else:            
            logger.error('{action_name} action not supported!'.format(action_name=key))
            return False            
            
        dic_kwargs = {k:None for k in lst_supported_kwargs}
        
        lst_args = value.split(';')
        lst_args = [arg.strip() for arg in lst_args if arg.strip()!='']
        
        if len(lst_args) <= len(dic_kwargs):
            pos = 0
            for arg in lst_args:
                if '=' in arg:
                    key_val = arg.split('=')
                    if key_val[0].strip().upper() in dic_kwargs:
                        dic_kwargs[key_val[0].strip().upper()] = key_val[1].strip()
                    else:
                        logger.error('please check rule #{rule_num} - keyword argument \
                                     {kwarg} provided for {action_name} action does not\
                                      exist!'.format(rule_num=self.rule_num,
                                     action_name=key, kwarg=key_val[0].strip()))                       
                else:
                    dic_kwargs[lst_supported_kwargs[pos]] = arg
                pos += 1
            self.__lst_actions.append((key_new, dic_kwargs))
        else:
            logger.error('please check rule #{rule_num} - too many arguments \
                provided for {action_name} action!'.format(rule_num=self.rule_num,
                action_name=key))  
    
    def add_condition(self, key, value):
        key_new = key.strip().upper()
        self.num_of_conditions += 1
        if key_new == 'TO':
            if isinstance(value, list):
                lst_emails = [email.strip().upper() for email in [val.split(';') for val in value] if email.strip()!='']
                self.__dic_conditions[key_new] = lst_emails
            elif isinstance(value, str):
                if ';' in value:
                    lst_emails = value.split(';')
                    lst_emails = [val.strip().upper() for val in lst_emails if val.strip()!='']
                    self.__dic_conditions[key_new] = lst_emails
                else:
                    self.__dic_conditions[key_new] = [value.strip().upper()]
            else:
                logger.debug('please check rule #{rule_num} - value provided for `TO` \
                             condition is invalid!'.format(rule_num=self.rule_num))
        elif key_new == 'FROM':
            if isinstance(value, list):
                if len(value)>1:
                    logger.debug('please check rule #{rule_num} - `FROM` condition \
                             can only contain one email address!'.format(rule_num=self.rule_num)) 
                 
                lst_emails = [email.strip().upper() for email in [val.split(';') for val in value] if email.strip()!='']
                if len(lst_emails) == 1:
                    self.__dic_conditions[key_new] = lst_emails                    
                else:
                    logger.debug('please check rule #{rule_num} - `FROM` condition \
                             can only contain one email address!'.format(rule_num=self.rule_num))
            elif isinstance(value, str):
                if ';' in value:
                    lst_emails = value.split(';')
                    lst_emails = [val.strip().upper() for val in lst_emails if val.strip()!='']
                    if len(lst_emails) == 1:
                        self.__dic_conditions[key_new] = lst_emails                    
                    else:
                        logger.debug('please check rule #{rule_num} - `FROM` condition \
                                can only contain one email address!'.format(rule_num=self.rule_num))                    
                else:
                    self.__dic_conditions[key_new] = [value.strip().upper()]
            else:
                logger.debug('please check rule #{rule_num} - value provided for `FROM` \
                             condition is invalid!'.format(rule_num=self.rule_num)) 
        elif key_new == 'CC':
            if isinstance(value, list):
                lst_emails = [email.strip().upper() for email in [val.split(';') for val in value] if email.strip()!='']
                self.__dic_conditions[key_new] = lst_emails
            elif isinstance(value, str):
                if ';' in value:
                    lst_emails = value.split(';')
                    lst_emails = [val.strip().upper() for val in lst_emails if val.strip()!='']
                    self.__dic_conditions[key_new] = lst_emails
                else:
                    self.__dic_conditions[key_new] = [value.strip().upper()]
            else:
                logger.debug('please check rule #{rule_num} - value provided for `CC` \
                             condition is invalid!'.format(rule_num=self.rule_num))
          
            
        elif key_new == 'SUBJECT':
            if isinstance(value, list):
                lst_words = [word.strip() for word in [w.split(';') for w in value] if word.strip()!='']
                self.__dic_conditions[key_new] = lst_words
            elif isinstance(value, str):
                if ';' in value:
                    lst_words = value.split(';')
                    lst_words = [val.strip() for val in lst_words if val.strip()!='']
                    self.__dic_conditions[key_new] = lst_words
                else:
                    self.__dic_conditions[key_new] = [value.strip()]
            else:
                logger.debug('please check rule #{rule_num} - value provided for `SUBJECT` \
                             condition is invalid!'.format(rule_num=self.rule_num))
                
        else:
            self.num_of_conditions -= 1
            logger.error('{condition_name} condition not supported!'.format(condition_name=key))
        
        return self.__dic_conditions[key_new]    

def send_email(str_to, 
               str_cc, 
               str_bcc, 
               str_subject, 
               str_body, 
               bln_send = False, 
               dte_delay = None, 
               str_mailbox_to_use = None, 
               lst_attachment_paths = None):
    """
    Sends email through Outlook application via win32com.
    
    Parameters
    ----------
    str_to : string
        string containing email addresses of intended recipients separated by ';'
    str_cc : string
        string containing email addresses of cc recipients separated by ';'
    str_bcc : string 
        string containing email addresses of bcc recipients separated by ';'
    str_subject : string 
        string representing email subject
    str_body : string
        email content - if '<HTML>' tag is present, content will be applied to 
        email's `HTMLBody` property instead of email's `Body` property
    bln_send : boolean
        True to automatically send out email (default: False)
    dte_delay : datetime
        (delayed) datetime to send out email
    str_mailbox_to_use : string
        email address of mailbox to use
    lst_attachment_paths : list
        list of full file paths of files to attach to email
    
    Returns
    -------
    boolean
        True if email is successfully sent
    """
    outlook = win32com.client.DispatchEx('Outlook.Application')
    if str_mailbox_to_use:
        namespace = outlook.GetNamespace('MAPI')
        recipient = namespace.CreateRecipient(str_mailbox_to_use)
        recipient.Resolve()
        try:
            folder = namespace.Folders[str_mailbox_to_use].Folders["Inbox"]
        except:
            logger.error('Mailbox not found.')
            return False
        if not folder:
            logger.error('Inbox not found in specified mailbox.')
            return False
        mail_item = folder.Items.Add()
    else:
        mail_item = outlook.CreateItem(0)
    mail_item.To = str_to
    mail_item.CC = str_cc
    mail_item.BCC = str_bcc
    mail_item.Subject = str_subject
    if '<html>' in str_body.lower():
        mail_item.HTMLBody = str_body
    else:
        mail_item.Body = str_body
    if lst_attachment_paths:
        for attachment in lst_attachment_paths:
            if file_exists(attachment):
                mail_item.Attachments.Add(attachment)
            else:
                logger.info(str(attachment) + ' does not exist.')
    if dte_delay:
        mail_item.DeferredDeliveryTime = dte_delay
    if bln_send:
        mail_item.Send()
    else:
        mail_item.Display()
    return True

def email_recipient_names_to_addresses(str_email_names, mail_item):
    """
    Convert email recipient names to mail addresses.
    
    Parameters
    ----------
    str_email_names : string
        string containing names of recipients in `mail_item` object
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    string
        mail addresses of recipients in `mail_item` object
    """
    dic_email_addresses = dict()
    str_output = ''
    dic_email_addresses = get_all_recipients_SMTP_mail_addresses(mail_item)
    temp = str_email_names.split('; ')
    for name in temp:
        if name.strip() != '':
            str_output = str_output + str(dic_email_addresses[name]) + '; '        
    return str_output.strip()

def get_sender_SMTP_mail_address(mail_item):
    """
    Returns sender's SMTP mail address.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    string
        SMTP mail address of sender
    """
    reply = mail_item.Reply()
    recipient = reply.Recipients[1]
    str_address = recipient.PropertyAccessor.GetProperty(r'http://schemas.microsoft.com/mapi/proptag/0x39FE001E').strip()                
    return str_address

def get_all_recipients_SMTP_mail_addresses(mail_item):
    """
    Returns dictionary containing SMTP mail addresses of all recipients in 
    `mail_item` object.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    dictionary
        contains {recipient_name : SMTP_mail_address} key-value pairs of all 
        recipients in `mail_item` object
    """
    dic_outputs = dict()
    for recipient in mail_item.Recipients:
        dic_outputs[recipient.Name] = recipient.PropertyAccessor.GetProperty(r'http://schemas.microsoft.com/mapi/proptag/0x39FE001E').strip()
    return dic_outputs

def get_real_attachment_count(mail_item):
    """
    Count the number of real attachments in the `mail_item` object.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    string
        email address of mailbox
    """
    i = 0
    for attachment in mail_item.Attachments:
        str_cid = attachment.PropertyAccessor.GetProperty(r'http://schemas.microsoft.com/mapi/proptag/0x3712001E')
        if str_cid == '':
            i = i + 1
    return i

def get_mailbox_from_mailitem(mail_item):
    """
    Return mailbox to which `mail_item` belongs to.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    string
        email address of mailbox
    """
    parent = mail_item.Parent
    name = parent.Name
    while not '@' in name:
        parent = parent.Parent
        name = parent.Name
        
    return name

def get_basic_email_details(mail_item):
    """
    Returns a dictionary containing basic properties of an Outlook `mail_item` object.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    dictionary
        containing basic properties/attributes of an Outlook `mail_item` object
        {property_name : property_value}
    """
    dic_basic_email_details = dict()
    dic_basic_email_details['Mailbox'] = get_mailbox_from_mailitem(mail_item)
    dic_basic_email_details['To'] = email_recipient_names_to_addresses(mail_item.To, mail_item)
    dic_basic_email_details['From'] = get_sender_SMTP_mail_address(mail_item)
    dic_basic_email_details['Cc'] = email_recipient_names_to_addresses(mail_item.CC, mail_item)
    dic_basic_email_details['Subject'] = mail_item.Subject
    dic_basic_email_details['ConversationID'] = mail_item.ConversationID
    dic_basic_email_details['ConversationIndex'] = mail_item.ConversationIndex                     
    dic_basic_email_details['ConversationTopic'] = mail_item.ConversationTopic
    dic_basic_email_details['Body'] = re.sub(r'\r\n', ' ', mail_item.Body)
    dic_basic_email_details['HTMLBody'] = mail_item.HTMLBody
    dic_basic_email_details['SentOn'] = mail_item.SentOn
    dic_basic_email_details['ReceivedOn'] = mail_item.ReceivedTime
    dic_basic_email_details['Attachment'] = (get_real_attachment_count(mail_item) > 0)
    return dic_basic_email_details

def html_to_tables(str_HTML):
    """Extracts tables from html body of Outlook email"""
    objHTML = bs(str_HTML, 'lxml')
    objTables = objHTML.findAll('table')
    arrTable = []
    for objTable in objTables:
        arrRow = []
        for objRow in objTable.findAll('tr'):
            arrCol = []
            for objCol in objRow.findAll('td'):
                arrCol.append(objCol.get_text().strip())                
            arrRow.append(arrCol)            
        arrTable.append(arrRow)    
    return arrTable

def table_to_html(lst_table,
                  bln_header = True):
    
    str_html = '<table style="width:100%; border-collapse:collapse;", border=1>'
    first_row = 0
    if bln_header:
        str_html = str_html + '<tr>'
        for i in range(len(lst_table[0])):
            str_html = str_html + '<th>' + str(lst_table[0][i]) + '</th>'
        str_html = str_html + '</tr>'
        first_row = 1
    
    for i in range(first_row, len(lst_table)):
        str_html = str_html + '<tr>'
        for j in range(len(lst_table[i])):
            str_html = str_html + '<td>' + str(lst_table[i][j]) + '</td>'
            
        str_html = str_html + '</tr>'
        
    str_html = str_html + '</table>'
    return str_html