# Bind Shell in Python 3

A simple and educational Python 3-based bind shell script that supports both **server** and **client** modes. Compatible with both **Linux** and **Windows** systems.

> ⚠️ **Disclaimer:** This tool is for **educational purposes only**. Unauthorized use on systems you do not own or have explicit permission to test may be illegal.

---

## Features

- ✅ Python 3 compatible
- ✅ Works on Windows and Linux
- ✅ Simple and readable structure
- ✅ Clean shutdown support with `exit` command
- ✅ Sends current directory with every response

---

## Usage

### Server Mode

Start the server on the target/victim machine:

```
python3 shaker.py server [port]
```
* Listens on all interfaces (0.0.0.0) for incoming connections.
* Executes commands sent from the client and returns output.

###Client Mode
Start the client to control the remote machine:
```
python3 shaker.py client [port] [server_ip]

```
**You need**:

* IP address of the machine running the server.
* Port on which the server is listening.

Once connected:

* You will get a shell prompt.
* Type shell commands and receive output.
* Type `exit` to shut down the server and end the session.

### Shutting Down the Server

To stop the bind shell cleanly:

* From the client session, type:
`exit`
- This will:
  - Terminate the server process.
  - Release the bound port.
  - Leave minimal traces.

## Contact

Have questions or suggestions? Reach out to @_j0lt on Twitter.

© This script is meant for ethical hacking and learning. Always get proper authorization.

