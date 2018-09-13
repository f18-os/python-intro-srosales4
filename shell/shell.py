#! /usr/bin/env python3

# The following code is CV'd from:
# https://github.com/robustUTEP/os-demos/blob/master/ch5-api/p4-redirect.py

# TODO: read: https://stackoverflow.com/questions/4204915/please-explain-the-exec-function-and-its-family#4205020 TDTDTDTDTDTDTDTD
# To get another viewpoint on the topics of fork() and exec() read:

import os, sys, time, re

pid = os.getpid()               # get and remember pid

os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

rc = os.fork()

if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
    
    while True:
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                     (os.getpid(), pid)).encode())
        args = input('minersh:: ')
        tokens = args.split(' ')

        for dir in re.split(':', os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, tokens[0])
            try:
                os.execve(program, tokens[1:], os.environ) # try to exec program
            except OSError as e:                      # ...expected
                os.write(2, ("%s\n" % e).encode() )
                pass                                       # ...fail quietly

        # for dir in re.split(":", os.environ['PATH']): # try each directory in path
        #     program = "%s/%s" % (dir, tokens[0])
        #     try:
        #         os.execve(program, tokens[1:], os.environ) # try to exec program
        #     except FileNotFoundError:             # ...expected
        #         pass                              # ...fail quietly


    # !!!!!!!!!!!   WHAT DOES THIS LINE DO?   !!!!!!!!!!!!!!!!!!!!!
    #os.close(1)                 # redirect child's stdout

    #sys.stdout = open("shell-output.txt", "w")

    # !!!!!!!!!!!   WHAT DO THESE TWO LINES DO?   !!!!!!!!!!!!!!!!!!!!!
    #fd = sys.stdout.fileno() # Oh!!!  I think this line looks for the lowest fd that's available
    #os.set_inheritable(fd, True)  # TODO: I need to look up what this func does TDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTD

    
    #os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    #sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
    childPidCode = os.wait()
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())