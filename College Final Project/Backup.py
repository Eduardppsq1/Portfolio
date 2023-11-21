### GUI

from tkinter import *
from Captura import *


lista_pachete = []
c = Captura()

root = Tk()
root.title("Proiect captură de pachete și detecție de DoS")
root.geometry("450x490")

label_interfata = Label(text='Interfață',
              font=("Calibri Bold",12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )
label_interfata.grid(row=0, column=0)

entry_interfata = Entry(bg='white', fg='black')
entry_interfata.grid(row=0, column=1)

label_filtru = Label(text='Filtru',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )
label_filtru.grid(row=1, column=0)

entry_filtru = Entry(bg='white',fg='black')
entry_filtru.grid(row=1, column=1)

label_nr_pachete = Label(text='Număr Pachete',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )

label_nr_pachete.grid(row=2, column=0)

entry_nr_pachete = Entry(bg='white',fg='black')
#entry_nr_pachete.insert(0,'20')
entry_nr_pachete.grid(row=2, column=1)


buton_captura = Button(root,
           command=lambda: c.capture(lista_pachete, entry_nr_pachete.get(), entry_interfata.get(), entry_filtru.get()),
           text='Start captură',
           font=("Arial Bold",14),
           bg="#33C9FF",
           fg="black",
           width=17,
           height=2
           )
buton_captura.grid(row=3,column=1)

label_path = Label(text='Cale Director',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )
label_path.grid(row=5,column=0)

entry_path = Entry(bg='white',fg='black')
entry_path.grid(row=5,column=1)

buton_save = Button(root,
                command = lambda: c.save(lista_pachete, entry_path.get()),
                text='Salvare date local',
                font=("Arial Bold",14),
                bg="yellow",
                fg="purple",
                width=17,
                height=2
                )
buton_save.grid(row=6,column=1)

buton_statistics = Button(root,
                command = lambda: c.show_stats(lista_pachete),
                text='Afișare statistici',
                font=("Arial Bold",14),
                bg="orange",
                fg="blue",
                width=17,
                height=2)
buton_statistics.grid(row=4,column=1)

######
label_IP_server = Label(text='IP Server',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )

label_IP_server.grid(row=7, column=0)

entry_IP_server = Entry(bg='white',fg='black')

entry_IP_server.insert(END, '192.168.83.128')

entry_IP_server.grid(row=7, column=1)

label_user_ftp = Label(text='Username FTP',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )

label_user_ftp.grid(row=8, column=0)

entry_user_ftp = Entry(bg='white',fg='black')

entry_user_ftp.insert(END, 'Eduard')

entry_user_ftp.grid(row=8, column=1)

label_parola_ftp = Label(text='Parolă FTP',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )

label_parola_ftp.grid(row=9, column=0)

entry_parola_ftp = Entry(show="*", bg='white', fg='black')

entry_parola_ftp.grid(row=9, column=1)

buton_ftp = Button(root,
                command = lambda: c.ftp_transfer(entry_IP_server.get(), entry_user_ftp.get(), entry_parola_ftp.get(), entry_path.get()),
                text='Transfer FTP',
                font=("Arial Bold",14),
                bg="pink",
                fg="green",
                width=17,
                height=2)

buton_ftp.grid(row=10,column=1)

buton_all = Button(root,
                command = lambda: c.show_stats(lista_pachete),
                text='Rulare automata',
                font=("Arial Bold",14),
                bg="brown",
                fg="white",
                width=17,
                height=2)

buton_all.grid(row=11,column=1)

root.mainloop()

### Captura

from Pachete import *
from scapy.all import sniff, sendp
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, ICMP
from getmac import get_mac_address
from datetime import datetime
from ftplib import FTP
import matplotlib.pyplot as plt
import os
import socket
import json

adresa_mac = get_mac_address()
host = socket.gethostname()
adresa_IP = socket.gethostbyname(host)
run = True

class Captura(object):
    _instance = None

    @staticmethod
    def getInstance():
        if Captura._instance == None:
            Captura()
        return Captura._instance

    def __init__(self):
        if Captura._instance != None:
            raise Exception("This class is a singleton!")
        else:
            Captura._instance = self

    @staticmethod
    def capture(lista_pachete, dictionar_final, nr_pachete, interfata=None, filtru=None):
        os.system('cls')
        lista_pachete.clear()
        dictionar_final.clear()
        d = {}
        id_pachet = 0
        timp_incepere = datetime.now()
        if nr_pachete == "":
            pachete = sniff(count=100, iface=interfata, filter=filtru)
        else:
            pachete = sniff(count=int(nr_pachete), iface=interfata, filter=filtru)
        timp_finalizare = datetime.now()
        delta_t = timp_finalizare-timp_incepere
        durata_capturarii = delta_t.seconds + delta_t.microseconds * 1e-6
        prag_nivel2 = 10*(delta_t.seconds + delta_t.microseconds * 1e-6)
        prag_nivel1 = 5*(delta_t.seconds + delta_t.microseconds * 1e-6)
        for i in pachete:
            id_pachet += 1
            if 'ARP' in i:
                p = Pachet_ARP(id_pachet, i['Ether'].dst, i['Ether'].src, i['ARP'].op)
                lista_pachete.append(p)
            elif 'IP' in i:
                if 'TCP' in i:
                    p = Pachet_TCP(id_pachet, i['Ether'].dst, i['Ether'].src, i['IP'].dst, i['IP'].src,
                               i['IP'].version, i['IP'].proto, i['TCP'].sport, i['TCP'].dport)
                    lista_pachete.append(p)
                elif 'UDP' in i:
                    p = Pachet_UDP(id_pachet, i['Ether'].dst, i['Ether'].src, i['IP'].dst, i['IP'].src,
                               i['IP'].version, i['IP'].proto, i['UDP'].sport, i['UDP'].dport)
                    lista_pachete.append(p)
                elif 'ICMP' in i:
                    p = Pachet_ICMP(id_pachet, i['Ether'].dst, i['Ether'].src, i['IP'].dst, i['IP'].src,
                               i['IP'].version, i['IP'].proto, i['ICMP'].type)
                    lista_pachete.append(p)
        for j in lista_pachete:
            try:
                ip_periculos = j.IP_src
                if ip_periculos != adresa_IP:
                    if ip_periculos in d.keys():
                        d[ip_periculos] += 1
                    else:
                        d[ip_periculos] = 1
            except AttributeError:
                continue
        for cheie in d.keys():
            if d[cheie] >= prag_nivel2:
                for p in lista_pachete:
                    if (type(p) != Pachet_ARP) and (p.IP_src == cheie):
                        p.nivel_pericol = 2
                        dictionar_final[cheie] = d[cheie]
            elif d[cheie] >= prag_nivel1:
                for p in lista_pachete:
                    if (type(p) != Pachet_ARP) and (p.IP_src == cheie):
                        p.nivel_pericol = 1
                        dictionar_final[cheie] = d[cheie]
# Teste output
        print(pachete)
        print(f"Mapare IP sursa : numar pachete {d}")
        print(f"Mapare IP sursa : numar pachete periculoase {dictionar_final}")
        k1 = 0
        k2 = 0
        for p in lista_pachete:
            if p.nivel_pericol >= 1 and type(p) != Pachet_ARP and p.IP_src != adresa_IP:
                k1 += 1
        for p in lista_pachete:
            try:
                if p.nivel_pericol == 0 and p.IP_src != adresa_IP:
                    k2 += 1
            except AttributeError:
                if p.nivel_pericol == 0 and p.eth_src != adresa_mac:
                    k2 += 1
        if nr_pachete == "":
            print(f"Au fost capturate 100 pachete; {k1+k2} daca se exclud pachetele provenite de la host, impartite astfel: {k1} periculoase si {k2} obisnuite")
        else:
            print(f"Au fost capturate {int(nr_pachete)} pachete; {k1+k2} daca excludem pachetele provenite de la host, impartite astfel: {k1} periculoase si {k2} obisnuite")
        t1 = 0
        u1 = 0
        i1 = 0
        a1 = 0
        for p in lista_pachete:
            if type(p) == Pachet_ARP and p.eth_src != adresa_mac:
                a1 += 1
            elif type(p) == Pachet_TCP and p.IP_src != adresa_IP:
                t1 += 1
            elif type(p) == Pachet_UDP and p.IP_src != adresa_IP:
                u1 += 1
            elif type(p) == Pachet_ICMP and p.IP_src != adresa_IP:
                i1 += 1
        print(f"Cele {k1+k2} pachete sunt impartite astfel: {t1} TCP, {u1} UDP, {i1} ICMP, {a1} ARP")
        print(f"Durata capturarii: {durata_capturarii}s")

    @staticmethod
    def show_stats(lista_pachete):
        plt.close()
        t = 0
        u = 0
        i = 0
        a = 0
        for p in lista_pachete:
            if type(p) == Pachet_ARP and p.eth_src != adresa_mac:
                a += 1
            elif type(p) == Pachet_TCP and p.IP_src != adresa_IP:
                t += 1
            elif type(p) == Pachet_UDP and p.IP_src != adresa_IP:
                u += 1
            elif type(p) == Pachet_ICMP and p.IP_src != adresa_IP:
                i += 1
        figura, (pie1, pie2) = plt.subplots(2, 1, figsize=(8, 6))
        tcp = 100*t/(t+u+i+a)
        udp = 100*u/(t+u+i+a)
        icmp = 100*i/(t+u+i+a)
        arp = 100*a/(t+u+i+a)
        tipuri_pachete_1 = [f'Pachete TCP {tcp:.2f}%', f'Pachete UDP {udp:.2f}%', f'Pachete ICMP {icmp:.2f}%', f'Pachete ARP {arp:.2f}%']
        valori_1 = [tcp, udp, icmp, arp]
        culori_1 = ['g', 'b', 'y', 'r']
        pie1.pie(valori_1, colors=culori_1, startangle=90, shadow=False)
        pie1.legend(bbox_to_anchor=(1, 1), loc='best', labels=tipuri_pachete_1)
        s = 0
        o = 0
        for p in lista_pachete:
            try:
                if p.nivel_pericol >= 1 and p.IP_src != adresa_IP:
                    s += 1
                elif p.IP_src != adresa_IP:
                    o += 1
            except AttributeError:
                if p.nivel_pericol >= 1 and p.eth_src != adresa_mac:
                    s += 1
                elif p.eth_src != adresa_mac:
                    o += 1
        pachete_suspicioase = 100*s/(s+o)
        pachete_obisnuite = 100*o/(s+o)
        tipuri_pachete_2 = [f'Pachete Suspicioase {pachete_suspicioase:.2f}%',f'Pachete Obișnuite {pachete_obisnuite:.2f}%']
        valori_2 = [pachete_suspicioase, pachete_obisnuite]
        culori_2 = ['r', 'b']
        pie2.pie(valori_2, colors=culori_2, startangle=90, shadow=False)
        pie2.legend(bbox_to_anchor=(1, 1), loc='best', labels=tipuri_pachete_2)
        figura.suptitle("Statistici ale pachetelor capturate")
        plt.show()

    @staticmethod
    def save(lista_pachete, dictionar_final, adresa):
        if os.path.exists(f'{adresa}.txt'):
            os.remove(f'{adresa}.txt')
        for i in lista_pachete:
            with open(f'{adresa}.txt', 'a') as fisier:
                fisier.write(str(i))
        if os.path.exists(f'{adresa}_json.json'):
            os.remove(f'{adresa}_json.json')
        with open(f'{adresa}_json.json', 'w') as dictionar:
            json.dump(dictionar_final, dictionar)

    @staticmethod
    def ftp_transfer(ip_server, username_server, parola_server, adresa):
        ftp = FTP(ip_server)
        ftp.login(username_server, parola_server)
        ftp_transfer1 = open(f'{adresa}.txt', 'rb')
        ftp.storlines(f'STOR {adresa}.txt', ftp_transfer1)
        ftp_transfer2 = open(f'{adresa}_json.json', 'rb')
        ftp.storlines(f'STOR {adresa}_json.json', ftp_transfer2)
        ftp_transfer1.close()
        ftp_transfer2.close()
        ftp.quit()

    @staticmethod
    def oprire_rulare():
        global run
        run = False
        print("Execuția automată se va opri dupa rularea actuală")

    @staticmethod
    def pornire_rulare():
        global run
        run = True
        print("Execuția automată a fost repornită")

    @staticmethod
    def test_DoS():
        pachet_fals = Ether(src='D0:B0:56:C0:00:04', dst='D1:B1:57:C1:01:04')/IP(src='5.5.5.5', dst='192.168.1.202', version=4)/ICMP(type=8)
        sendp(pachet_fals, count=50)

    @staticmethod
    def rulare_automata(lista_pachete, dictionar_final, nr_pachete, adresa, ip_server, username_server, parola_server, interfata=None, filtru=None):
        while 1:
            if run:
                lista_pachete.clear()
                dictionar_final.clear()
                d = {}
                id_pachet = 0
                timp_incepere = datetime.now()
                if nr_pachete == "":
                    pachete = sniff(count=100, iface=interfata, filter=filtru)
                else:
                    pachete = sniff(count=int(nr_pachete), iface=interfata, filter=filtru)
                timp_finalizare = datetime.now()
                delta_t = timp_finalizare - timp_incepere
                durata_capturarii = delta_t.seconds + delta_t.microseconds * 1e-6
                prag_nivel2 = 2 * (delta_t.seconds + delta_t.microseconds * 1e-6)
                prag_nivel1 = delta_t.seconds + delta_t.microseconds * 1e-6
                for i in pachete:
                    id_pachet += 1
                    if 'ARP' in i:
                        p = Pachet_ARP(id_pachet, i['Ether'].dst, i['Ether'].src, i['ARP'].op)
                        lista_pachete.append(p)
                    elif 'IP' in i:
                        if 'TCP' in i:
                            p = Pachet_TCP(id_pachet, i['Ether'].dst, i['Ether'].src, i['IP'].dst, i['IP'].src,
                                           i['IP'].version, i['IP'].proto, i['TCP'].sport, i['TCP'].dport)
                            lista_pachete.append(p)
                        elif 'UDP' in i:
                            p = Pachet_UDP(id_pachet, i['Ether'].dst, i['Ether'].src, i['IP'].dst, i['IP'].src,
                                           i['IP'].version, i['IP'].proto, i['UDP'].sport, i['UDP'].dport)
                            lista_pachete.append(p)
                        elif 'ICMP' in i:
                            p = Pachet_ICMP(id_pachet, i['Ether'].dst, i['Ether'].src, i['IP'].dst, i['IP'].src,
                                            i['IP'].version, i['IP'].proto, i['ICMP'].type)
                            lista_pachete.append(p)
                for j in lista_pachete:
                    try:
                        ip_periculos = j.IP_src
                        if ip_periculos != adresa_IP:
                            if ip_periculos in d.keys():
                                d[ip_periculos] += 1
                            else:
                                d[ip_periculos] = 1
                    except AttributeError:
                        continue
                for cheie in d.keys():
                    if d[cheie] >= prag_nivel2:
                        for p in lista_pachete:
                            if (type(p) != Pachet_ARP) and (p.IP_src == cheie):
                                p.nivel_pericol = 2
                                dictionar_final[cheie] = d[cheie]
                    elif d[cheie] >= prag_nivel1:
                        for p in lista_pachete:
                            if (type(p) != Pachet_ARP) and (p.IP_src == cheie):
                                p.nivel_pericol = 1
                                dictionar_final[cheie] = d[cheie]
                # Teste output
                print(pachete)
                print(f"Mapare IP sursa : numar pachete {d}")
                print(f"Mapare IP sursa : numar pachete periculoase {dictionar_final}")
                k1 = 0
                k2 = 0
                for p in lista_pachete:
                    if p.nivel_pericol >= 1 and type(p) != Pachet_ARP and p.IP_src != adresa_IP:
                        k1 += 1
                for p in lista_pachete:
                    try:
                        if p.nivel_pericol == 0 and p.IP_src != adresa_IP:
                            k2 += 1
                    except AttributeError:
                        if p.nivel_pericol == 0 and p.eth_src != adresa_mac:
                            k2 += 1
                if nr_pachete == "":
                    print(
                        f"Au fost capturate 100 pachete; {k1 + k2} daca se exclud pachetele provenite de la host, impartite astfel: {k1} periculoase si {k2} obisnuite")
                else:
                    print(
                        f"Au fost capturate {int(nr_pachete)} pachete; {k1 + k2} daca excludem pachetele provenite de la host, impartite astfel: {k1} periculoase si {k2} obisnuite")
                t1 = 0
                u1 = 0
                i1 = 0
                a1 = 0
                for p in lista_pachete:
                    if type(p) == Pachet_ARP and p.eth_src != adresa_mac:
                        a1 += 1
                    elif type(p) == Pachet_TCP and p.IP_src != adresa_IP:
                        t1 += 1
                    elif type(p) == Pachet_UDP and p.IP_src != adresa_IP:
                        u1 += 1
                    elif type(p) == Pachet_ICMP and p.IP_src != adresa_IP:
                        i1 += 1
                print(f"Cele {k1 + k2} pachete sunt impartite astfel: {t1} TCP, {u1} UDP, {i1} ICMP, {a1} ARP")
                print(f"Durata capturarii: {durata_capturarii}s")

                t = 0
                u = 0
                i = 0
                a = 0
                for p in lista_pachete:
                    if type(p) == Pachet_ARP and p.eth_src != adresa_mac:
                        a += 1
                    elif type(p) == Pachet_TCP and p.IP_src != adresa_IP:
                        t += 1
                    elif type(p) == Pachet_UDP and p.IP_src != adresa_IP:
                        u += 1
                    elif type(p) == Pachet_ICMP and p.IP_src != adresa_IP:
                        i += 1
                figura, (pie1, pie2) = plt.subplots(2, 1, figsize=(8, 6))
                tcp = 100*t/(t+u+i+a)
                udp = 100*u/(t+u+i+a)
                icmp = 100*i/(t+u+i+a)
                arp = 100*a/(t+u+i+a)
                tipuri_pachete_1 = [f'Pachete TCP {tcp:.2f}%', f'Pachete UDP {udp:.2f}%', f'Pachete ICMP {icmp:.2f}%',
                                    f'Pachete ARP {arp:.2f}%']
                valori_1 = [tcp, udp, icmp, arp]
                culori_1 = ['g', 'b', 'y', 'r']
                pie1.pie(valori_1, colors=culori_1, startangle=90, shadow=False)
                pie1.legend(bbox_to_anchor=(1, 1), loc='best', labels=tipuri_pachete_1)
                s = 0
                o = 0
                for p in lista_pachete:
                    try:
                        if p.nivel_pericol >= 1 and p.IP_src != adresa_IP:
                            s += 1
                        elif p.IP_src != adresa_IP:
                            o += 1
                    except AttributeError:
                        if p.nivel_pericol >= 1 and p.eth_src != adresa_mac:
                            s += 1
                        elif p.eth_src != adresa_mac:
                            o += 1
                pachete_suspicioase = 100*s/(s+o)
                pachete_obisnuite = 100*o/(s+o)
                tipuri_pachete_2 = [f'Pachete Suspicioase {pachete_suspicioase:.2f}%',
                                    f'Pachete Obișnuite {pachete_obisnuite:.2f}%']
                valori_2 = [pachete_suspicioase, pachete_obisnuite]
                culori_2 = ['r', 'b']
                pie2.pie(valori_2, colors=culori_2, startangle=90, shadow=False)
                pie2.legend(bbox_to_anchor=(1, 1), loc='best', labels=tipuri_pachete_2)
                figura.suptitle("Statistici ale pachetelor capturate")
                figura.savefig(f'{adresa}_grafic.png')

                if os.path.exists(f'{adresa}.txt'):
                    os.remove(f'{adresa}.txt')
                for i in lista_pachete:
                    with open(f'{adresa}.txt', 'a') as fisier:
                        fisier.write(str(i))
                if os.path.exists(f'json_{adresa}.json'):
                    os.remove(f'{adresa}_json.json')
                with open(f'{adresa}_json.json', 'w') as dictionar:
                    json.dump(dictionar_final, dictionar)

                ftp = FTP(ip_server)
                ftp.login(username_server, parola_server)
                cale_folder = f'{timp_incepere.day}-{timp_incepere.month}-{timp_incepere.year}_{timp_incepere.hour}-{timp_incepere.minute}-{timp_incepere.second}-{timp_incepere.microsecond}'
                ftp.mkd(cale_folder)
                ftp.cwd(cale_folder)
                ftp_transfer1 = open(f'{adresa}.txt', 'rb')
                ftp.storlines(f'STOR {adresa}.txt', ftp_transfer1)
                ftp_transfer1.close()
                ftp_transfer2 = open(f'{adresa}_json.json', 'rb')
                ftp.storlines(f'STOR {adresa}_json.json', ftp_transfer2)
                ftp_transfer2.close()
                ftp_transfer3 = open(f'{adresa}_grafic.png', 'rb')
                ftp.storbinary(f'STOR {adresa}_grafic.png', ftp_transfer3)
                ftp_transfer3.close()
                ftp.quit()


### Pachet

class Pachet(object):

    def __init__(self, id_pachet, eth_dst, eth_src, nivel_pericol=0):
        self.id_pachet = id_pachet
        self.eth_dst = eth_dst
        self.eth_src = eth_src
        self.nivel_pericol = nivel_pericol
        # self.continut = continut


#     def __str__(self):
#         return f"""
# ##############################
# 'Numar Pachet': {self.id_pachet}
# 'Nivel Pericol': {self.nivel_pericol}
#
# 'Ethernet':
#     'dst': {self.eth_dst},
#     'src': {self.eth_src},
#
# 'ARP':
#     'type': {self.arp_type}
#
# 'IP':
#     'dst': {self.IP_dst},
#     'src': {self.IP_src},
#     'version': {self.IP_version},
#     'protocol' : {self.IP_protocol}
#
# 'ICMP':
#     'type': {self.ICMP_type}
#
# 'TCP':
#     'sport': {self.TCP_sport},
#     'dport': {self.TCP_dport}
#
# 'UDP':
#     'sport':{self.UDP_sport},
#     'dport':{self.UDP_dport}
#
#     """

class Pachet_ARP(Pachet):

    def __init__(self, id_pachet, eth_dst, eth_src, arp_type, nivel_pericol=0, tip_pachet='ARP'):
        super().__init__(id_pachet, eth_dst, eth_src, nivel_pericol)
        self.arp_type = arp_type
        self.tip_pachet = tip_pachet

    def __str__(self):
        return f"""
##############################
'Numar Pachet': {self.id_pachet}
'Nivel Pericol': {self.nivel_pericol}
'Tip Pachet': {self.tip_pachet}

'Ethernet':
    'dst': {self.eth_dst},
    'src': {self.eth_src},

'ARP':
    'type': {self.arp_type}

    """


class Pachet_TCP(Pachet):

    def __init__(self, id_pachet, eth_dst, eth_src, IP_dst, IP_src, IP_version, IP_protocol, TCP_sport, TCP_dport,
                 nivel_pericol=0, tip_pachet='TCP'):
        super().__init__(id_pachet, eth_dst, eth_src, nivel_pericol)
        self.IP_dst = IP_dst
        self.IP_src = IP_src
        self.IP_version = IP_version
        self.IP_protocol = IP_protocol
        self.TCP_sport = TCP_sport
        self.TCP_dport = TCP_dport
        self.tip_pachet = tip_pachet

    def __str__(self):
        return f"""
##############################
'Numar Pachet': {self.id_pachet}
'Nivel Pericol': {self.nivel_pericol}
'Tip Pachet': {self.tip_pachet}

'Ethernet':
    'dst': {self.eth_dst},
    'src': {self.eth_src},

'IP':
    'dst': {self.IP_dst},
    'src': {self.IP_src},
    'version': {self.IP_version},
    'protocol' : {self.IP_protocol}

'TCP':
    'sport': {self.TCP_sport},
    'dport': {self.TCP_dport}

    """


class Pachet_UDP(Pachet):

    def __init__(self, id_pachet, eth_dst, eth_src, IP_dst, IP_src, IP_version, IP_protocol, UDP_sport, UDP_dport,
                 nivel_pericol=0, tip_pachet='UDP'):
        super().__init__(id_pachet, eth_dst, eth_src, nivel_pericol)
        self.IP_dst = IP_dst
        self.IP_src = IP_src
        self.IP_version = IP_version
        self.IP_protocol = IP_protocol
        self.UDP_sport = UDP_sport
        self.UDP_dport = UDP_dport
        self.tip_pachet = tip_pachet

    def __str__(self):
        return f"""
##############################
'Numar Pachet': {self.id_pachet}
'Nivel Pericol': {self.nivel_pericol}
'Tip Pachet': {self.tip_pachet}

'Ethernet':
    'dst': {self.eth_dst},
    'src': {self.eth_src},

'IP':
    'dst': {self.IP_dst},
    'src': {self.IP_src},
    'version': {self.IP_version},
    'protocol' : {self.IP_protocol}

'UDP':
    'sport': {self.UDP_sport},
    'dport': {self.UDP_dport}

    """


class Pachet_ICMP(Pachet):
    def __init__(self, id_pachet, eth_dst, eth_src, IP_dst, IP_src, IP_version, IP_protocol, ICMP_type, nivel_pericol=0,
                 tip_pachet='ICMP'):
        super().__init__(id_pachet, eth_dst, eth_src, nivel_pericol)
        self.IP_dst = IP_dst
        self.IP_src = IP_src
        self.IP_version = IP_version
        self.IP_protocol = IP_protocol
        self.ICMP_type = ICMP_type
        self.tip_pachet = tip_pachet

    def __str__(self):
        return f"""
##############################
'Numar Pachet': {self.id_pachet}
'Nivel Pericol': {self.nivel_pericol}
'Tip Pachet': {self.tip_pachet}

'Ethernet':
    'dst': {self.eth_dst},
    'src': {self.eth_src},

'IP':
    'dst': {self.IP_dst},
    'src': {self.IP_src},
    'version': {self.IP_version},
    'protocol' : {self.IP_protocol}

'ICMP':
    'type': {self.ICMP_type}

    """

# #, arp_type, IP_dst, IP_src, IP_version, IP_protocol, ICMP_type, TCP_sport, TCP_dport, UDP_sport, UDP_dport
# self.arp_type = arp_type
# self.IP_dst = IP_dst
# self.IP_src = IP_src
# self.IP_version = IP_version
# self.IP_protocol = IP_protocol
# self.ICMP_type = ICMP_type
# self.TCP_sport = TCP_sport
# self.TCP_dport = TCP_dport
# self.UDP_sport = UDP_sport
# self.UDP_dport = UDP_dport

