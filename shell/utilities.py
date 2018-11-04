import argparse
import os, sys, time, re

""" The following is based on:
	-) https://brennan.io/2015/01/16/write-a-shell-in-c/
"""

def tokenize(symbol, stringInput):
	# attempt to open input file

    tokens = re.compile('\W')
    listOfTokens = stringInput.split(symbol)

    return listOfTokens


def runProgram(args):
	pid = os.getpid()

	os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
	rc = os.fork()

	if rc < 0:
		os.write(2, ("fork failed, returning %d\n" % rc).encode())
		sys.exit(-1)

	elif rc == 0:
		os.write(1, ("Child: My pid==%d. Parent's pid==%d\n" % 
					(os.getpid(), pid)).encode())

		if execProgram(args) == -1:
			os.write(2, ("error in utilities, runProgram, rc == 0\n").encode())
			return -1

	else:
		childPIDcode = os.wait()
		os.write(1, ("Parent: My pid=%d. Child's pid=%d\n" %
					(pid, rc)).encode())
		os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
					childPIDcode).encode())

	return 1


def execProgram(args):
	for dir in re.split(":", os.environ['PATH']):
		programPath = "%s/%s" %(dir, args[0])
		os.write(1, ("runProgram: exec-ing %s\n" % programPath).encode())
		try:
			if len(args) == 1:
				os.execv(programPath, args)
			else:
				os.execve(programPath, args[1:], os.environ)
				os.write(1, ("next line after exec").encode())
		except FileNotFoundError:
			pass

	# else something went wrong
	os.write(2, ("command not found: %s\n" % args[0]).encode())
	# and return -1 to signal an error
	return -1

def exitShell(args):
	sys.exit(0)

def getWorkingDirectory():
	os.getcwd()

# def changeDirectory(path):

