# Tic-Tac-Toe

A terminal Tic-Tac-Toe over the network.

Two instances must be started:
- Server: ```./tictactoe.py -s -h REMOTE_HOSTNAME -p REMOTE_PORT```
- Client: ```./tictactoe.py -h REMOTE_HOSTNAME -p REMOTE_PORT```


# Usage
```
usage: tictactoe.py [-h] [-s] [-p PORT] --host HOST

The command line Tic-Tac-Toe Game

optional arguments:
  -h, --help            show this help message and exit
  -s, --server          Is this instance the server?
  -p PORT, --port PORT  port number
  --host HOST           hostname

```
