#!/bin/bash

# Editar las siguientes líneas con la información requerida

# Ruta a los archivos del planet.py
PLANET_PATH="/home/usuario/planet"
# Ruta al repositorio local de Github con la web. Por seguridad debe ser diferente al del planet
LOCAL_REPO="/home/usuario/web"
# Usuario de Github
USERNAME="username"
# Contraseña ¡¡¡Se almacena en texto plano!!!
PASSWORD="password"
# URL al repositorio de Github
REMOTE_REPO="github.com/github_user/repo-name.git"

######################################################
######################################################
date_var="$(date)"
# Se accede al directorio del planet y se actualizan las entradas
cd $PLANET_PATH
python3 planet.py --no-browser
# Se copian los archivos html al repositorio local
cd salida 
cp *.html *.xml $LOCAL_REPO
# Se suben los cambios a Github
cd $LOCAL_REPO
git add *.html *.xml
git commit -a -m "Actualización $date_var"
git push -u https://$USERNAME:$PASSWORD@$REMOTE_REPO master

