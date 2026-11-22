# Démarrer l’application

Depuis la racine du dépôt, dans PowerShell, créez un environnement virtuel et installez Django :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

> Python 3.12 ou une version plus récente est requis par Django 6.1.

> Sur macOS ou Linux, activez l’environnement avec `source .venv/bin/activate`.

> Si PowerShell bloque l’activation du script, utilisez directement `.\.venv\Scripts\python.exe` à la place de `python` dans les commandes ci-dessous.

Appliquez les migrations puis démarrez le serveur de développement :

```powershell
python manage.py migrate
python manage.py runserver
```

Ouvrez ensuite [http://127.0.0.1:8000/polls/](http://127.0.0.1:8000/polls/) pour consulter les sondages. L’administration est disponible à [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

Pour créer un compte administrateur, ouvrez un second terminal à la racine du dépôt, activez le même environnement virtuel puis lancez :

```powershell
python manage.py createsuperuser
```

## Fonctionnalités

- Affichage des cinq questions publiées les plus récentes ; les questions dont la date est dans le futur restent masquées.
- Page de détail avec formulaire de vote protégé par le jeton CSRF de Django.
- Enregistrement des votes et page de résultats avec le nombre de voix par choix.
- Gestion des questions et de leurs choix liés dans l’administration Django.
- Tests automatisés pour les dates, l’affichage, les questions à venir et le vote.

Exécutez les tests avec :

```powershell
python manage.py test polls
```

Les modèles `Question` et `Choice` se trouvent dans `polls/models/models.py`. Les vues sont dans `polls/views/views.py`, les routes dans `polls/urls.py`, les modèles d’administration dans `polls/admin/admin.py`, et les pages HTML dans `polls/templates/polls/`.

## Documentation de référence

Cette application suit le tutoriel officiel [Writing your first Django app](https://docs.djangoproject.com/en/6.1/intro/), parties 1 à 7, pour Django 6.1.
