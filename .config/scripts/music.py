import os, sys
from subprocess import Popen, PIPE 

action = sys.argv[1]
mpc_output = os.popen("mpc %s" % action).read()
status = mpc_output.split("\n")
if(status[1].startswith("[paused]")):
    sys.exit()
song_and_artist = status[0].split(" - ")
song = song_and_artist[1].replace("&", "$amp")
artist = song_and_artist[0].replace("&", "$amp")
os.popen('notify-send -a music.py "%s" "%s"' % (song, artist))
