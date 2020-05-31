#Create my own library
#Apply pypi.org so we can upload package to that web
#pip install twine
#upload package to pypi.org

class MyOwnLibrary:

  def __init__(self):
    self.name = 'Me'
    self.lastname = 'Myself'
    self.nickname = 'Nick'

  def whoami(self):
    '''
    Function for display name of this class
    '''
    print('My name is: {}'.format(self.name))
    print('My lastname is: {}'.format(self.lastname))
    print('You can call me: {}'.format(self.nickname))

  @property#make function as a property
  def email(self):
    return '{}.{}@email.com'.format(self.name.lower(), self.lastname.lower())

  def localname(self):
    print('ไลบรารี่')
    return 'ไลบรารี่'

  def __str__(self):
    return 'This is a Create own Lib class'

if __name__ == '__main__':
  #Create a new object
  mylib = MyOwnLibrary()
  print(help(mylib.whoami))
  print(mylib.name) #replace the self with parameter
  print(mylib.lastname)
  print(mylib.nickname)

  mylib.whoami()

  print(mylib.email)#if no @property must have ()

  print(mylib)

  my2lib = MyOwnLibrary()
  my2lib.name = 'AA'
  print(my2lib)