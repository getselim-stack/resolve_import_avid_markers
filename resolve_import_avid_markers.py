#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This Script imports markers to DaVinci Resolve
# from a txt file exported by avid
#
# Tested on a txt file generated by Media Composer v2018.11
# Iddos, Bootqe color studio, iddolahman@gmail.com

import sys, os, re
from tkinter import Tk, filedialog, messagebox
from python_get_resolve import GetResolve

Tk().withdraw()

markersFile = filedialog.askopenfilename()
if not markersFile or not os.path.splitext(markersFile)[1] == '.txt':
    sys.exit(0)

pattern = r'(^.+)(\d{2}:\d{2}:\d{2}:\d{2}).*\s.*\s.*\t(.+)1'

def messageWindow(message):
	"""message window and exit"""
	messagebox.showinfo('Resolve Import Markers', message)
	sys.exit(0)

def timecode2frames(timecodeString, fps):
    """
    Takes a timecode string and integer framerate returns integer frame count
    """
    return sum(f * int(t) for f, t in zip((0, 60*fps, fps, 1),\
                                   timecodeString.split(':')))

def main():
    """
    Initiate resolve instance, get timeline and framerate
    Open and parse text file
    Apply markers to timeline
    Close file and save project
    """
    resolve = GetResolve()

    if resolve == None:
        messageWindow('Please open Resolve and select a timeline')

    projectManager = resolve.GetProjectManager()
    currentProject = projectManager.GetCurrentProject()
    currentTimeline = currentProject.GetCurrentTimeline()

    if currentTimeline == None:
        messageWindow('Please select a timeline')

    fps = int(float(currentProject.GetSetting('timelineFrameRate')))

    with open(markersFile, 'r') as infile:
        for line in infile:
            matches = re.search(pattern, line)
            tc = timecode2frames(matches.group(2), fps)
            title = matches.group(3)
            user = matches.group(1)
            apply = currentTimeline.AddMarker(tc, 'Blue', title, user, 1)

    infile.close()
    projectManager.SaveProject()

if __name__ == '__main__':
    main()
