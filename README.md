# revshell-py
reverse shell generator for HTB boxes

```
$ ./rev.py -h    
usage: rev.py [-h] [-l LHOST] [-p LPORT] [-b64] [--linux] [--windows]

Reverse Shell Generator (Linux & Windows) with Base64 Encoding

options:
  -h, --help         show this help message and exit
  -l, --LHOST LHOST  Listen host IP
  -p, --LPORT LPORT  Listen port
  -b64               Base64 encode the output
  --linux            Show Linux payloads only
  --windows          Show Windows payloads only
```
