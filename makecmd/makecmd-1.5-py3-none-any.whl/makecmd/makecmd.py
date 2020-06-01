#!/usr/bin/env python3
import argparse
import os
from os.path import exists
import sys
import platform


class Makecmd(object):

    def __init__(self):
        # Directory for storing the python executable conversion
        self.exec_directory = "/usr/local/bin"
        self.exec_tag = "#!/usr/bin/env python3"
        self.filename_directory = "/tmp"
        self.os = platform.platform()
        parser = argparse.ArgumentParser(description='Converts Python scripts to callable shell commands',
                                         usage='''makecmd <command> [file] 
    
        The most command commands used with makecmd are: 

        convert     Converts Python file into shell executable
        list        Lists files converted by makecmd
        delete      Deletes bash executables made by makecmd
        ''')

        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()
        #self.args2 = parser.parse_args(sys.argv[2:])

    def convert(self):

        # Function to prepend executable tag at beginning of selected Python file
        def prepend_line(file_name, line):
            """ Insert given string as a new line at the beginning of a file """
            # define name of temporary dummy file
            dummy_file = file_name + '.bak'
            # open original file in read mode and dummy file in write mode
            with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
                # Write given line to the dummy file
                write_obj.write(line + '\n')
                # Read lines from original file one by one and append them to the dummy file
                for line in read_obj:
                    write_obj.write(line)
            # remove original file
            os.remove(file_name)
            # Rename dummy file as the original file
            os.rename(dummy_file, file_name)

        parser = argparse.ArgumentParser(description="""
        Converts Python file to bash executable
    
        """)
        exec_tag = "#!/usr/bin/env python3"
        parser.add_argument("file", type=str, help="Name of Python file")
        args = parser.parse_args(sys.argv[2:])
        FILE = args.file

        try:
            if (not FILE[FILE.index('.'):] == ".py"):
                print("File is not a Python file. Please try again.")
                exit(1)

            if (not exists(FILE)):
                print("File does not exist. Please try again.")
                exit(1)
        except ValueError:
            print("File does not have an extension. Please try again.")
            exit(1)

        with open(FILE, "r") as py_file_read:
            py_lines = py_file_read.readlines()
            py_file_read.close()

        if (py_lines[0].strip("\n") != exec_tag):
            prepend_line(FILE, exec_tag)
        else:
            pass

        new_filename = FILE[0: FILE.index('.')] + "\n"
        if ("Linux" in self.os):
            self.exec_directory = "/usr/bin"
        os.system(f"sudo cp {FILE} {self.exec_directory}")
        os.system(
            f"sudo mv {self.exec_directory}/{FILE} {self.exec_directory}/{new_filename}")
        os.system(f"sudo chmod +x {self.exec_directory}/{new_filename}")
        os.system(f"touch {self.filename_directory}/filenames.txt")
        with open(f"{self.filename_directory}/filenames.txt", "r") as file_storage_read:
            lines = file_storage_read.readlines()
            file_storage_read.close()
        with open(f"{self.filename_directory}/filenames.txt", "w+") as file_storage_change:
            for line in lines:
                if line.strip("\n") != new_filename.strip("\n"):
                    file_storage_change.write(line)
                else:
                    pass
            file_storage_change.close()
        with open(f"{self.filename_directory}/filenames.txt", "a") as file_storage:
            file_storage.write(new_filename)
            file_storage.close()

    def list(self):
        parser = argparse.ArgumentParser(description="""
        Lists files converted by bashify """)
        args = parser.parse_args(sys.argv[2:])
        with open(f"{self.filename_directory}/filenames.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                print(line.strip("\n"))

    def delete(self):
        parser = argparse.ArgumentParser(description="""
        Deletes files converted by bashify
        """
                                         )
        parser.add_argument("file", type=str, help="Name of bash executable")
        args = parser.parse_args(sys.argv[2:])

        FILE = args.file
        try:
            os.system(f"rm -rf {self.exec_directory}/{FILE}")
            print("file successfully deleted")
        except FileNotFoundError:
            print("File does not exist. Please try again")
            exit(1)

        with open(f"{self.filename_directory}/filenames.txt", "r") as file_read:
            lines = file_read.readlines()
        with open(f"{self.filename_directory}/filenames.txt", "w+") as file_write:
            for line in lines:
                if (line.strip("\n") != FILE.strip("\n")):
                    file_write.write(line)
            file_write.close()

def main():
    Makecmd()


if __name__ == "__main__":
    main()







