'''
This Module is One to Make Your Code Shorter.
High API Will Make You Feel You're Ordering And Machine Is Doing!
Also There is Collection of most usefull function and methods from popular modules of python.
(Read Help of Functions)
Official Documention Will Be Added Soon.
'''
'''
Written By RX
Last Update: 06-01-2020
'''
__version__='1.9.0'



#START
import os,shutil,random,time,requests,re,socket,subprocess
import psutil
from typing import Any

__all__=['p','re','rev',
         'read','write',
         'wait','cls',
         'progressbar',
         'cons_int',
         'wait_for',
         'call_later',
        #Tuples:
         'force','erase',
         'insert','replace',
        #Classes
         'rand','system',
         'file','files',
         'style','record'
         ]





#######        8888888888                         888    d8b                                   ####### 
 #####         888                                888    Y8P                                    #####  
  ###          888                                888                                            ###   
   #           8888888 888  888 88888b.   .d8888b 888888 888  .d88b.  88888b.  .d8888b            #    
   #           888     888  888 888 "88b d88P"    888    888 d88""88b 888 "88b 88K                #    
  ###          888     888  888 888  888 888      888    888 888  888 888  888 "Y8888b.          ###   
 #####         888     Y88b 888 888  888 Y88b.    Y88b.  888 Y88..88P 888  888      X88         #####  
#######        888      "Y88888 888  888  "Y8888P  "Y888 888  "Y88P"  888  888  88888P'        ####### 

                                                                 
def p(text='',end='\n'):
    '''
    p is print!
    But because we use it a lot, we\'ve decided to make it one letter.
    Example:
        p('Hello World')
        ==>Hello World
    '''
    print(text,end=end)

def repeat(function,n: int):
    '''
    Repeat function for n times
    for more info see the example below.
    Example:
        re(Func_Name, 3)
        ==> "function Func_Name will launch 3 times."
    '''
    i=1
    while i <= n:
        i+=1
        function() 

def rev(var:Any):
    '''
    This function is for reversing Strings, Lists, Tuples And also Integers.
    Example:
        b= rev('Football')
        print(b)
        ==> llabtooF
    '''
    ret=var
    if type(ret)==int or type(ret)==float:
        ret= str(ret)
        ret= ret[::-1]
        if type(var)==int:
            ret= int(ret)
        else:
            ret=float(ret)
    else:
        ret= ret[::-1]
    return ret

def read(file):
    '''
    This can help you to read your file faster.
    Example:
        read_file('C:\\users\\Jack\\test.txt')
        ==> "Content of 'test.txt' will be shown."
    '''
    op= open(file,mode='r')
    FileR= op.read()
    op.close()
    return FileR
    #print(FileR)
def write(file,text='',mode='replace',start=''):
    if mode=='replace':
        op= open(file,mode='w')
        #if text==None:
        #    text= input('Type what you want.\n\n')
        op.write(text)
        #print('File has been created/changed.')
        op.close()
    elif mode=='continue':
        '''opr= open(file,mode='r')
        FileR= opr.read()
        op= open(file,mode='w')'''
        op=open(file,'a')
        #if text==None:
        #    text= input('Type what you want to add in the end of the file.\n\n')
        #op.write(FileR+'\n'+text)
        #op.write(FileR+text)
        op.write(start+str(text))
        #print('File has been created/changed.')
        op.close() 
    else:   
        print('Error\nmode can only be: 1-replace(default)  2-continue\nNot "{0}"'.format(mode)) 

def wait(seconds):
    '''
    Use this if you want your program wait for a certain time.
    Example:
        wait(3)
        ==> "Nothing happen and there will be no calculation for 3 seconds"
    '''
    import time
    time.sleep(seconds)
#__SQ_= 'powernrxbetfromporto'
def cls():
    '''
    You can use this function if you want to clear the environment.
    '''
    os.system('clear')

def progressbar(total=100,dashes_nom=100,delay=1,dashes_shape='-',complete_shape='█',pre_text='Loading: ',
                left_port='|',right_port='|'):
    '''
    Use this function to make a custom in-app progress bar.
    Example:
        progressbar(Total=100,Dashes_Nom=10,Time=1,Dashes_Shape='-',Complete_Shape='#', Pre_Text='Loading')
        ==>   Loading|####------| 40/100
    '''
    import sys
    def Progressbar(it, prefix="", size=60, file=sys.stdout):
        count = len(it)
        def show(j):
            x = int(size*j/count)
            file.write("%s%s%s%s%s %i/%i\r" % (prefix, right_port, complete_shape*x, dashes_shape*(size-x), left_port, j, count))
            file.flush()        
        show(0)
        for i, item in enumerate(it):
            yield item
            show(i+1)
        file.write("\n")
        file.flush()
    for i in Progressbar(range(total), pre_text, dashes_nom):
        wait(delay)

def cons_int(First_Nom:int, Last_Nom:int):
    '''
    Make string from First_Nom to Last_Nom.
    string('1','12')  ==> '123456789101112
    '''
    if type(First_Nom)==int and type(First_Nom)==type(Last_Nom):
        strin=''
        i=First_Nom
        for i in range(First_Nom,Last_Nom+1):
            strin= strin+str(i)
        return strin
    else:
        TypeError('Both Args Most Have int Type')

def wait_for(button):
    '''
    If You Want to Wait For the User to Press a Key (Keyboard or Mouse) Use This Function.
    '''
    if button.lower() in ('middle','left','right','back','forward'):
        if button.lower()[:1]=='b':
            button='x'
        if button.lower()[:1]=='f':
            button='x2'
        import mouse
        mouse.wait(button)
    else:
        import keyboard
        try:
            keyboard.wait(button)
        except:
            raise ValueError('Incorrect Button Name.')

def call_later(function,*args,delay=0.001):
    '''
    Do You Want to Call Your Function Later Even Between Other Operations?
    call_later() will help you to do that!
    First arg should be your function name,
    After That (*args) you can add any args that you function need,
    And Last arg is delay for calling your function.
    '''
    import keyboard
    keyboard.call_later(function,args,delay)

def convert_bytes(num:int) -> str :
    """
    Convert num to idiomatic byte unit.
    num is the input number (bytes).
    
    >>> convert_bytes(200)
    '200.0 bytes'
    >>> convert_bytes(6000)
    '5.9 KB'
    >>> convert_bytes(80000)
    '78.1 KB'
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

#####################
#    TUPLE FUNCS    #
#####################
def force(tpl,*var):  
    '''
    (TUPLE FUNCTION)
    It returns tpl with adding var(s) to it.
    '''
    return tuple(list(tpl)+[v for v in var])
#force= lambda tpl,*var: tuple(list(tpl)+[v for v in var])

def erase(tpl,*var):
    '''
    (TUPLE FUNCTION)
    It returns tpl with removing var(s) to it.
    '''
    #lstv= [v for v in var if v in tpl]
    lstt= list(tpl)
    for th in [v for v in var if v in tpl]:
        lstt.remove(th)
    return tuple(lstt)

def replace(tpl,ind,var):
    '''
    (TUPLE FUNCTION)
    Replace tpl[ind] with var
    '''
    tpl=list(tpl)
    if type(ind) == str:
        ind= tpl.index(ind)
    tpl[ind]=var
    return tuple(tpl)

def insert(tpl,ind,var):
    '''
    (TUPLE FUNCTION)
    Exactly like tpl[ind]=var for lists.
    '''
    tpl=list(tpl)
    if type(ind) == str:
        ind= tpl.index(ind)
    tpl.insert(ind,var)
    return tuple(tpl)    



#######         .d8888b.   888  888                                                         #######
 #####         d88P  Y88b  888  888                                                          ##### 
  ###          888    888  888  888                                                           ###  
   #           888         888  888   8888b.   .d8888b   .d8888b    .d88b.   .d8888b           #   
   #           888         888  888      "88b  88K       88K       d8P  Y8b  88K               #
  ###          888    888  888  888  .d888888  "Y8888b.  "Y8888b.  88888888  "Y8888b.         ###  
 #####         Y88b  d88P  888  888  888  888       X88       X88  Y8b.           X88        ##### 
#######         "Y8888P"   888  888  "Y888888   88888P'   88888P'   "Y8888    88888P'       #######

     
class rand:
    '''
    Random Variable Generator Class.
    '''
    @staticmethod
    def choose(iterator,k: int =1,duplicate=True):
        '''
        Return a random element from a non-empty sequence.
        '''
        if k==1:
            return random.choice(iterator)
        elif k>1:
            if duplicate:
                return random.choices(iterator,k=k)
            else:
                return random.sample(iterator,k=k)
        else:
            raise ValueError('k Must Be Higher 0')
        
    @staticmethod
    def integer(first_number,last_number):
        '''
        Return random integer in range [a, b], including both end points.
        '''
        return random.randint(first_number,last_number)
    @staticmethod
    def O1(decimal_number=17):
        '''
        return x in the interval [0, 1)
        '''
        return round(random.random(),decimal_number)
    @staticmethod
    def number(first_number,last_number):
        '''
        return x in the interval [F, L]
        '''
        return random.uniform(first_number,last_number)        


'''
class Math:
    def sqrt(number):
        import math
        return math.sqrt(number)
'''


class system:
    '''
    Some system actions and information.
    '''
    @staticmethod
    def accname():
        '''
        return account username you have logged in.
        '''
        return os.getlogin()
    @staticmethod
    def pid():
        '''
        Get pid number of terminal and return it.
        '''
        return os.getpid()
    @staticmethod
    def disk_usage(path):
        ####
        return shutil.disk_usage(path)
    @staticmethod
    def chdir(path):
        '''
        Change directory of terminal.
        '''
        os.chdir(path)
    @staticmethod
    def SHUT_DOWN():
        '''
        Shut down the PC.
        '''
        os.system("shutdown /s /t 1")
    @staticmethod
    def RESTART():
        '''
        Restart the PC.
        '''
        os.system("shutdown /r /t 1")
    @staticmethod
    def terminal_size():
        return os.get_terminal_size()
    @staticmethod
    def cwd():
        return os.getcwd()
    @staticmethod
    def ip_global():
        """
        Return ip with by http://ipinfo.io/ip api.
        returns global ip as string
        """
        try:
            new_session = requests.session()
            response = new_session.get("http://ipinfo.io/ip")
            ip_list = re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", response.text)
            new_session.close()
            return ip_list[0]
        except:
            class ConnectionError(requests.exceptions.ConnectionError):
                def __init__(self, message): super().__init__(message)
            raise ConnectionError('No Internet Connection')
    @staticmethod
    def ip_local():
        import platform
        """
        Return local ip of computer in windows by socket module
        and in unix with hostname command in shell.
        """
        class NetworkError(Exception):
            def __init__(self, message): super().__init__(message)
        try:
            ip = socket.gethostbyname(socket.gethostname())
            if ip != "127.0.0.1":
                return ip
            elif platform.system() != "Windows":
                command = sub.Popen(["hostname", "-I"],stdout=sub.PIPE,stderr=sub.PIPE,stdin=sub.PIPE,shell=False)
                response = list(command.communicate())
                if len(response[0]) > 0:
                    return str(response[0])[2:-4]
                raise NetworkError('No Network Connection')
            raise NetworkError('No Network Connection')
        except:
            raise
    @staticmethod
    def ram_total(convert=True):
        """
        Return total ram of board as string
        parameter convert: flag for convert mode (using of convert_byte function)
        """
        response = list(psutil.virtual_memory())
        if convert:
            return convert_bytes(int(response[0]))
        return str(response[0])
    @staticmethod
    def ram_used(convert=True):
        """
        Return how much ram is using.
        parameter convert: flag for convert mode (convert with convert_byte function)
        """
        response = list(psutil.virtual_memory())
        if convert:
            return convert_bytes(int(response[3]))
        return str(response[3])
    @staticmethod
    def ram_free(convert=True):
        """
        Return how much ram is available.
        parameter convert: flag for convert mode (convert with convert_byte function)
        """
        response = list(psutil.virtual_memory())
        if convert:
            return convert_bytes(int(response[1]))
        return str(response[1])
    @staticmethod
    def ram_percent(ONLY_NOM=False):
        """
        Return available ram percentage as an integer if ONLY_NOM, as string with % if not ONLY_NOM
        Parameter ONLY_NOM: flag for return type and value.
        """
        response = list(psutil.virtual_memory())
        if ONLY_NOM:
            return response[2]    
        return str(response[2]) + " %"
    @staticmethod
    def boot_time():
        '''
        Return the system boot time expressed in seconds since the epoch.
        '''
        return psutil.boot_time()




class files:
    #self.info: size-atime-mtime-hide-ronly
    '''
    (STATIC METHODS)
    Actions and information about files.
    READ FUNCTIONS DOCSTRING
    '''
    @staticmethod
    def size(path):
        '''
        return size of the file in byte(s).
        Also work on directories.
        '''
        return os.path.getsize(path)
        #rooye pooshe emtehan she

    @staticmethod
    def remove(path):
        '''
        Use this to delete a file or a directory.
        '''
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    @staticmethod
    def rename(old_name,new_name):
        '''Rename files with this function.'''
        os.rename(old_name,new_name)
    @staticmethod
    def abspath(path):
        '''
        return absolute path of given path.
        '''
        return os.path.abspath(path)
    @staticmethod
    def exists(path):
        '''
        Search for the file And Returns a boolean.
        if file exists: True
        else: False
        '''
        return os.path.exists(path)
    @staticmethod
    def mdftime(path):
        '''
        Get last modify time of the file.
        '''
        return os.path.getmtime(path)
    @staticmethod
    def acstime(path):    
        '''
        Get last access time of the file.
        '''
        return os.path.getatime(path)
        # change to date bayad biad
    @staticmethod
    def move(src,dst):
        '''
        Move (cut) file from crs to dst.
        '''
        shutil.move(src,dst)
        #live_path= dst
        #Baraye folder hast ya na?
    @staticmethod
    def copy(path,dst):
        '''
        Copy the file from src to destination.
        (You can use it instead of rename too.
         e.g:
            copy('D:\\Test.py','E:\\Ali.py')
            (It copies Test.py to E drive and renames it to Ali.py)
         )
        '''
        if os.path.isdir(path):
            shutil.copytree(path,dst)
        else:
            shutil.copy(path,dst)
    @staticmethod
    def hide(path,mode=True):
        '''
        Hide file or folder.
        If mode==False: makes 'not hide'
        '''
        if mode:
            os.system("attrib -h "+path)
        else:
            subprocess.check_call(["attrib","+H",path])
    @staticmethod
    def read_only(path,mode=True):
        '''
        Make file attribute read_only.
        If mode==False: makes 'not read_only'
        '''
        if type(mode)==bool:
            from stat import S_IREAD,S_IWUSR
            if mode==True:
                os.chmod(path, S_IREAD)
            elif mode==False:
                os.chmod(path, S_IWUSR)
        else:
            raise Exception('Second argumant (mode) should be boolean.')
    @staticmethod
    def read(path):
        '''
        This can help you to read your file faster.
        Example:
            read('C:\\users\\Jack\\test.txt')
            ==> "Content of 'test.txt' will be shown."
        '''
        op= open(path,mode='r')
        FileR= op.read()
        op.close()
        return FileR
    @staticmethod
    def write(path,text=None,mode='replace',start=''):
        if mode=='replace':
            op= open(path,mode='w')
            if text==None:
                text= input('Type what you want.\n\n')
            op.write(text)
            #print('File has been created/changed.')
            op.close()
        elif mode=='continue':
            '''opr= open(file,mode='r')
            FileR= opr.read()
            op= open(file,mode='w')'''
            op=open(path,'a')
            if text==None:
                text= input('Type what you want to add in the end of the file.\n\n')
            #op.write(FileR+'\n'+text)
            #op.write(FileR+text)
            op.write(start+text)
            #print('File has been created/changed.')
            op.close() 
        else:   
            print('Error\nmode can only be: 1-replace(default)  2-continue\nNot "{0}"'.format(mode)) 
    @staticmethod
    def isdir(path):
        return os.path.isdir(path)
    @staticmethod
    def isfile(path):
        return os.path.isfile(path)


class file:
    # hide-ronly
    '''
    (CLASS METHODS)
    Actions and Information about files and directories.
    READ METHODS DOCSTRING
    '''
    def __init__(self,path):
        self.path=    path
        self.live_path= path
        self.size=    None
        self.abspath= None
        self.acstime= None
        self.mdftime= None
        #self.content= None
        if files.exists(path):
            self.size= files.size(path)
            self.abspath= files.abspath(path)
            self.acstime= files.acstime(path)
            self.mdftime= files.mdftime(path)
            if os.path.isfile(path):
             self.type= 'file'
             self.content= files.read(path)
            if os.path.isdir(path):
             self.type='dir'                
             walk= os.walk(path)
             self.file_list=[]
             for i in walk:
                 self.file_list.append(i)
             self.files=self.file_list[0][2]
             self.all_files=[val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)] for val in sublist]
             self.all_files_sep=[[os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)]

    def delete(self):
        '''
        Use this to delete a file or a directory.\n
        FOR STATIC USAGE USE 'remove()'
        '''
        files.remove(self.path)            
    def rename(self,new_name):
        '''
        Rename files with this function.\n
        FOR STATIC USAGE USE 'chname()'
        '''
        os.rename(self.path,new_name)
    def move(self,dst):
        '''
        Move (cut) file from crs to dst.
        '''
        shutil.move(self.path,dst)
        #self.live_path= dst
        #Baraye folder hast ya na?
    def copy(self,dst):
        '''
        Copy the file from src to destination.
        (You can use it instead of rename too.
         e.g:
            copy('D:\\Test.py','E:\\Ali.py')
            (It copies Test.py to E drive and renames it to Ali.py)
         )
        '''
        files.copy(self.path,dst)
    def hide(self,mode=True):
        '''
        Hide file or folder.
        If mode==False: makes 'not hide'
        '''
        files.hide(self.path,mode)
    def read_only(self,mode=True):
        '''
        Make file attribute read_only.
        If mode==False: makes 'not read_only'
        '''
        files.read_only(self.path,mode)


    #####
    # ext of file - 
    #####



class style:
    '''
    This class is for Changing text Color,BG & Style.
    - style.print  to customize your print.
    - style.switch to change terminal colors.
    - style.switch_default for making everything default.
    '''
    def __init__(self,text,color='default',BG='black'):
        from colored import fg,bg,attr
        try: color= color.lower();BG=BG.lower()#;style=style.lower()
        except:pass        
        if color=='default':
            color=7 #188
        self.text= text     
        self.content= f"{fg(color)}{bg(BG)}{text}{attr(0)}"
    def __str__(self):
        return self.content
    def __repr__(self):
        return self.content
    def __add__(self,other):
        #print(type(other))
        if type(other)!=style:
            return self.content+other
        else:
            return self.content+other.content
    def __mul__(self,nom):
        return self.content*nom
    def __getitem__(self,index):
        return self.text[index]


    @staticmethod
    def print(text='',color='default',BG='black',style='None',end='\n'):
        '''
        text(text='Hello World',color='red',BG='white')
        output ==> 'Hello World' (With red color and white BG)
        Styles: bold - underline - reverse - hidden
         *bold and underline may not work. (Depends on terminal and OS)
        '''
        from colored import fg,bg,attr
        try: color= color.lower();BG=BG.lower();style=style.lower()
        except:pass
        if color=='default':
            color=7 #188
        if style=='none':
            style=0
        if text=='':
            print('%s%s%s' % (attr(style),bg(BG),fg(color)),end=end)
        else:
            print('%s%s%s%s%s' % (attr(style),bg(BG),fg(color),text,attr(0)),end=end)
    @staticmethod
    def switch(color='default',BG='black',style='None'):
        '''
        Change color,BG and style untill you call it again and change them.
        '''
        try: color= color.lower();BG=BG.lower();style=style.lower()
        except:pass        
        if style=='none':
            style=0
        if color=='default':
            color=7
        from colored import fg,bg,attr
        print('%s%s%s' % (attr(style),bg(BG),fg(color)),end='')
    @staticmethod
    def switch_default():
        '''Switch Terminal Attributes to its defaults'''
        from colored import attr
        print('%s' % (attr(0)),end='')

# reset, clear lap, lap(save=True)
class record:
    '''
    Use this method to record an action time in second.
    Usage:
        Start= record()
        #Some codes here...
        Finnish= Start.lap()
        print(Finnish) ==> 0.25486741
        #Some more codes here...
        Finnish= Start.lap() ==> 0.4502586
    Use Start.stop() to finnish recording and save memory.
    (after self.stop() using self.lap will cause error.)
    '''
    def __init__(self):
        self.start= time.time()
        self.__end__=False
        self.laps=[]
    def __str__(self):
        if not self.__end__:
            running=True
        else:
            running=False
        return f'Running={str(running)} \nLaps: {self.laps}'
    def __repr__(self):
        if not self.__end__:
            running=True
        else:
            running=False
        return f'Running={str(running)} \nLaps: {self.laps}'

    class EndError(Exception):
        def __init__(self, message='Recording Has Been Finnished. Can Not Add a Lap.'):
            super().__init__(message)
    def lap(self):
        '''
        Return time of self.
        (Read 'record' Doc String)
        '''        
        if not self.__end__:
            lp= time.time()-self.start
            self.laps.append(lp)
            return lp
        else:
            raise self.EndError
    def stop(self):
        self.__end__=True
        '''del self
        return self.laps'''

#END
