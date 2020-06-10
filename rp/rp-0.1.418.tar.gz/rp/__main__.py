from rp.r import *
import rp.prompt_toolkit
def main():
    text_to_speech("yankee doodle")
    pseudo_terminal(locals(),globals(),rprc='from rp import *')
if __name__=='__main__':
    main()