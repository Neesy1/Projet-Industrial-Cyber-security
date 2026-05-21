import nmap
from tabulate import tabulate
from tqdm import tqdm
import threading
import time

def scan_interactif():
    # --- AJOUT : SELECTION INITIALE ---
    print("\n" + "="*60)
    print("              SÉLECTION DE LA CIBLE                      ")
    print("="*60)
    print(" [1] Utiliser l'IP directe (192.168.0.10)")
    print(" [2] Lancer un scan réseau")
    
    pre_choix = input("\n[>] Choix : ")

    if pre_choix == "1":
        ip = "192.168.0.10"
        ports_liste = ['80', '443', '102'] # Ports simulés pour passer au menu
    else:
        # --- TON CODE DE BASE SANS MODIFICATION ---
        nm = nmap.PortScanner()
        print("\n" + "="*60)
        print("   SCAN & SÉLECTION DE CIBLE (GROUPÉ PAR ÉQUIPEMENT)   ")
        print("="*60)
        
        cible = input("\n[?] IP ou Plage à analyser (ex: 192.168.0.10) : ")
        
        # --- SYSTÈME DE BARRE DE CHARGEMENT ---
        scan_termine = False

        def afficher_barre():
            # On crée une barre de 100%
            with tqdm(total=100, desc="[*] Analyse en cours", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]") as pbar:
                while not scan_termine:
                    time.sleep(0.5)
                    if pbar.n < 95: # On bloque à 95% tant que nmap n'a pas fini
                        pbar.update(2)
                pbar.update(100 - pbar.n) # On complète à 100% à la fin

        # On lance la barre dans un thread séparé pour ne pas bloquer le scan
        thread_barre = threading.Thread(target=afficher_barre)
        thread_barre.start()

        try:
            # SCAN OPTIMISÉ : On ne scanne que les ports 80, 443 pour ton automate Siemens
            # Ajoute d'autres ports si besoin (ex: -p 80,443,102,502)
            nm.scan(hosts=cible, arguments='-p 80,443,102 --open -sV')
        except Exception as e:
            print(f"\n[!] Erreur : {e}")
            scan_termine = True
            return None
        finally:
            scan_termine = True
            thread_barre.join() # On attend que le thread de la barre se termine propre
        # ---------------------------------------

        table_data = []
        liste_cibles = {} 
        compteur = 1

        for host in nm.all_hosts():
            ports_ouverts = []
            services_detectes = []
            versions_detectees = []

            for proto in nm[host].all_protocols():
                lport = sorted(nm[host][proto].keys())
                for port in lport:
                    service = nm[host][proto][port].get('name', 'N/A')
                    product = nm[host][proto][port].get('product', '')
                    version = nm[host][proto][port].get('version', '')
                    
                    ports_ouverts.append(f"{port}/{proto}")
                    services_detectes.append(service)
                    if product:
                        versions_detectees.append(f"{product} {version}".strip())

            ports_str = "\n".join(ports_ouverts)
            services_str = "\n".join(services_detectes)
            versions_str = "\n".join(list(set(versions_detectees)))

            table_data.append([compteur, host, ports_str, services_str, versions_str])
            liste_cibles[str(compteur)] = {"ip": host, "ports": ports_ouverts}
            compteur += 1

        if table_data:
            print("\n" + tabulate(table_data, headers=["ID", "IP", "Ports", "Services", "Versions"], tablefmt="grid"))
            
            print("\n" + "-"*30)
            choix = input("[>] Choisissez l'ID d'un équipement à analyser (ou 'q') : ")
            
            if choix in liste_cibles:
                cible_verrouillee = liste_cibles[choix]
                ip = cible_verrouillee['ip']
                ports_liste = [str(p).split('/')[0] for p in cible_verrouillee['ports']]
            else:
                return None
        else:
            print("\n[!] Aucun service trouvé (Vérifiez si l'IP est correcte ou si le port 80/443 est ouvert).")
            return None

    # --- MENU DES ATTAQUES (TON CODE DE BASE) ---
    print(f"\n[!] CIBLE VERROUILLÉE : {ip}")
    print("\n--- MENU DES ATTAQUES DISPONIBLES ---")
    
    attaques_possibles = {}
    id_att = 1

    # Option Brute Force (Priorité si port 80/443 ouvert)
    if '80' in ports_liste or '443' in ports_liste:
        print(f" [{id_att}] Brute Force Web (Siemens S7 détecté)")
        attaques_possibles[id_att] = "bruteforce.py"
        id_att += 1

    # Option DoS
    print(f" [{id_att}] DoS (Attaque par déni de service)")
    attaques_possibles[id_att] = "dos.py"
    id_att += 1
    
    # Ajout du Replay si port 102 présent
    if '102' in ports_liste:
        print(f" [{id_att}] Replay Attack (S7Comm détecté)")
        attaques_possibles[id_att] = "Replay.py"
        id_att += 1

    final_choice = input("\n[>] Quelle attaque lancer ? : ")
    
    try:
        script_nom = attaques_possibles.get(int(final_choice))
        return {"ip": ip, "script": script_nom}
    except:
        print("[!] Choix invalide.")
        return None

if __name__ == "__main__":
    resultat = scan_interactif()
    if resultat:
        print(f"\n[*] Prêt à lancer {resultat['script']} sur {resultat['ip']}")