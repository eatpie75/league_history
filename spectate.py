#!/usr/bin/env python
import os
import subprocess
import sys
import _winreg


args=sys.argv[1]
options={}
for arg in args.replace('lolspectate://', '').split('&'):
	tmp=arg.split('=')
	options[tmp[0]]=tmp[1]
print options

reg=_winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
key=_winreg.OpenKey(reg, r'SOFTWARE\Riot Games\RADS')
path=os.path.normpath(_winreg.EnumValue(key, 0)[1])
reg.Close()
key.Close()
# "0.0.0.159", "deploy"
launcherbase=os.path.join(path, "solutions", "lol_game_client_sln", "releases")
# "0.0.0.152", "deploy", "LolClient.exe"
clientbase=os.path.join(path, "projects", "lol_air_client", "releases")
launcher=os.path.join(launcherbase, sorted(os.listdir(launcherbase), key=lambda val:val.split('.')[-1], reverse=True)[0], "deploy")
client=os.path.join(clientbase, sorted(os.listdir(clientbase), key=lambda val:val.split('.')[-1], reverse=True)[0], "deploy", "LolClient.exe")
os.chdir(launcher)
subprocess.call([os.path.join(launcher,"League of Legends.exe"), '8394', 'LoLLauncher.exe', client, "spectator {}:{} {} {} {}".format(options['ip'], options['port'], options['key'], options['game_id'], options['region'])])
