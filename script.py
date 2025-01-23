import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.cng.sante.fr/evc-prochaine-session"
CACHE_FILE = "last_update.txt"

def get_page_content():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.text
    return None

def get_latest_update(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text()[:1000]  # Prend les 1000 premiers caractères

def has_page_changed():
    content = get_page_content()
    if not content:
        return False

    latest_update = get_latest_update(content)
    
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            last_update = file.read()
        if last_update == latest_update:
            return False  # Pas de changement

    # Sauvegarde la nouvelle version
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        file.write(latest_update)
    
    return True  # Page mise à jour !

if has_page_changed():
    print("🔔 La page a été mise à jour !")
else:
    print("✅ Aucune mise à jour trouvée.")
