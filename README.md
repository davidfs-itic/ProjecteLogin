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
