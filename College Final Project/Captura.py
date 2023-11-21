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

#Initializare Mac si IP Host, variabila globala run
adresa_mac = get_mac_address()
host = socket.gethostname()
adresa_IP = socket.gethostbyname(host)
run = True

# Definire clasa Captura cu design patternul singleton
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

    # Definire metoda statica capture
    @staticmethod
    def capture(lista_pachete, dictionar_final, nr_pachete, interfata=None, filtru=None):
        # Cleanup general in cazul rularilor multiple consecutive
        os.system('cls')
        lista_pachete.clear()
        dictionar_final.clear()
        # Initializare variabile
        d = {}
        id_pachet = 0
        # Capturarea pachetelor, calculare timp de rulare si calculare praguri de pericol
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
        # Transformare elemente din lista in instante ale clasei Pachet si subclase ale ei
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
        # Verificare numar de aparitii pentru fiecare IP sursa
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
        # Verificare daca numarul de aparitii a depasit vreunul din pragurile de pericol
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

    # Definire metoda statica show_stats
    @staticmethod
    def show_stats(lista_pachete):
        # Initializare si cleanup
        plt.close()
        t = 0
        u = 0
        i = 0
        a = 0
        # Generare grafic tipuri de pachete
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
        # Generare grafic pachete obisnuite sau suspicioase
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

    # Definire metoda statica save
    @staticmethod
    def save(lista_pachete, dictionar_final, adresa):
        # Salvare locala a pachetelor folosind path-ul specificat. Daca este nevoie, intai se sterg datele vechi.
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
    # Definire metoda statica ftp_transfer
    def ftp_transfer(ip_server, username_server, parola_server, adresa):
        # Logare si transfer de date catre Windows Server remote pentru centralizarea datelor
        ftp = FTP(ip_server)
        ftp.login(username_server, parola_server)
        ftp_transfer1 = open(f'{adresa}.txt', 'rb')
        ftp.storlines(f'STOR {adresa}.txt', ftp_transfer1)
        ftp_transfer2 = open(f'{adresa}_json.json', 'rb')
        ftp.storlines(f'STOR {adresa}_json.json', ftp_transfer2)
        ftp_transfer1.close()
        ftp_transfer2.close()
        ftp.quit()

    # Definire netida statica oprire_rulare
    @staticmethod
    def oprire_rulare():
        # Metoda ce opreste rularea automata dupa finalizarea rularii in curs
        global run
        run = False
        print("Execuția automată se va opri dupa rularea actuală")

    # Definire metoda statica pornire_rulare
    @staticmethod
    def pornire_rulare():
        # Metoda ce reporneste rularea automata dupa oprirea acesteia
        global run
        run = True
        print("Execuția automată a fost repornită")

    @staticmethod
    # Definire metoda statica test_DoS
    def test_DoS():
        # Metoda ce genereaza un numar mare de pachete pentru a vedea comportamentul programului in cazul unui atac DDoS
        pachet_fals = Ether(src='D0:B0:56:C0:00:04', dst='D1:B1:57:C1:01:04')/IP(src='5.5.5.5', dst='192.168.1.202', version=4)/ICMP(type=8)
        sendp(pachet_fals, count=50)

    # Definire metoda statica rulare_automata
    @staticmethod
    def rulare_automata(lista_pachete, dictionar_final, nr_pachete, adresa, ip_server, username_server, parola_server, interfata=None, filtru=None):
        # Metoda ce va rula automat toate celelalte metode mentionate anterior
        # In acest caz, graficele si testele de output vor fi de asemenea transferate catre server
        while 1:
            if run:
                lista_pachete.clear()
                dictionar_final.clear()
                d = {}
                id_pachet = 0
                os.chdir(r'C:\Users\Carillas\Desktop\Licenta')
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
                print("\n")

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
                cale_folder = f'{timp_incepere.day}-{timp_incepere.month}-{timp_incepere.year}_{timp_incepere.hour}-{timp_incepere.minute}-{timp_incepere.second}-{timp_incepere.microsecond}'
                os.mkdir(cale_folder)
                os.chdir(cale_folder)
                figura.savefig(f'{adresa}_grafic.png')

                if os.path.exists(f'{adresa}.txt'):
                    os.remove(f'{adresa}.txt')
                for i in lista_pachete:
                    with open(f'{adresa}.txt', 'a') as fisier:
                        fisier.write(str(i))
                if os.path.exists(f'{adresa}_json.json'):
                    os.remove(f'{adresa}_json.json')
                with open(f'{adresa}_json.json', 'w') as dictionar:
                    json.dump(dictionar_final, dictionar)
                if os.path.exists(f'{adresa}_output.txt'):
                    os.remove(f'{adresa}_output.txt')
                with open(f'{adresa}_output.txt', 'w') as output:
                    output.write(str(pachete))
                    output.write('\n')
                    output.write(f"Mapare IP sursa : numar pachete {d}")
                    output.write('\n')
                    output.write(f"Mapare IP sursa : numar pachete periculoase {dictionar_final}")
                    output.write('\n')
                    if nr_pachete == "":
                        output.write(
                            f"Au fost capturate 100 pachete; {k1 + k2} daca se exclud pachetele provenite de la host, impartite astfel: {k1} periculoase si {k2} obisnuite")
                        output.write('\n')
                    else:
                        output.write(
                            f"Au fost capturate {int(nr_pachete)} pachete; {k1 + k2} daca excludem pachetele provenite de la host, impartite astfel: {k1} periculoase si {k2} obisnuite")
                        output.write('\n')
                    output.write(f"Cele {k1 + k2} pachete sunt impartite astfel: {t1} TCP, {u1} UDP, {i1} ICMP, {a1} ARP")
                    output.write('\n')
                    output.write(f"Durata capturarii: {durata_capturarii}s")

                ftp = FTP(ip_server)
                ftp.login(username_server, parola_server)
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
                ftp_transfer4 = open(f'{adresa}_output.txt', 'rb')
                ftp.storlines(f'STOR {adresa}_output.txt', ftp_transfer4)
                ftp_transfer4.close()
                ftp.quit()
