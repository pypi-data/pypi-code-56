#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, getopt

__title__ = "gitlab-management"
__version__ = "0.1.2"
__doc__ = "https://gitlab.com/nofusscomputing/projects/python-gitlab-management"


class GitlabManagement:
  """
  No Fuss Computing's Gitlab Config Management python module. (version: """ + __version__ + """)

  """

 
  import gitlab as GitLabAPIWrapper
  import gitlab.v4.objects
  import traceback
  import logging
  from enum import Enum

  
  GitlabSession:GitLabAPIWrapper.Gitlab = None
  ModuleVersion = __version__

  DesiredOutputLevel:int = None

  Config:dict = None

  class OutputSeverity(Enum):
    
    Emergency:int = 0
    Alert:int = 1
    Critical:int = 2
    Error:int	= 3
    Warnin:int = 4
    Notice:int = 5
    Informational:int = 6
    Debug:int = 7


  def __init__(self, GitLab_URL:str, GitLab_PrivateToken:str):

    self.DesiredOutputLevel = self.OutputSeverity.Informational

    if self.GitlabLoginAuthenticate(GitLab_URL, GitLab_PrivateToken):
      
      if not self.GetConfig():

        self.Output(self.OutputSeverity.Critical, "Couldn't load config yml")

      else:

        self.Output(self.OutputSeverity.Notice, 'config loaded')

    else:
      
      self.Output(self.OutputSeverity.Critical, 'could not logon to ' + GitLab_URL)


  def GitlabLoginAuthenticate(self, URL:str, PrivateToken:str) -> bool:
    """
    Establish the Gitlab instance to connect to and authenticate.


    Parameters
    ----------
    URL : str
      The url of the gitlab instance to connect to.

    PrivateToken : str
      The private token of the user that will be used to authenticate against the gitlab instance.


    Raises
    ------
    GitLabAPIWrapper.GitlabAuthenticationError
      Returns text output of the failed authentication issue that occured when attemping to authenticate.

    Exception
      Generic catch all exception.


    Returns
    -------
    bool
      Returns `bool` to denote success/failure of the connection and authentication.

    """
    GitlabLoginAuthenticate = False

    try:
      GitlabLogin = self.GitLabAPIWrapper.Gitlab(URL, private_token=PrivateToken)

      GitlabLogin.headers['User-Agent'] = "%s/%s %s" % (__title__, __version__, __doc__)

      GitlabLogin.auth()

      self.GitlabSession = GitlabLogin

      GitlabLoginAuthenticate = True

    except self.GitLabAPIWrapper.GitlabAuthenticationError as e:

      self.Output(self.OutputSeverity.Error, str(e))

    except Exception as e:

      self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

    return GitlabLoginAuthenticate


  def Output(self, OutputLevel:OutputSeverity, OutputMessage:str) -> None:
    """
    Method to output commands to the console.


    Parameters
    ----------
    OutputLevel : GitlabManagement.OutputSeverity(Enum)
      The output leval that the message is categorised as.

    OutputMessage : str
      The text to output.
        

    Raises
    ------
    Exception
      None raised.
      # ToDo: do proper error and exception handling.


    Returns
    -------
    None
      This method does not require output as it is part of the error handling of the application.

    """
    if OutputLevel.value <= self.DesiredOutputLevel.value:
      print(str(OutputLevel.name) + ': ' + OutputMessage)

  
  def GetConfig(self) -> bool:
    """
    Read all of the `config.yml` config file to an object in this class.
        

    Raises
    ------
    yaml.YAMLError
      any error with the yml, will return the text output

    Exception
      Generic catch all exception. if this exception occurs, please log an issue ticket.


    Returns
    -------
    bool
      returns success/failure on reading the config and adding to the class object `self.Config`

    """
    import yaml
    
    GetConfig = False

    with open("config.yml", 'r') as stream:

      try:

        self.Config = dict(yaml.safe_load(stream))
        GetConfig = True

      except yaml.YAMLError as exc:

        self.Output(self.OutputSeverity.Error, exc)

      except Exception as e:
        self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))
        
    return GetConfig


  def CreateGroupLabel(self, Group:gitlab.v4.objects.Group, Name:str, Description:str, Color:str) -> bool:
    """Create a group label within the specified group
    
    Parameters
    ----------
    Group : gitlab.v4.objects.Group
      A gitlab group Object
    
    Name : str
      The name of the label to create

    Description : str
      The description for the label. the description will be prefixed with [Managed Label] to denote this script created the label.

    Color : str
      the colour that the label shoud be in format '#RRGGBB'

    Raises
    ------
    Exception
      No Exception is returned, however the exception will be printed to the console

    Returns
    -------
    bool
      if the string was successfully created, true is returned. false will be returned when there was an exception
    """
    NewLabelString = {}
    CreateGroupLabel = False

    if type(Group) == self.GitLabAPIWrapper.v4.objects.Group:
      
      try:

        if self.GetLabelByName(Group, Name) is None:
          
          NewLabelString['name'] = Name
          NewLabelString['description'] = '[Managed Label] ' + Description
          NewLabelString['color'] = Color

          Group.labels.create(NewLabelString)

          self.Output(self.OutputSeverity.Notice, 'Created label {} in group {}'.format(NewLabelString['name'], Group.attributes['name']))
        
        else:

          self.Output(self.OutputSeverity.Debug, 'Label {} exists in group {}'.format(Name, Group.attributes['name']))

        CreateGroupLabel = True

      except Exception as e:

        self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

    return CreateGroupLabel


  def GetGroupByName(self, GroupName:str) -> gitlab.v4.objects.Group:
    """
    Find and return a group by name.

    Workflow
    1. Find all groups that the current user (the one authorized in this module) has maintainer access to
    2. iterate through all returned groups until the group is found that matches the string.

    Parameters
    ----------
    GroupName : str
      description
        

    Raises
    ------
    Exception
      Generic catch all exception. if this method returns an exception please log an issue.

      # ToDo: add proper error checking and exception checking.


    Returns
    -------
    gitlab.v4.objects.Group
      The Group that matches the search string will be returned.
    
    None
      Returned if nothing found

    """
    GetGroupByName = None

    try:
      Groups = self.GitlabSession.groups.list(min_access_level = self.GitLabAPIWrapper.MAINTAINER_ACCESS)

      for Group in Groups:

        if Group.attributes['name'] == GroupName:
          
          GetGroupByName = Group
    
    except Exception as e:

      self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))
      
    return GetGroupByName


  def GetLabelByName(self, Group:gitlab.v4.objects.Group, LabelName:str) -> gitlab.v4.objects.GroupLabel:
    """
    Finds a label by human readable name and returns a `gitlab.v4.objects.GroupLabel` object.

    Workflow:
    1. iterate through each label in the group until the `LabelName` matches.
    2. return the label as a `gitlab.v4.objects.GroupLabel`


    Parameters
    ----------
    Group : gitlab.v4.objects.Group
      The group that is being searched.
    
    LabelName : str
      The group name to search for.
    
    
    Raises
    ------
    #ToDo: do some error checking
    Nothing is raised in this method.


    Returns
    -------
    gitlab.v4.objects.GroupLabel
      returns thoe object that has a name that matches what was searched for.

    None
      Only returned if no group is found.

    """
    GetLabelByName = None

    if type(Group) is self.GitLabAPIWrapper.v4.objects.Group:

      Labels = Group.labels.list()

      for Label in Group.labels.list():

        if Label.attributes['name'] == LabelName:

          GetLabelByName = Label

    return GetLabelByName 


  def ProcessConfigLabels(self, ConfigGroups:list) -> bool:
    """
    Process the provided configuration labels.


    Parameters
    ----------
    ConfigGroups : list
      The labels array from the config.yml file  

      The array that is passed to the function is processed as follows.

      1. iterates through list of labels
      2. finds the group id that the label is for 
      3. confirms that label attributes are in the config file Group, Name, Description and color.
      4. creates the label in each group that the label is intended for. `CreateGroupLabel()` does the check to see if it exists before creating it.
    

    Raises
    ------
    Exception
      currently is a catch all exception. if this function returns an exception, an issue needs to be raised.


    Returns
    -------
    bool
      returns bool denoting success/failure for the processing of the labels provided.
    """
    ProcessConfigGroups = False

    try:

      self.Output(self.OutputSeverity.Notice, 'Processing Config: labels')

      for Label in ConfigGroups:

        if 'Group' in Label and 'Name' in Label and 'Description' in Label and 'Color' in Label:

          
          if type(Label['Group']) is list:

            for Group in Label['Group']:

              Group = self.GetGroupByName(Group)

              self.CreateGroupLabel(Group, Label['Name'], Label['Description'], Label['Color'])

          else:

            self.CreateGroupLabel(self.GetGroupByName(Label['Group']), Label['Name'], Label['Description'], Label['Color'])
            

        else:
          self.Output(self.OutputSeverity.Error, 'missing the Group for the label')

      ProcessConfigGroups = True

    except Exception as e:
      self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

    return ProcessConfigGroups
