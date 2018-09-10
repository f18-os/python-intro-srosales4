import os, sys

command = ""

while (command != "exit"):
	command = input('minersh::\n')
	userInput = command.split(" ")

	if ".py" in userInput[0]:
		program = userInput[0]
		io = 'python3 %s %s %s' % (program, userInput[1], userInput[2])
		os.system(io)
	elif "." not in userInput[0]:
		os.system(command)
