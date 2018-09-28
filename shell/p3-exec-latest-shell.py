#! /usr/bin/env python3

import os, sys, time, re
from wordCount import tokenize

# The following code is CV'd from:
# https://github.com/robustUTEP/os-demos/blob/master/ch5-api/p3-exec.py

# Still needs work:
# 	-) The child finds the program and does the execve() call.  The problem
#	   is that this code as is, will execve() and then return to the parent,
#	   the parent, which then continues after the os.wait() line.
#	-) I cannot get the child to loop for a prompt.
#	-) I need to figure out a better way to pass args into the execve() call

global argTokens
argTokens = []

pid = os.getpid()
args = input("$ ")
argTokens = tokenize(' ', args)

os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
rc = os.fork()

if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
	
	os.write(1, ("Child: My pid==%d. Parent's pid==%d\n" % (os.getpid(), pid)).encode())
	# global args = ["wc", "p3-exec-latest-shell.py"]
	for dir in re.split(":", os.environ['PATH']): # try each directory in the path
		program = "%s/%s" % (dir, argTokens[0])
		os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
		try:
			# os.write(1, (args).encode() )
			# I got the call to work by making the 2nd arg a weird 
			# list but eventually I need to be more elegant about this
			os.execve(program, argTokens[1:], os.environ) # try to exec program
		except FileNotFoundError:				 # ...expected
			pass 								 # ...fail quietly
	os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
	sys.exit(1)					# terminate with error
else:                           # parent (forked ok)

    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
    childPidCode = os.wait()
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())
