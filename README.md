# bind-shell-python
This is a basic bind shell script in python 2 , containing both server and client classes. This bind shell can work on both Windows and Linux OS.

## Server Mode

Server mode of script should be started at victim machine by executing bellow commands in terminal of victim machine:<br />
  `python shaker.py server [port to bind]` <br />
This will open specified port and listen for incoming shell commands from a user running this script in Client mode.

## Client Mode

Client mode od script should be used to communicate with victim machine running this script in server mode , inshort, we can run this script in client mode to communicate with device running this bind shell in server mode.<br />
Two things we should know before running this script in client mode are :<br />
1. IP of victim machine.
2. Port on which this bind shell is running.<br />
Run bellow terminal command to start client mode :<br />
  `python shaker.py client [port on which bind shell is running] [IP of victim machine]`<br />
This will connect with the victim machine

## Stoping Server Mode From Client Side

Now we have the shell and want to shut the bind shell running on victim machine, then we just have to type "exit" on running shell at client side . It will stop the script on victim side and port will go free. So there will be no traces that somebody bind the port. Many a time people don't know how to shut the bind port off , this script will do this for you. <br />

If any issues or comments connect with me at twitter @_j0lt 
