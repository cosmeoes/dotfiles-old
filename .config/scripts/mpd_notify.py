#!/usr/bin/env python

"""Notifies the user when MPD changes

This script polls mpd and sends out a notification using either pynotify or notify-send whenever either the status of
MPD changes or if a new song is being played. In general, it should work fine without any modifications.
Just run it with python mpd-notify.py. If that doesn't work, read on.

Specify the cover art folder, where downloaded cover images will be
stored, below. You can use pycoverart (http://pycoverart.googlecode.com/svn/trunk/cover_art.py) to download cover art
for your whole collection if necessary, otherwise, this script will download them when needed. If you want to copy the
art to a particular file location - to display it in conky, for example - you can specify a path to that file on line
101.

Note: The daemonizer apparently doesn't work for everyone. If this is the case for you, uncomment line 58
Dependencies:
    - python-mpd
    - python-notify (Optional but highly recommended)
    - python-imaging (Only for conky support)

Get the latest version of the script here: http://mpd.wikia.com/wiki/Hack:mpd-notify.py"""

from __future__ import print_function
import os
import time
import sys
import socket
import glob
import mpd

__author__ = "Durand D'souza"
__email__ = "durand1 [at] gmail [dot] com"
__credits__ = ["Durand D'souza",
               ("Patrick Hirt", "patrick [dot] hirt [at] gmail [dot] com"),
               ("Henning Hollermann", "laclaro [at] mail [dot] com")]
__version__ = "28/07/12"
__license__ = "GPL v3"

# MPD settings
MPD_HOST = "localhost"
MPD_PORT = 6600

# Time to wait in seconds between checking mpd status changes
POLLING_INTERVAL = 0.5
# Time to wait in seconds between checking for mpd existing
SLEEP_INTERVAL = 5

def sanitize(name):
    """Replaces disallowed characters with an underscore"""
    ## Disallowed characters in filenames
    DISALLOWED_CHARS = "\\/:<>?*|"
    if name == None:
        name = "Unknown"
    for character in DISALLOWED_CHARS:
        name = name.replace(character,'_')
    # Replace " with '
    name = name.replace('"', "'")

    return name

def send_notification(summary, message="", icon=None, update=True):
    """This function takes information and sends a notification to the notification daemon using pynotify or
    notify-send. If update is set to False, a new notification will be created rather than updating the previous one"""
    os.popen('notify-send "{1}" "{0}" -a music.py'.format(summary.replace('"', '\\"'), message.replace('"', '\\"')))

def observe_mpd(client):
    """This is the main function in the script. It observes mpd and notifies the user of any changes."""
    # Loop and detect mpd changes
    last_status = "Initial"
    last_song = "Initial"

    while True:
        # Get status
        current_status = client.status()['state']
        # There might be errors when getting song details if there is no song in the playlist
        try:
            current_song = client.currentsong()['file']
            # Get song details
            artist = client.currentsong()['artist']
            album = client.currentsong()['album']
            title = client.currentsong()['title']
        except KeyError:
            current_song, artist, album, title = ("", "", "", "")

        # If the song or status has changed, notify the user
        if current_status != last_status and last_status != "Initial":
            if current_status == "play": # Not sure how to make this one show in an efficient way so we won't bother
                pass # send_notification(summary="MPD", message="Playing", icon="media-playback-start")
            elif current_status == "pause":
                pass #send_notification(summary="MPD", message="Paused", icon="media-playback-pause")
            else: # Otherwise we assume that mpd has stopped playing completely
                send_notification(summary="MPD", message="Stopped", icon="media-playback-stop")

        if (current_song != last_song and current_song != "") or (current_status != last_status and current_status ==
                                                                  "play") and last_song != "Initial":
            send_notification(summary=artist, message=title, icon="", update=True)

        # Save current status to compare with later
        last_status = current_status
        last_song = current_song
        # Sleep for some time before checking status again
        time.sleep(POLLING_INTERVAL)

def run_notifier(self=None):
    """Runs the notifier"""
    # Initialise mpd client and wait till we have a connection
    while True:
        try:
            client = mpd.MPDClient()
            client.connect(MPD_HOST, int(MPD_PORT))
            # Run the observer but watch for mpd crashes
            observe_mpd(client)
        except KeyboardInterrupt:
            print("\nLater!")
            sys.exit()
        except (socket.error, mpd.ConnectionError):
            time.sleep(SLEEP_INTERVAL)


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    """Fork the notification daemon using an alternate method to daemon.py
    Contributed by Patrick Hirt"""
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
            sys.stderr.write('Fork #1 failed: (%d) %s\n' % (e.errno, e.strerror))
            sys.exit(1)

    os.chdir('/')
    os.umask(0)
    os.setsid()

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write('Fork #2 failed: (%d) %s\n' % (e.errno, e.strerror))
        sys.exit(1)

    for f in sys.stdout, sys.stderr:
        f.flush()
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

if __name__ == "__main__":
    if len(sys.argv) == 2:
       if sys.argv[1] == "daemonize":
           # If we don't use the daemon module, just use daemonize()
           daemonize()
           run_notifier()
       else:
           print("""Usage: {0} [daemonize]""".format(sys.argv[0]))

    else:
        run_notifier()
