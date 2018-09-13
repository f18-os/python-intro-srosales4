import os, sys

rc = 1
pid = os.getpid()
command = "tixe"

os.write(1, ("About to fork (pid:%d)\n" % pid).encode() )
rc = os.fork()

if rc < 0:
	os.write(2, ("fork failed, returning %d\n" % rc).encode() )
	sys.exit(1)
elif rc == 0:
	os.write(1, ("I'm a child. My pid==%d. Parent's pid==%d\n" % (os.getpid(), pid) ).encode() )

	# while (command != "exit"):
	# 	# raw_input was renamed to input http://docs.python.org/dev/py3k/whatsnew/3.0.html
	# 	command = input("minersh:: ")
	# 	command.strip()
	# 	userInput = command.split(" ")

	# 	if userInput[0] != "":
	# 		os.write(1, ("About to exit (pid:%d)\n" % pid).encode() )
	# 		rc = os.exit()
	command = input('type something:: ')
	if command == "\0":
		os.write(1, ("About to fork (pid:%d)\n" % pid).encode() )
		rc = os.fork()
		os.wait()

else:
	os.write(1, ("I'm a parent. My pid==%d. Parent's pid==%d\n" % (pid, rc) ).encode() )

	command = input('minersh::')
	command.strip()

	if command == "\0":
		os.write(1, ("About to fork (pid:%d)\n" % pid).encode() )
		rc = os.fork()
		os.wait()

# while (command != "exit"):
# 	command = input('minersh::\n')
# 	userInput = command.split(" ")

	# QUESTION: Do we fork before or after we find the program?


	# if ".py" in userInput[0]:
	# 	pythonFile = userInput[0]
	# 	io = 'python3 %s %s %s' % (pythonFile, userInput[1], userInput[2])
	# 	os.system(io)
	# elif "." not in userInput[0]:
	# 	os.system(command)


# "wordCount.py testFile.txt myOutput.txt"
# "cat wordCount.py"

# METHODS FOR SHELL API
