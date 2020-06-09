import os

os.system('wget -qO bat.deb https://github.com/sharkdp/bat/releases/download/v0.15.4/bat_0.15.4_amd64.deb')
os.system('dpkg -i bat.deb')
os.remove('bat.deb')

os.makedirs('/root/.config/bat')
with open('/root/.config/bat/config', "w") as f:
    f.write('''
--theme="ansi-light"
--wrap=never
''')

