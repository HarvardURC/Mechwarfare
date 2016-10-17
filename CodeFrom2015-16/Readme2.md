# Mechwarfare
Code for running the controller(server) and robot(client) of the HURC Mechwarfare 2015-2016 robot

## How it works
The client side has stored arrays, which describe each of the servo movement sequences needed to make the robot walk and turn. The client side listens in for commands from the server via Xbee communications. When it gets a command, it executes the sequence of movements corresponding to the command.

The server side polls a Nintendo Wii Nunchuck for input and when the input passes some threshold (a button is pressed or the joystick is moved far enough), it sends a command to the client.
