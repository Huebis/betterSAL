#!/bin/bash

# Lokaler Ordner
LOCAL_DIR="/home/eliahh/Programmieren/Projekte/betterSAL/backend/"

# Remote Server
REMOTE_USER="huebis"
REMOTE_HOST="huebis.dev"
REMOTE_DIR="/var/www/huebis.dev/repos/betterSAL/backend/"

# rsync Optionen:
# -a  = Archivmodus (Rechte, Symlinks, etc.)
# -v  = verbose
# -z  = Komprimierung
# --delete = löscht auf dem Server Dateien, die lokal nicht mehr existieren
# -e ssh = benutzt SSH

rsync -avz --delete --exclude "venv" --exclude "database.db*" -e ssh "$LOCAL_DIR" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}"

# Status prüfen
if [ $? -eq 0 ]; then
    echo "Sync erfolgreich!"
else
    echo "Fehler beim Sync!"
fi