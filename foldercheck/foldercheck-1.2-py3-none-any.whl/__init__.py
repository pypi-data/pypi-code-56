#                                  Folder Checker
#
# for Python 3
# ©Anime no Sekai - 2020
#

# Imports
from time import sleep
from datetime import date
from datetime import datetime

import subprocess
import os
import shutil
import sys
import platform

from lifeeasy import working_dir

# Variable declaration
folder_path = ''
folder_name = ''
folder_check_result_folder = ''
destination_folder = ''
deletedfiles = []
moved_to_trash_files = []
kept_files = []

# Initialization
def initialization():
    global folder_path
    if __name__ == "__main__":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("         - Welcome on Folder Checker! -       ")
        print('')
        print("by Anime no Sekai")
        print('')
        print('')
        ask_for_folder_path()
    else:
        folder_path = working_dir()

# Asking for the folder to check
def ask_for_folder_path():
    global folder_path

    print("What is the path to the folder you wanna check today?")
    sleep(0.1)
    folder_path = input('> ')
    indexes_of_slash = [i for i, ltr in enumerate(folder_path) if ltr == "\\"]
    number_of_iterations = 0
    for index in indexes_of_slash:
        character_after_slash = folder_path[index + 1 - number_of_iterations]
        print(character_after_slash)
        if character_after_slash == ' ' or character_after_slash == '/':
            folder_path = folder_path[:index - number_of_iterations] + folder_path[index + 1 - number_of_iterations:]
            number_of_iterations += 1
    if folder_path.lower() == 'cancel' or folder_path.lower() == 'stop' or folder_path.lower() == 'quit' or folder_path.lower() == 'exit':
        goodbye_message()
    elif not os.path.isdir(folder_path):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('You mistyped something in your folder path')
        sleep(1)
        print('Please try again...')
        sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        print('')
        ask_for_folder_path()
    else:
        display_action("Loading the folder")

        create_session_folder()

# Creating the session folder
def create_session_folder():
    global destination_folder
    global folder_check_result_folder
    global folder_path
    global folder_name

    if folder_path.endswith('/'):
        folder_path = folder_path[:-(1)]
    folder_check_result_folder = "{}/Folder Check".format(folder_path)
    
    if not os.path.isdir(folder_check_result_folder):
        os.makedirs(folder_check_result_folder)
        create_session_folder()

    index_of_last_slash = folder_path.rfind('/')
    folder_name = folder_path[index_of_last_slash:]

    results_folder = folder_check_result_folder + '/' + folder_name + ' ' + str(date.today())

    number = 0
    if os.path.isdir(results_folder):
        number += 1
    while os.path.isdir(results_folder + ' ' + str(number)):
        number += 1
    number = str(number)
    if number == '0':
        os.makedirs(results_folder)
        destination_folder = results_folder
    else:
        os.makedirs(results_folder + ' ' + number)
        destination_folder = results_folder + ' ' + number
    
    core()

# The core of the program, asking the user to take a decision on all files of the folder
def core():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Commands
    print("Commands available")
    print('____________________________')
    print('')
    print(" 'o' or 'open'       >    to open the file")
    print("'rev' or 'reveal'    >    to reveal the file in your file explorer")
    print(" 'r' or 'remove'     >    to move the file into the trash folder")
    print(" 'R'                 >    to delete the file permanently")
    print(" '-R'                >    to delete the file permanently (without confirmation)")
    print("'stop' or 'cancel'   >    to stop the execution")
    print('')
    print(" - Any other key to keep the file in his location - ")
    print('')
    print('')
    print('')
    input('Press any key to continue...')
    os.system('cls' if os.name == 'nt' else 'clear')
    list_of_files_in_folder = os.listdir(folder_path)
    kept_files = list_of_files_in_folder
    for file in list_of_files_in_folder: 
        if file == __file__:
            continue
        if file == 'Folder Check':
            continue
        if file == '.DS_Store':
            continue
        if file == '.gitattributes':
            continue
        if file == '.git':
            continue
        os.system('cls' if os.name == 'nt' else 'clear')
        def user_decision():
            show_commands()
            print('')
            print('What do you want to do with the file/folder: ' + file)
            user_input = input('> ')
            if user_input == 'o' or user_input == 'open':
                display_action('Opening you file')
                open_file(file)
                user_decision()
            elif user_input == 'r' or user_input == 'remove':
                display_action('Moving your file to the trash folder')
                end_point = move_to_trash_folder(file)
                if end_point == 'The user decided not to move this file to the trash.':
                    user_decision()
            elif user_input == 'R':
                print('This file will be deleted permanently')
                confirmation = input('Type [yes] if you really want to delete it or anything else to abort: ')
                if confirmation.lower() == 'yes':
                    display_action('Deleting your file')    
                    end_point = remove(file)
                    if end_point == 'The user decided not to erase this file.':
                        user_decision()
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    user_decision()
            elif user_input == '-R' or user_input == 'removenow':
                display_action('Deleting your file')
                end_point = remove(file)
                if end_point == 'The user decided not to erase this file.':
                    user_decision()
            elif user_input.lower() == 'reveal' or user_input.lower() == 'rev':
                reveal(file)
                user_decision()
            elif user_input.lower() == 'stop' or user_input.lower() == 'cancel' or user_input.lower() == 'exit' or user_input.lower() == 'quit':
                display_action('Stoping')
                goodbye_message()
            elif user_input != '':
                print('No known command detected')
                sleep(1)
                print('Next File!')
                sleep(0.5)
            else:
                print('Next File!')
                sleep(0.5)
        user_decision()
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Done!')
    sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Do you want a summary of all actions?")
    user_choice_on_summary = input("Type [no] for no summary: ")
    if user_choice_on_summary.lower() == 'no':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Ok!')
        display_action('Opening the result folder')
        subprocess.call(["open", "-R", destination_folder])
        sleep(2)
        if '-d' in sys.argv or '--debug' in sys.argv:
            os.system('cls' if os.name == 'nt' else 'clear')
            input("Enter any key when you are ready to display the debug message...")
            os.system('cls' if os.name == 'nt' else 'clear')
            debug()
        goodbye_message()
    else:
        # Deleted files
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Here are the permanently deleted files')
        print('___________________________________________')
        print('')
        file_number = 0
        for deletedfile in deletedfiles:
            file_number += 1
            print(deletedfile)
        if file_number == 0:
            print("No deleted file.")
        print('')
        print('Total: ' + str(file_number))
        input('Press any key to continue...')
        # Moved to trash files
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Here are the files moved to trash')
        print('___________________________________________')
        print('')
        file_number = 0
        for movedfile in moved_to_trash_files:
            file_number += 1
            print(movedfile)
        if file_number == 0:
            print("No file got moved to trash.")
        print('')
        print('Total: ' + str(file_number))

        input('Press any key to continue...')

        # Kept files
        for file in deletedfiles:
            kept_files.remove(file)
        for file in moved_to_trash_files:
            kept_files.remove(file)

        os.system('cls' if os.name == 'nt' else 'clear')
        print('Here are the kept files')
        print('___________________________________________')
        print('')
        file_number = 0
        for file in kept_files:
            file_number += 1
            print(file)
        if file_number == 0:
            print("No file got kept in the folder.")
        print('')
        print('Total: ' + str(file_number))

        end_choice = input('Press [any key] to quit or [save] to save this summary to a file... ')
        if end_choice.lower() == 'save' or end_choice.lower() == 'ave' or end_choice.lower() == 'sve' or end_choice.lower() == 'sae' or end_choice.lower() == 'sav' or end_choice.lower() == 'export' or end_choice.lower() == 'download':
            display_action('Creating your file')
            os.chdir(destination_folder)
            summary_file = open("summary_file.txt", "w+")

            summary_file.write("Here is the summary of all actions taken on the folder: {} \n".format(folder_name))
            summary_file.write(datetime.now().strftime("%B, the %d of %Y") + '\n')

            summary_file.write('\n')
            summary_file.write('\n')
            summary_file.write('\n')

            summary_file.write('Here are the permanently deleted files\n')
            summary_file.write('___________________________________________\n')
            summary_file.write('\n')
            file_number = 0
            for deletedfile in deletedfiles:
                file_number += 1
                summary_file.write(deletedfile + '\n')
            if file_number == 0:
                summary_file.write("No deleted file.\n")
            
            number_of_permanently_deleted_files = file_number
            summary_file.write('\n')
            summary_file.write('Total: ' + str(file_number) + '\n')

            summary_file.write('\n')
            summary_file.write('\n')
            summary_file.write('\n')

            summary_file.write('Here are the files moved to trash\n')
            summary_file.write('___________________________________________\n')
            summary_file.write('\n')
            file_number = 0
            for movedfile in moved_to_trash_files:
                file_number += 1
                summary_file.write(movedfile + '\n')
            if file_number == 0:
                summary_file.write("No file got moved to trash.\n")
            
            number_of_files_moved_to_trash = file_number
            summary_file.write('\n')
            summary_file.write('Total: ' + str(file_number) + '\n')

            summary_file.write('\n')
            summary_file.write('\n')
            summary_file.write('\n')

            summary_file.write('Here are the kept files\n')
            summary_file.write('___________________________________________\n')
            summary_file.write('\n')
            file_number = 0
            for file in kept_files:
                file_number += 1
                summary_file.write(file + '\n')
            if file_number == 0:
                summary_file.write("No file got kept in the folder.\n")

            number_of_kept_files = file_number
            summary_file.write('\n')
            summary_file.write('Total: ' + str(file_number) + '\n')
            summary_file.write('\n')
            summary_file.write('\n')
            summary_file.write('\n')
            summary_file.write('\n')
            summary_file.write('\n')
            summary_file.write('TOTAL OF FILES: {}\n'.format(number_of_files_moved_to_trash + number_of_kept_files + number_of_permanently_deleted_files))
            summary_file.write('\n')
            summary_file.write('\n')
            summary_file.write('Generated by Folder Checker\n')
            summary_file.write('©Anime no Sekai - 2020')

            summary_file.close()

        display_action('Opening the result folder')
        subprocess.call(["open", "-R", destination_folder])
        sleep(1)
        if '-d' in sys.argv or '--debug' in sys.argv:
            os.system('cls' if os.name == 'nt' else 'clear')
            input("Enter any key when you are ready to display the debug message...")
            os.system('cls' if os.name == 'nt' else 'clear')
            debug()
        goodbye_message()





# Decision responses
def show_commands():
    print(" 'o' or 'open'       >    to open the file")
    print("'rev' or 'reveal'    >    to reveal the file in your file explorer")
    print(" 'r' or 'remove'     >    to move the file into the trash folder")
    print(" 'R'                 >    to delete the file permanently")
    print(" '-R'                >    to delete the file permanently (without confirmation)")
    print("'stop' or 'cancel'   >    to stop the execution")

def open_file(file):
    file_path = folder_path + '/' +  file
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', file_path))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(file_path)
    else:                                   # linux variants
        subprocess.call(('xdg-open', file_path))

def move_to_trash_folder(file):
    global moved_to_trash_files
    file_path = folder_path + '/' +  file
    file_extension = extension(file)
    if file_extension in type_system_data():
        print('A system file was detected.')
        sleep(1)
        print('Moving this file to the trash might not work')
        sleep(1)
        user_input = input('Do you still wanna move this file to the trash? ([yes] or any other key to abort) ')
        if user_input.lower() == 'yes':
            try:
                shutil.move(file_path, destination_folder)
                moved_to_trash_files.append(file)
            except:
                print('A problem occured while moving your file to the trash folder.')
                sleep(1)
                print('The file will be kept in his current location')
                sleep(1)
        else:
            return 'The user decided not to move this file to the trash.'
    else:
        try:
            shutil.move(file_path, destination_folder)
            moved_to_trash_files.append(file)
        except:
            print('A problem occured while moving your file to the trash folder.')
            sleep(1)
            print('The file will be kept in his current location')
            sleep(1)

def remove(file):
    global deletedfiles
    file_path = folder_path + '/' +  file
    file_extension = extension(file)
    if file_extension in type_system_data():
        print('A system file was detected.')
        sleep(1)
        print('Erasing might not work on this file')
        sleep(1)
        user_input = input('Do you still wanna try to erase it? ([yes] or any other key to abort) ')
        if user_input.lower() == 'yes':
            if os.path.isdir(file_path):
                try:
                    shutil.rmtree(file_path)
                    deletedfiles.append(file)
                except:
                    print('An error occured while deleting your folder.')
                    sleep(1)
                    print('The folder will be kept in his current location')
                    sleep(1)
            else:
                try:
                    os.remove(file_path)
                    deletedfiles.append(file)
                except:
                    print('An error occured while deleting your file.')
                    sleep(1)
                    print('The file will be kept in his current location')
                    sleep(1)
        else:
            return 'The user decided not to erase this file.'
    else:
        if os.path.isdir(file_path):
            try:
                shutil.rmtree(file_path)
                deletedfiles.append(file)
            except:
                print('An error occured while deleting your folder.')
                sleep(1)
                print('The folder will be kept in his current location')
                sleep(1)
        else:
            try:
                os.remove(file_path)
                deletedfiles.append(file)
            except:
                print('An error occured while deleting your file.')
                sleep(1)
                print('The file will be kept in his current location')
                sleep(1)

def reveal(file):
    file_path = folder_path + '/' +  file
    if platform.system() == 'Windows':       # macOS
        print('Sorry, Windows does not support revealing files in the file explorer')
        display_action('Opening the folder instead')
        os.startfile(folder_path)
    else:
        display_action('Revealing the file in your file explorer')
        subprocess.call(["open", "-R", file_path])


# Nice way to display performed actions to the user
def display_action(action_to_display):
    for _ in range(2):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(action_to_display + ".")
        sleep(0.15)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(action_to_display + "..")
        sleep(0.15)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(action_to_display + "...")
        sleep(0.15)

# Good Bye message
def goodbye_message():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Thank you for using this program!')
    sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("F")
    sleep(0.2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Fo")
    sleep(0.18)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Fol")
    sleep(0.15)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Fold")
    sleep(0.11)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Folde")
    sleep(0.06)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Folder")
    sleep(0.07)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Folder C")
    sleep(0.09)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Folder Ch")
    sleep(0.13)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Folder Che")
    sleep(0.16)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Folder Check")
    sleep(0.18)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Folder Checke")
    sleep(0.19)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Folder Checker")
    sleep(2)
    print('')
    print('© Anime no Sekai - 2020')
    print('')
    sleep(3)
    quit()

##### Debug
def debug():
    print('')
    print('')
    print('// START OF DEBUG //')
    print('')
    print("If you get the 'ModuleNotFoundError: No module named 'psutil'':  you need to install the psutil module in order to get access to debug")
    print("If you already have pip installed: enter 'pip install psutil' to easily install it'")
    print("If not, just download pip as explained on this page: https://pip.pypa.io/en/stable/installing/ and then install the psutil module with 'pip install psutil'")
    print('')
    print('')
    print('Arguments passed: ' + str(sys.argv))
    print('')
    print('')
    print('#VERSIONS')
    print('Folder Check v.0.9.5 Beta by Anime no Sekai')
    print(sys.version)
    print('')
    print('')
    print('#SYSTEM INFORMATION')
    print("System information code credit: PythonCode")
    print("https://www.thepythoncode.com/article/get-hardware-system-information-python")
    print('')

    import psutil
    import platform
    from datetime import datetime

    def get_size(bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor


    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")

    # Boot Time
    print("="*40, "Boot Time", "="*40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

    # let's print CPU information
    print("="*40, "CPU Info", "="*40)
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

    # Memory Information
    print("="*40, "Memory Information", "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")

    # Disk Information
    print("="*40, "Disk Information", "="*40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")

    # Network information
    print("="*40, "Network Information", "="*40)

    # Remove the pair of ''' if you want to have your IP and MAC address (it will be added to the troubleshoot file if you output everything to a troubleshoot file > troubleshoot.txt)
    '''
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    '''
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

    print('')
    print('')
    print('')
    print('#GLOBAL VARIABLES')
    print('')
    print('1. ' + folder_path)
    print('2. ' + folder_name)
    print('3. ' + folder_check_result_folder)
    print('4. ' + destination_folder)
    print('5. ' + str(deletedfiles))
    print('6. ' + str(moved_to_trash_files))
    print('7. ' + str(kept_files))
    
    print('')
    print('')
    print('')
    print('// END OF DEBUG //')
    print('')
    input("Enter any key to quit...")



###### DATA ######
### Data from my library filecenter
### Consider checking it out too ☆(･ω･*)ゞ
###

def extension(file):
    file_extension = ''
    filename, file_extension = os.path.splitext(file)
    return(file_extension)

def type_system_data():
    data = ['.hiv', '.mapimail', '.73u', '.bash_history', '.admx', '.ebd', '.reg', '.iconpackage', '.regtrans-ms', '.htt', '.cur', '.searchconnector-ms', '.aml', '.pck', '.sdt', '.ani', '.dll', '.deskthemepack', '.dvd', '.desklink', '.lnk', '.ftf', '.clb', '.scr', '.dmp', '.cpl', '.icns', '.pk2', '.ion', '.nfo', '.inf_loc', '.mdmp', '.nt', '.library-ms', '.msc', '.theme', '.cab', '.wdgt', '.ico', '.sys', '.asec', '.sfcache', '.rc1', '.qvm', '.manifest', '.log1', '.000', '.prop', '.dat', '.fota', '.h1s', '.cannedsearch', '.cgz', '.vx_', '.bin', '.etl', '.mi4', '.rmt', '.lockfile', '.drpm', '.ci', '.bashrc', '.edj', '.pat', '.vga', '.zone.identifier', '.ffx', '.pwl', '.mui', '.sys', '.mobileconfig', '.mtz', '.profile', '.mlc', '.bash_profile', '.3fs', '.bcd', '.wdf', '.bio', '.msstyles', '.cm0013', '.msp', '.lfs', '.0', '.bom', '.sdb', '.c32', '.elf', '.pnf', '.dimax', '.group', '.pdr', '.mbr', '.dev', '.webpnp', '.hhk', '.208', '.efi', '.pit', '.adm', '.diagcab', '.ins', '.drv', '.firm', '.job', '.pol', '.log2', '.cnt', '.ime', '.prefpane', '.savedsearch', '.img3', '.ioplist', '.cat', '.ppd', '.dthumb', '.vxd', '.hcd', '.wpx', '.dit', '.sbf', '.key', '.fx', '.prf', '.8xu', '.lst', '.adml', '.386', '.mbn', '.cmo', '.cpq', '.grp', '.swp', '.thumbnails', '.ffo', '.shsh', '.aos', '.ffa', '.schemas', '.8cu', '.tdz', '.sbn', '.itemdata-ms', '.chg', '.timer', '.mod', '.hdmp', '.sqm', '.hlp', '.flg', '.dfu', '.idx', '.odex', '.chk', '.blf', '.shd', '.2fs', '.cpi', '.trx_dll', '.fpbf', '.pro', '.tha', '.printerexport', '.icl', '.crash', '.pfx', '.wer', '.adv', '.nb0', '.cht', '.ko', '.hhc', '.fl1', '.atahd', '.nbh', '.msstyle', '.ps2', '.prt', '.mui_cccd5ae0', '.ks', '.im4p', '.ruf', '.metadata_never_index', '.saver', '.str', '.mum', '.xrm-ms', '.kext', '.customdestinations-ms', '.uce', '.pid', '.xfb', '.rs', '.fid', '.hsh', '.chs', '.bk2', '.idi', '.sb', '.gmmp', '.hpj', '.rfw', '.spl', '.efires', '.configprofile', '.provisionprofile', '.escopy', '.service', '.ifw', '.mem', '.ta', '.lpd', '.cap', '.cpr', '.so.0', '.grl', '.scf', '.vgd', '.trashes', '.nls', '.bmk', '.automaticdestinations-ms', '.kbd', '.devicemetadata-ms', '.dyc', '.me', '.ps1', '.evtx', '.qky', '.ppm', '.fts', '.ntfs', '.dss', '.lpd', '.wph', '.iptheme', '.jpn', '.rco', '.mydocs', '.ipod', '.bud', '.wgz', '.dlx', '.spx', '.scap', '.bk1', '.evt', '.cdmp', '.mmv', '.panic', '.diagcfg', '.kor', '.rcv', '.ftg', '.ius', '.emerald', '.networkconnect', '.reglnk', '.ffl', '.hve', '.plasmoid', '.sin', '.ann', '.help', '.internetconnect', '.diagpkg', '.rc2', '.rvp', '.its']
    return data

### END OF DATA ###

initialization()
