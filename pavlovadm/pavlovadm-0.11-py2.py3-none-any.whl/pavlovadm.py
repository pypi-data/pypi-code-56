#!/usr/bin/env python3

from os import environ

from os.path import expanduser

from socket import \
    socket as sock, \
    timeout as TimeOutError, \
    SOCK_DGRAM, SHUT_WR, \
    AF_INET, SOCK_STREAM

from argparse import ArgumentParser

from yaml import load as yload, dump as ydump, Loader, Dumper

from time import sleep

try:
    import readline
except ModuleNotFoundError:
    pass

from requests import post

from inquirer import prompt, List as iList

from cmd import Cmd

from discord import Client as DiscordClient

from discord.ext import commands


class PavlovADM(Cmd):
	servers = {}
	socket = sock(AF_INET, SOCK_STREAM)
	socket.settimeout(3)
	gameini = ''
	itemtbl = ''
	maptbl = '~/.cache/pavlovadm/maps.tbl'
	mapnames = {}
	maps = {}
	hlp = None
	cnt = 0
	srv = None
	def __init__(self, *args, **kwargs):
		self.use_rawinput = False
		for (k, v) in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
		super().__init__()
		try:
			self.serverselect()
		except IndexError as err:
			print('\033c')
			print('known index error occured, restarting')
			self.serverselect()

	def serverselect(self):
		if not self.srv:
			self.srv = self._login()
		if not self.hlp:
			while True:
				hlp = self._send('Help')
				if hlp:
					break
			self.hlp = hlp
		#print(self.servers)
		cmd = self._cmdselects()
		self._send('\n', False)
		if cmd is None:
			return self.serverselect()
		elif not cmd:
			print('unexpectedly received %s from prompter as command - retrying...'%cmd)
			return self.serverselect()
		res = self.fire(cmd.strip('<>'))
		if res:
			print(res)
		if cmd == '<Disconnect>':
			self.socket.close()
			self.srv = None
			self.maps = {}
			self.socket = sock(AF_INET, SOCK_STREAM)
		self.serverselect()

	def _login(self):
		"""server login method"""
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
		passwd = self.servers[srv][0]
		if len(self.servers[srv]) > 1:
			maplist = self.servers[srv][1]
		server, port = srv.split(':')
		self.socket.connect((server, int(port)))
		self._send('')
		print(self._send(passwd))
		return srv
		#self.prompt = '%s:%s >'%(server, port)

	def _getmapname(self, mapid):
		if mapid in self.mapnames:
			return self.mapnames[mapid]
		url = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
		res = requests.post('%s%s'%(url, mapid.strip('UGC')))
		for l in res.text.split('\n'):
			if 'workshopItemTitle' in l:
				return l.split('>')[1].split('<')[0]

	def _getmaps(self, noask=None):
		if not self.maps:
			maplst = self.gameini
			if len(self.servers[self.srv]) > 1:
				maplst = self.servers[self.srv][1]
			if maplst.startswith('~'):
				maplst = expanduser(maplst)
			if not maplst.startswith('/'):
				print('error: cannot read maplist if no absolute path is provided')
			with open(maplst, 'r') as mfh:
				lines = mfh.readlines()
			with open(expanduser(self.maptbl), 'r') as mfh:
				self.mapnames = yload(mfh.read(), Loader=Loader)
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
			if noask: return
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

	def _cmdselects(self):
		noargs = ['Info', 'ResetSND', 'RefreshList', 'RotateMap', 'ServerInfo', 'Help', '<Disconnect>']
		steams = ['Kick', 'Ban', 'Unban', 'InspectPlayer']
		others = ['SwitchMap', 'SwitchTeam', 'GiveItem', 'GiveCash', 'GiveTeamCash', 'SetPlayerSkin', 'SetLimitedAmmoType']
		order = ['Info', 'SwitchMap', 'RotateMap', 'ResetSND', 'Kick', 'Ban', 'Unban', 'InspectPlayer', 'GiveItem', 'GiveCash', 'GiveTeamCash', 'SetPlayerSkin', 'SetLimitedAmmoType', 'RefreshList', 'ServerInfo', '<Disconnect>']
		try:
			hlp = self.hlp.strip().strip('{}').split('": "')[1].strip().rstrip('"')
		except IndexError as err:
			print('index error occoured while interpreting %s - restarting...'%hlp)
			return self._cmdselects()
		hlp = [h.split(' ')[0] for h in hlp.split(', ') if h.split(' ')[0] != 'Disconnect'] + ['<Disconnect>']
		ask = [
            iList(
                'cmd',
                carousel=True,
                message='select command',
                choices=order,
            ),
        ]
		cmd = list(prompt(ask).values())[0].strip()
		if cmd in noargs:
			return cmd
		elif cmd in steams:
			sid = self._getsteamid(cmd)
			#print(sid)
			if not sid:
				return
			return '%s %s'%(cmd, sid)
		elif cmd in others:
			if cmd == 'SwitchMap':
				mapmod = self._getmaps()
				if not mapmod:
					return
				return 'SwitchMap %s'%mapmod
			elif cmd == 'SwitchTeam':
				sid = self._getsteamid(cmd)
				if not sid:
					return
				return 'SwitchTeam %s %s'%(sid, self._getteam())
			elif cmd == 'GiveItem':
				sid = self._getsteamid(cmd)
				if not sid:
					return
				return 'GiveItem %s %s'%(sid, self._getitem())
			elif cmd == 'GiveCash':
				sid = self._getsteamid(cmd)
				if not sid:
					return
				return 'GiveCash %s %s'%(sid, self._getcash())
			elif cmd == 'GiveTeamCash':
				team = self._getteam()
				if not team:
					return
				return 'GiveTeamCash %s %s'%(team, self._getcash())
			elif cmd == 'SetPlayerSkin':
				sid = self._getsteamid(cmd)
				if not sid:
					return
				return 'SetPlayerSkin %s %s'%(sid, self._getskin())
			elif cmd == 'SetLimitedAmmoType':
				ammo = self._getammotype()
				if not ammo:
					return
				return 'SetLimitedAmmoType %s'%ammo

	def _getsteamid(self, cmd):
		userids = self._players()
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

	def fire(self, cmd):
		#print(cmd)
		if cmd == 'Info':
			if not self.maps:
				self._getmaps(True)
			print('\n'.join('%s %s'%(k, v) for (k, v) in self.maps.items()))
			print(self._send('ServerInfo'))
			print(self._send('RefreshList'))
			return
		res = self._send(cmd)

	def _players(self):
		pout = self._send('RefreshList')
		pout = pout.split('{\n\t"PlayerList": [')[1]
		pout = pout.split('\t]\n}')[0]
		#print(pout)
		_players = {}
		for blk in pout.split('}'):
			useruid = [l.strip() for l in blk.rstrip('}').split('\n') if l.strip() and l.strip() not in (',', '{')]
			if not useruid or str(useruid).strip() == '[\']\']': continue
			#print(useruid)
			_players[useruid[0].split('": "')[1].rstrip('",')] = useruid[1].split('": "')[1].rstrip('"')
		return _players

	def _getresponse(self):
		res = []
		while True:
			ret = self.socket.recv(1024)
			res.append(ret.decode())
			if len(ret) <= 1023:
				break
		return ''.join(res)

	def _send(self, data, answer=True):
		try:
			self.socket.sendall(data.encode())
			if answer:
				res = self._getresponse()
				if not res:
					self.socket.sendall('\n'.encode())
					res = self._getresponse()
				if res:
					return res
		except TimeOutError:
			print('we ran into a timeout wile executing "%s"'%data, end='')
			self.cnt += 1
			if self.cnt <= 3:
				print(' retrying...')
				return self._send(data, answer)
			print(' aborting...')
	#def default(self, line):
	#       if line == 'Disconnect':
	#               self.socket.close()
	#               self._login()
	#       else:
	#               out = self._send(line)





class MatchMaker(DiscordClient):
	dbg = False
	lad = None
	def __init__(self, lad):
		super().__init__()
		self.lad = lad
		self.ladlst = pjoin(expanduser('~'), '.cache', 'pamm', '%son%s.lst'%(lad, lad))
		if not isdir(dirname(self.ladlst)):
			makedirs(dirname(self.ladlst))
		if self.dbg:
			print(bgre(MatchMaker.__mro__))
			print(bgre(tabd(MatchMaker.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))

	@property                # ladder <rw>
	def ladder(self):
		if not isfile(self.ladlst):
			with open(self.ladlst, 'w+') as lfh:
				lfh.write('{}')
		with open(self.ladlst, 'r') as lfh:
			return yload(lfh.read(), Loader=Loader)
	@ladder.setter
	def ladder(self, val):
		with open(self.ladlst, 'w+') as lfh:
			lfh.write(ydump(val))

	def matcher(self, seek={}):
		sids = list(seek.keys())
		match = None
		mmatch = []
		smatch = None
		if not self.ladder and not sids:
			return False
		if not self.ladder:
			self.ladder = seek
			return None
		_lad = self.ladder
		if len(sids) == 0:
			return None
		sid = sids[0]
		maps = seek[sid]['maps']
		skil = int(seek[sid]['skill'])
		_lad[sid] = {'maps': maps, 'skill': skil}
		for (k, vs) in _lad.items():
			if k == sid:
				continue
			for m in vs['maps']:
				if m in maps:
					mmatch.append(m)
			if not mmatch:
				break
			vsk = int(vs['skill'])
			if vsk == skil or vsk+1 == skil or vsk-1 == skil:
				match =  {k: {'maps': mmatch[:3], 'skill': smatch}, sid: {'maps': mmatch[:3], 'skill': skil}}
				try:
					del _lad[k]
					del _lad[sid]
				except KeyError:
					pass
				break
		self.ladder = _lad
		return match

	async def on_message(self, chat):
		msg = chat.content
		await chat.create_dm()
		if str(msg).startswith('/help'):
			print()
		if str(msg).startswith('/list'):
			print()
		if str(msg).startswith('/unregister'):
			print()
		if str(msg).startswith('/search'):
			await chat.dm_channel.send('trying to find match for %s'%(' '.join(m for m in str(msg).split(' ')[1:])))


def config(cfg):
	with open(cfg, 'r') as cfh:
		return yload(cfh.read(), Loader=Loader)

def cli(cfgs):
	app = PavlovADM(**cfgs)
	app.cmdloop()

def discordbot(cfgs):
	token = cfgs['bot']['token']
	server = cfgs['bot']['server']
	environ['DISCORD_TOKEN'] = token
	environ['DISCORD_GUILD'] = server
	client = MatchMaker()
	client.run(token)


def main():
	__me = 'pavlovadm'
	__dsc = '%s <by d0n@janeiskla.de> manages pavlov servers commands via it\'s rcon like admin interface'%__me
	cfgs = config(expanduser('~/.config/%s/%s.conf'%(__me, __me)))
	pars = ArgumentParser(description=__dsc)
	pars.add_argument(
        '--version',
        action='version', version='%s v0.1'%__me)
	pars.add_argument(
        '--discobot',
        action='store_true', help='start the discord bot insted of rcon tool')
	args = pars.parse_args()
	if args.discobot:
		discordbot(cfgs)
		exit()
	cli(cfgs)


if __name__ == '__main__':
	cli()
