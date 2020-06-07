import sys
sys.path.append('.')




if __name__ == '__main__':
    import menus

    fc = menus.FastCommand('Example Fast Command 7', type='.txt', command='cd ? & mkdir hello', command_vars=['DIR'])
    fc.compile()
