#! /usr/bin/env python3

import os, sys, time, re
from utilities import tokenize, runProgram, exitShell

""" The following is based on:
	-) https://github.com/robustUTEP/os-demos/blob/master/ch5-api/p3-exec.py
	-) https://brennan.io/2015/01/16/write-a-shell-in-c/
"""

# set the status an impossibly large number as an initial start
status = sys.maxsize
args = ''

while True:
	args = tokenize(' ', input("$ "))

	if args[0] == 'exit':
		exitShell(args)

	elif args[0] == 'pwd':
		os.write(1, (os.getcwd()+'\n').encode())
		continue

	elif len(args) == 1 and args[0] == '':
		os.write(2, ("No input\n").encode())
		continue
	else:
		# if succesful status is set to 1
		status = runProgram(args)
	# if runProgram is not successful stop the show
	if not status is 1:
		break
