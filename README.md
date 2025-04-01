# Projecte

Projecte per desplegar en un contenidor docker

## Arxiu .env que cal crear/copiar dins la carpeta API del projecte (no està en el git)

Executeu la seguent comanda per crear l'arxiu .env
```
cat <<EOF > ./ProjecteLogin/API/.env
DB_USER=root
DB_PASSWORD=P@ssw0rd
DB_HOST=mariadb
DB_NAME=loginapi
SECRET_KEY=230200495632927592
EMAIL_HOST=mailhog
EMAIL_PORT=1025
EMAIL_USER=noreply@loginapi.net
EMAIL_PASSWORD=password_fake
TOKEN_CONFIRMATION_URL=https://**loginapiIP**:8443/validar
EOF
```
! -> Cal assegurar-se que l'usuari té permisos per crear bases de dades.

## Comandes de docker per veure informació dels contenidors
### Veure llista de contenidors i el seu estat
docker container list -a

### Veure els logs d'un contenidor
docker logs {nomcontenidor}

### Aturar un contenidor
docker stop {nomcontenidor}

### Engegar un contenidor 
docker start {nomcontenidor}

## Comandes de docker-compose per aixecar o aturar conjunts de contenidors.

(Des de la carpeta on està l'arxiu docker-compose-yaml)

### Aixecar els contenidors de l'arxiu docker-compose.yaml
docker-compose up -d --build

### Aturar i eliminar els contenidors de l'arxiu docker-compose.yaml
docker-compose down


