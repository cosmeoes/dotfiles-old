import os, sys
from subprocess import Popen, PIPE
ops = sys.argv
value = ops[2]
current = os.popen('cat /sys/class/backlight/radeon_bl0/brightness').read()

if(ops[1]=='-dec'):
	value= int(value)*-1

new = int(current) + int(value)
if(new > 255):
	new=255
elif(new < 10):
	new = 10
os.system("tee /sys/class/backlight/radeon_bl0/brightness <<< "+ str(new))
