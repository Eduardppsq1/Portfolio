class Pachet(object):

    def __init__(self, id_pachet, eth_dst, eth_src, nivel_pericol=0):
        self.id_pachet = id_pachet
        self.eth_dst = eth_dst
        self.eth_src = eth_src
        self.nivel_pericol = nivel_pericol

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

    def __init__(self, id_pachet, eth_dst, eth_src, IP_dst, IP_src, IP_version, IP_protocol, TCP_sport, TCP_dport, nivel_pericol=0, tip_pachet='TCP'):
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

    def __init__(self, id_pachet, eth_dst, eth_src, IP_dst, IP_src, IP_version, IP_protocol, UDP_sport, UDP_dport, nivel_pericol=0, tip_pachet='UDP'):
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
    def __init__(self, id_pachet, eth_dst, eth_src, IP_dst, IP_src, IP_version, IP_protocol, ICMP_type, nivel_pericol=0, tip_pachet='ICMP'):
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
