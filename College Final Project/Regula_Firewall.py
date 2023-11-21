import os
import subprocess
import json

# Script amplasat la nivelul serverului care:
# - Citeste IP-urile periculoase din fisierele primite
# - Construieste reguli de firewall inbound si outbound pentru a bloca IP-urile respective
director = r'C:\inetpub\FTP_Main_Site'
for fisier in os.walk(director):
    if fisier[2]:
        os.chdir(fisier[0])
        with open(fisier[2][2], 'rt') as f:
            dictionar = json.load(f)
            for cheie in dictionar.keys():
                subprocess.call(f'netsh advfirewall firewall add rule name = "Block IP Address - {cheie}" dir = in action = block remoteip = {cheie}')
                subprocess.call(f'netsh advfirewall firewall add rule name = "Block IP Address - {cheie}" dir = out action = block remoteip = {cheie}')
