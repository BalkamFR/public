
Pour transformer un script Python en exécutable .exe, tu peux utiliser une bibliothèque comme PyInstaller. Voici les étapes :

1. Installer PyInstaller

Assure-toi d'avoir installé PyInstaller avec la commande suivante :
pip install pyinstaller


2. Créer un exécutable

Exécute cette commande dans le terminal à partir du répertoire où se trouve ton script Python (remplace mon_script.py par le nom de ton fichier) :
pyinstaller --onefile mon_script.py

L'option --onefile crée un fichier .exe unique contenant toutes les dépendances nécessaires.

3. Vérifier le résultat
Une fois la commande terminée, tu trouveras ton fichier .exe dans le dossier dist.

4. Options supplémentaires (facultatif)

Pour ajouter une icône à ton exécutable :
pyinstaller --onefile --icon=mon_icone.ico mon_script.py

Pour cacher la console (utile pour les applications GUI) :
pyinstaller --onefile --noconsole mon_script.py