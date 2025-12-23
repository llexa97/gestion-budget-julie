# Déploiement Rapide - LXC Proxmox

Guide rapide pour déployer dans `/root/gestion-budget-julie`

## 1. Transférer les fichiers vers le LXC

Depuis votre machine locale :

```bash
# Compresser le projet
cd "/Users/axeldondin/Projets/Code/Gestion de budget"
tar -czf gestion-budget.tar.gz .

# Transférer vers le LXC (remplacer <IP_LXC> par l'IP de votre container)
scp gestion-budget.tar.gz root@<IP_LXC>:/root/

# Se connecter au LXC
ssh root@<IP_LXC>
```

## 2. Installation sur le LXC

```bash
# Décompresser dans le bon dossier
cd /root
mkdir -p gestion-budget-julie
tar -xzf gestion-budget.tar.gz -C gestion-budget-julie
cd gestion-budget-julie

# Nettoyer l'archive
rm /root/gestion-budget.tar.gz

# Mettre à jour le système
apt update && apt upgrade -y

# Installer les dépendances
apt install -y python3 python3-pip python3-venv nginx

# Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer les packages Python
pip install --upgrade pip
pip install flask flask-sqlalchemy flask-migrate flask-wtf gunicorn
```

## 3. Configuration

```bash
# Créer le fichier .env
cp .env.example .env

# Générer une clé secrète et configurer
cat > .env << 'EOF'
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
EOF

# Ou éditer manuellement
nano .env
```

## 4. Base de données

```bash
# Toujours dans /root/gestion-budget-julie avec .venv activé
source .venv/bin/activate

# Créer le dossier instance
mkdir -p instance

# Initialiser la base de données
export FLASK_APP=wsgi.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 5. Test manuel

```bash
# Tester que tout fonctionne
cd /root/gestion-budget-julie
source .venv/bin/activate
gunicorn -w 2 -b 0.0.0.0:5001 wsgi:app

# Tester dans un navigateur: http://<IP_LXC>:5001
# Ctrl+C pour arrêter
```

## 6. Installation du service systemd

```bash
# Créer le dossier de logs
mkdir -p /var/log/budget-manager

# Copier le service
cp /root/gestion-budget-julie/budget-manager.service /etc/systemd/system/

# Recharger systemd
systemctl daemon-reload

# Activer et démarrer le service
systemctl enable budget-manager
systemctl start budget-manager

# Vérifier le statut
systemctl status budget-manager
```

## 7. Nginx (optionnel)

```bash
# Créer la config
nano /etc/nginx/sites-available/budget-manager
```

Coller :
```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /root/gestion-budget-julie/app/static;
        expires 30d;
    }
}
```

Activer :
```bash
ln -s /etc/nginx/sites-available/budget-manager /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# Si Nginx est utilisé, modifier le service pour bind sur localhost:
nano /etc/systemd/system/budget-manager.service
# Changer: --bind 0.0.0.0:5001 en --bind 127.0.0.1:5001
systemctl daemon-reload
systemctl restart budget-manager
```

## Accès à l'application

- **Sans Nginx** : `http://<IP_LXC>:5001`
- **Avec Nginx** : `http://<IP_LXC>`

## Commandes utiles

```bash
# Voir les logs
journalctl -u budget-manager -f

# Redémarrer le service
systemctl restart budget-manager

# Arrêter le service
systemctl stop budget-manager

# Voir le statut
systemctl status budget-manager

# Mettre à jour l'app
cd /root/gestion-budget-julie
source .venv/bin/activate
# Copier nouveaux fichiers...
flask db upgrade
systemctl restart budget-manager
```

## Backup

```bash
# Backup manuel
cp /root/gestion-budget-julie/instance/budget.db \
   /root/backups/budget_$(date +%Y%m%d).db

# Backup automatique (cron)
crontab -e
# Ajouter:
0 3 * * * cp /root/gestion-budget-julie/instance/budget.db /root/backups/budget_$(date +\%Y\%m\%d).db
```

## Troubleshooting

```bash
# Service ne démarre pas
journalctl -u budget-manager -n 50

# Tester manuellement
cd /root/gestion-budget-julie
source .venv/bin/activate
gunicorn -w 2 -b 0.0.0.0:5001 wsgi:app

# Port occupé
lsof -i :5001
kill -9 <PID>

# Permissions
chmod -R 755 /root/gestion-budget-julie
```

## Chemin complet de l'application

```
/root/gestion-budget-julie/
├── app/
├── instance/
│   └── budget.db
├── .venv/
├── wsgi.py
├── main.py
├── config.py
├── .env
└── budget-manager.service
```
