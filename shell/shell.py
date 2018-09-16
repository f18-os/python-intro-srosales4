#! /usr/bin/env python3

# The following code is CV'd from:
# https://github.com/robustUTEP/os-demos/blob/master/ch5-api/p4-redirect.py

# TODO: read: https://stackoverflow.com/questions/4204915/please-explain-the-exec-function-and-its-family#4205020 TDTDTDTDTDTDTDTD
# To get another viewpoint on the topics of fork() and exec() read:

import os, sys, time, re
from wordCount import tokenize

pid = os.getpid()               # get and remember pid

os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

rc = os.fork()

if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:

    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), pid)).encode())

    for dir in re.split(':', os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, tokens[0])
        os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
        try:
            os.execve(program, tokens[1:], os.environ) # try to exec program
            os.wait()
        except OSError as e:                      # ...expected
            os.write(2, ("%s\n" % e).encode() )
            pass                                       # ...fail quietly

else:                           # parent (forked ok)
    childPidCode = os.wait()
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())

    command = ""
    while command != "exit":
        command = input('$ ')
        tokens = tokenize(' ', command)

        # Not sure if I even need this line???
        if tokens[0] == '':
            break
        os.write(1, ("%s\n" % tokens).encode() )

    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())