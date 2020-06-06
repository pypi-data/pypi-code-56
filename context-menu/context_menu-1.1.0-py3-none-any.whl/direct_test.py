import sys
sys.path.append('.')




if __name__ == '__main__':
    import menus

    fc = menus.FastCommand('Example Fast Command 5', type='FILES', command='cd ? & mkdir hello', command_vars=['DIR'])
    fc.compile()
