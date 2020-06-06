#!/usr/bin/env python3

from os import \
    makedirs, environ

from os.path import \
    join as pjoin, \
    expanduser, isdir, \
    basename, isfile, dirname

from socket import \
    socket as sock, \
    timeout as TimeOutError, \
    SOCK_DGRAM, SHUT_WR, \
    AF_INET, SOCK_STREAM

from argparse import ArgumentParser

from yaml import \
    load as yload, \
    dump as ydump, \
    Loader, Dumper

from json import \
    loads as jload, \
    dumps as jdump
from json.decoder import \
    JSONDecodeError

from time import sleep

try:
    import readline
except (ImportError, ModuleNotFoundError):
    pass

from requests import post

from inquirer import prompt, List as iList

from cmd import Cmd

from pavlovadm.colortext import tabd, error, bgre

class PavlovADM(Cmd):
	servers = {}
	gameini = ''
	itemtbl = ''
	maptbl = '~/.cache/pavlovadm/maps.tbl'
	mapnames = {}
	maps = {}
	hlp = None
	cnt = 0
	dbg = None
	pwd = None
	def __init__(self, *args, **kwargs):
		self.use_rawinput = False
		for (k, v) in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
		super().__init__()
		self.serverselect()

	def serverselect(self):
		ask = [
            iList(
                'srv',
                carousel=True,
                message='select server',
                choices=[s for s in self.servers.keys()] + ['<Exit>'],
            ),
        ]
		srv = list(prompt(ask).values())[0]
		if srv == '<Exit>':
			exit()
		while True:
			cmd = self._cmdselects(srv)
			if not cmd:
				continue
			if cmd == '<Disconnect>':
				self.maps = {}
				break
			res = self.rconexec(srv, cmd.strip('<>'))
			if res:
				print(tabd(res))
		self.serverselect()

	def _getmapname(self, mapid):
		if mapid in self.mapnames:
			return self.mapnames[mapid]
		url = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
		res = post('%s%s'%(url, mapid.strip('UGC')))
		for l in res.text.split('\n'):
			if 'workshopItemTitle' in l:
				return l.split('>')[1].split('<')[0]

	def _getmaps(self, srv, noask=None):
		if not self.maps:
			maplst = self.gameini
			if len(self.servers[srv]) > 1:
				maplst = self.servers[srv][1]
			if maplst.startswith('~'):
				maplst = expanduser(maplst)
			if not maplst.startswith('/'):
				print('error: cannot read maplist if no absolute path is provided')
			with open(maplst, 'r') as mfh:
				lines = mfh.readlines()
			try:
				with open(expanduser(self.maptbl), 'r') as mfh:
					self.mapnames = yload(mfh.read(), Loader=Loader)
			except FileNotFoundError:
				with open(expanduser(self.maptbl), 'w+') as mfh:
					mfh.write(ydump({}, Dumper=Dumper))
				self.mapnames = {}
			for l in lines:
				if not l or not l.startswith('MapRotation'):
					continue
				ugcid = l.split('MapId="')[1].split('", ')[0]
				gmmod = l.split('GameMode="')[1].split('")')[0]
				name = self._getmapname(ugcid)
				self.maps[name] = [ugcid, gmmod]
				self.mapnames[ugcid] = name
			with open(expanduser(self.maptbl), 'w+') as mfh:
				mfh.write(ydump(self.mapnames, Dumper=Dumper))
			if noask: return self.mapnames
		ask = [
          iList(
            'map',
            carousel=True,
            message='select map',
            choices=[m for m in self.maps.keys()] + ['<Return>'],
          ),
        ]
		mapp = list(prompt(ask).values())[0]
		if mapp == '<Return>':
			return
		mmod = self.maps[mapp][1]
		modes = [mmod] + [s for s in ['SND', 'TDM', 'DM', 'GUN'] if s != mmod]
		ask = [
            iList(
                'mod',
                carousel=True,
                message='select mode (irrelevant if set by map)',
                choices=[m for m in modes] + ['<Return>'],
            ),
        ]
		mode = list(prompt(ask).values())[0]
		if mode != '<Return>':
			return '%s %s'%(self.maps[mapp][0], mode)

	def _getitem(self):
		with open(self.itemtbl, 'r') as ifh:
			items = [l.split(',')[0] for l in ifh.readlines()]
		ask = [
            iList(
                'item',
                carousel=True,
                message='select item',
                choices=items  + ['<Return>'],
            ),
        ]
		item = list(prompt(ask).values())[0]
		if item != '<Return>':
			return item


	def _getskin(self):
		ask = [
            iList(
                'skin',
                carousel=True,
                message='select skin',
                choices=['clown', 'prisoner', 'naked', 'farmer', 'russian', 'nato', '<Return>'],
            ),
        ]
		skin = list(prompt(ask).values())[0]
		if skin != '<Return>':
			return skin

	def _getammotype(self):
		ask = [
            iList(
                'ammo',
                carousel=True,
                message='select ammo-limit',
                choices=[0, 1, 2, '<Return>'],
            ),
        ]
		ammo = list(prompt(ask).values())[0]
		if ammo != '<Return>':
			return ammo

	def _getteam(self):
		ask = [
            iList(
                'team',
                carousel=True,
                message='select team',
                choices=["Blue Team (Defenders)", "Red Team (Attackers)", '<Return>'],
            ),
        ]
		team = list(prompt(ask).values())[0]
		if team != '<Return>':
			return team

	def _getcash(self):
		c = 0
		while True:
			cash = input('enter amount of cash (as number)')
			if cash.isdigit():
				return cash
			c+=1
			if c < 3:
				print('thats not a number - let\'s try again')
			else:
				print('too dumb for numbers? o.0 aborting...')

	def _cmdselects(self, srv):
		noargs = ['Info', 'ResetSND', 'RefreshList', 'RotateMap', 'ServerInfo', 'Help', '<Disconnect>']
		steams = ['Kick', 'Ban', 'Unban', 'InspectPlayer']
		others = ['SwitchMap', 'SwitchTeam', 'GiveItem', 'GiveCash', 'GiveTeamCash', 'SetPlayerSkin', 'SetLimitedAmmoType']
		order = ['Info', 'SwitchMap', 'RotateMap', 'ResetSND', 'Kick', 'Ban', 'Unban', 'InspectPlayer', 'GiveItem', 'GiveCash', 'GiveTeamCash', 'SetPlayerSkin', 'SetLimitedAmmoType', 'RefreshList', 'ServerInfo', '<Disconnect>']
		hlp = self.hlp if self.hlp else self.rconexec(srv, 'Help')
		if not hlp:
			error('no help', hlp)
		hlp = hlp['Help']
		hlp = [h.split(' ')[0] for h in hlp.split(', ') if h.split(' ')[0]] + ['Info']
		ask = [
            iList(
                'cmd',
                carousel=True,
                message='select command',
                choices=[o for o in order if o.strip('<>') in hlp],
            ),
        ]
		cmd = list(prompt(ask).values())[0].strip()
		if cmd in noargs:
			return cmd
		elif cmd in steams:
			sid = self._getsteamid(srv, cmd)
			if not sid:
				return
			return '%s %s'%(cmd, sid)
		elif cmd in others:
			if cmd == 'SwitchMap':
				mapmod = self._getmaps(srv)
				if not mapmod:
					return
				return 'SwitchMap %s'%mapmod
			elif cmd == 'SwitchTeam':
				sid = self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'SwitchTeam %s %s'%(sid, self._getteam())
			elif cmd == 'GiveItem':
				sid = self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'GiveItem %s %s'%(sid, self._getitem())
			elif cmd == 'GiveCash':
				sid = self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'GiveCash %s %s'%(sid, self._getcash())
			elif cmd == 'GiveTeamCash':
				team = self._getteam()
				if not team:
					return
				return 'GiveTeamCash %s %s'%(team, self._getcash())
			elif cmd == 'SetPlayerSkin':
				sid = self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'SetPlayerSkin %s %s'%(sid, self._getskin())
			elif cmd == 'SetLimitedAmmoType':
				ammo = self._getammotype()
				if not ammo:
					return
				return 'SetLimitedAmmoType %s'%ammo

	def _getsteamid(self, srv, cmd):
		userids = self._players(srv)
		if not userids:
			print('\nerror: executing "%s" is impossible - no players\n'%cmd)
			return
		ask = [
            iList(
                'user',
                carousel=True,
                message='select user to %s'%cmd,
                choices=list(userids.keys()) + ['<Return>'],
            ),
        ]
		usr = list(prompt(ask).values())[0]
		if usr == '<Return>':
			return
		return userids[usr]


	def _players(self, srv):
		pout = dict(self.rconexec(srv, 'RefreshList'))['PlayerList']
		return pout
		#pout = pout.split('{\n\t"PlayerList": [')[1]
		#pout = pout.split('\t]\n}')[0]
		##print(pout)
		#_players = {}
		#for blk in pout.split('}'):
		#	useruid = [l.strip() for l in blk.rstrip('}').split('\n') if l.strip() and l.strip() not in (',', '{')]
		#	if not useruid or str(useruid).strip() == '[\']\']': continue
		#	#print(useruid)
		#	_players[useruid[0].split('": "')[1].rstrip('",')] = useruid[1].split('": "')[1].rstrip('"')
		#return _players

	def _getresponse(self, socket):
		res = []
		while True:
			ret = socket.recv(1024)
			res.append(ret.decode())
			if len(ret) <= 1023:
				break
		return ''.join(res)

	def _send(self, srv, data):
		passwd = self.servers[srv][0]
		server, port = srv.split(':')
		socket = sock(AF_INET, SOCK_STREAM)
		socket.settimeout(3)
		socket.connect((server, int(port)))
		socket.sendall(''.encode())
		auth = self._getresponse(socket)
		socket.sendall(passwd.encode())
		auth = self._getresponse(socket)
		if str(auth).strip() != 'Authenticated=1':
			error('authentication failure')
		if self.dbg:
			print(bgre(auth))
		res = {}
		try:
			socket.sendall(data.encode())
			res = self._getresponse(socket)
			if res:
				res = jload(res)
		except JSONDecodeError as err:
			pass
		except TimeOutError:
			self.cnt += 1
			if self.cnt <= 3:
				print('we ran into a timeout wile executing "%s", retrying...'%data)
				res = self._send(srv, data)
			print('we ran into a timeout wile executing "%s", aborting...'%data)
		finally:
			socket.close()
		return res

	def rconexec(self, srv, cmd):
		if self.dbg:
			print(bgre('%s %s'%(srv, cmd)))
		res = self._send(srv, cmd)
		if res and cmd == 'ServerInfo':
			res = res['ServerInfo']
			res['MapName'] = self._getmapname(res['MapLabel'])
			__maps = self._getmaps(srv, True)
			if __maps:
				res['MapList'] = __maps
		if isinstance(res, dict):
			res = dict((k, v) for (k,v) in sorted(res.items()))
		return res


	#def default(self, line):
	#       if line == 'Disconnect':
	#               self.socket.close()
	#               self._login()
	#       else:
	#               out = self._send(line)

def config(cfg):
	with open(cfg, 'r') as cfh:
		return yload(cfh.read(), Loader=Loader)

def cli(cfgs):
	app = PavlovADM(**cfgs)
	app.cmdloop()


def main():
	__me = 'pavlovadm'
	__dsc = '%s <by d0n@janeiskla.de> manages pavlov servers commands via it\'s rcon like admin interface'%__me
	cfgdir = expanduser('~/.config/%s'%__me)
	cacdir = expanduser('~/.cache/%s'%__me)
	try:
		makedirs(cfgdir)
	except FileExistsError:
		pass
	try:
		makedirs(cacdir)
	except FileExistsError:
		pass
	src = expanduser('~/.local/share/pavlovadm')
	lsrc = '/usr/local/share/pavlovadm'
	if not isdir(src):
		src = lsrc
	if isdir(src):
		for f in ('%s/pavlovadm.conf'%src, '%s/Game.ini'%src, '%s/public.ini'%src, '%s/BalancingTable.csv'%src):
			if not isfile(f):
				f = '%s/%s'%(lsrc, basename(f))
				if not isfile(f):
					continue
			if not isfile('%s/%s'%(cfgdir, basename(f))):
				with open(expanduser(f), 'r') as lfh, open('%s/%s'%(cfgdir, basename(f)), 'w+') as gfh:
					gfh.write(lfh.read())
	cfgs = config('%s/%s.conf'%(cfgdir, __me))

	pars = ArgumentParser(description=__dsc)
	pars.add_argument(
        '--version',
        action='version', version='%s v0.13'%__me)
	pars.add_argument(
        '-D', '--debug',
        dest='dbg', action='store_true', help='enable debugging')
	args = pars.parse_args()
	if args.dbg:
		cfgs['dbg'] = True
	cli(cfgs)


if __name__ == '__main__':
	main()
