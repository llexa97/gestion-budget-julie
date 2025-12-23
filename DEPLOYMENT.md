# Guide de Déploiement - Gestion de Budget

## Table des matières
- [Prérequis](#prérequis)
- [Configuration Locale](#configuration-locale)
- [Variables d'Environnement](#variables-denvironnement)
- [Déploiement en Production](#déploiement-en-production)
- [Maintenance](#maintenance)

## Prérequis

- Python 3.10 ou supérieur
- uv (gestionnaire de paquets Python)
- Git

## Configuration Locale

### 1. Installation des dépendances

```bash
# Créer l'environnement virtuel
uv venv

# Activer l'environnement virtuel
# Sur macOS/Linux:
source .venv/bin/activate
# Sur Windows:
.venv\Scripts\activate

# Installer les dépendances
uv pip install -r pyproject.toml
```

### 2. Configuration de l'environnement

Copier le fichier `.env.example` en `.env` et modifier les valeurs :

```bash
cp .env.example .env
```

### 3. Initialisation de la base de données

```bash
# Créer les migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. Lancement du serveur de développement

```bash
python main.py
```

L'application sera accessible sur `http://localhost:5001`

## Variables d'Environnement

Voir le fichier `.env.example` pour la liste complète des variables.

### Variables Obligatoires en Production

- `SECRET_KEY` : Clé secrète pour les sessions (générer avec `python -c "import secrets; print(secrets.token_hex(32))"`)
- `FLASK_ENV` : `production` pour la production
- `DATABASE_URL` : URL de connexion à la base de données PostgreSQL (recommandé pour la production)

### Variables Optionnelles

- `PORT` : Port du serveur (par défaut : 5001)

## Déploiement en Production

### Option 1 : Heroku

1. **Installer Heroku CLI**
   ```bash
   brew install heroku/brew/heroku  # macOS
   ```

2. **Créer l'application**
   ```bash
   heroku create mon-budget-app
   ```

3. **Ajouter PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Configurer les variables d'environnement**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   ```

5. **Créer un Procfile**
   ```bash
   echo "web: gunicorn main:app" > Procfile
   ```

6. **Installer Gunicorn**
   ```bash
   uv pip install gunicorn
   ```

7. **Déployer**
   ```bash
   git push heroku main
   heroku run flask db upgrade
   heroku open
   ```

### Option 2 : Railway

1. **Créer un compte sur [Railway.app](https://railway.app)**

2. **Connecter le repository GitHub**

3. **Configurer les variables d'environnement dans le dashboard**
   - `FLASK_ENV=production`
   - `SECRET_KEY=<votre_clé_secrète>`

4. **Ajouter PostgreSQL depuis le dashboard Railway**

5. **Le déploiement se fait automatiquement à chaque push**

### Option 3 : Docker

1. **Créer un Dockerfile**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY pyproject.toml .
   RUN pip install uv && uv pip install --system -r pyproject.toml

   COPY . .

   ENV FLASK_ENV=production
   ENV PORT=5001

   EXPOSE 5001

   CMD ["gunicorn", "-b", "0.0.0.0:5001", "main:app"]
   ```

2. **Build et run**
   ```bash
   docker build -t budget-app .
   docker run -p 5001:5001 --env-file .env budget-app
   ```

### Option 4 : VPS (Digital Ocean, AWS EC2, etc.)

1. **Se connecter au serveur**
   ```bash
   ssh user@votre-serveur.com
   ```

2. **Installer les dépendances système**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

3. **Cloner le repository**
   ```bash
   git clone https://github.com/votre-repo/budget-app.git
   cd budget-app
   ```

4. **Configurer l'environnement**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **Créer un service systemd**
   ```bash
   sudo nano /etc/systemd/system/budget-app.service
   ```

   Contenu :
   ```ini
   [Unit]
   Description=Budget Manager Flask App
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/home/user/budget-app
   Environment="PATH=/home/user/budget-app/.venv/bin"
   ExecStart=/home/user/budget-app/.venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 main:app

   [Install]
   WantedBy=multi-user.target
   ```

6. **Configurer Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/budget-app
   ```

   Contenu :
   ```nginx
   server {
       listen 80;
       server_name votre-domaine.com;

       location / {
           proxy_pass http://127.0.0.1:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. **Activer et démarrer**
   ```bash
   sudo ln -s /etc/nginx/sites-available/budget-app /etc/nginx/sites-enabled
   sudo systemctl start budget-app
   sudo systemctl enable budget-app
   sudo systemctl restart nginx
   ```

## Maintenance

### Backup de la base de données

**SQLite (développement)**
```bash
cp instance/budget.db instance/budget_backup_$(date +%Y%m%d).db
```

**PostgreSQL (production)**
```bash
# Heroku
heroku pg:backups:capture
heroku pg:backups:download

# Autre
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Mise à jour de l'application

```bash
git pull origin main
uv pip install -r pyproject.toml
flask db upgrade
sudo systemctl restart budget-app  # Si VPS
```

### Logs

**Heroku**
```bash
heroku logs --tail
```

**VPS avec systemd**
```bash
sudo journalctl -u budget-app -f
```

## Sécurité en Production

- ✅ Utiliser HTTPS (Let's Encrypt gratuit)
- ✅ Changer la `SECRET_KEY` régulièrement
- ✅ Utiliser PostgreSQL au lieu de SQLite
- ✅ Activer les backups automatiques
- ✅ Mettre à jour les dépendances régulièrement
- ✅ Ne jamais committer le fichier `.env`
- ✅ Utiliser des variables d'environnement pour les secrets

## Troubleshooting

### Erreur de port occupé
```bash
# Trouver le processus
lsof -i :5001
# Tuer le processus
kill -9 <PID>
```

### Erreur de migration
```bash
flask db stamp head
flask db migrate
flask db upgrade
```

### L'application ne démarre pas
```bash
# Vérifier les logs
tail -f logs/app.log
# Vérifier les variables d'environnement
printenv | grep FLASK
```
