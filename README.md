# Projecte API Login:
https://github.com/davidfs-itic/ProjecteLogin

## Descarregar el projecte en el servidor amb un:
```
cd /opt/docker
git clone https://github.com/davidfs-itic/ProjecteLogin
```


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
TOKEN_CONFIRMATION_URL=https://loginapiIP:8443/validar
EOF
```
! -> Cal assegurar-se que l'usuari té permisos per crear bases de dades.

## Executar l'aplicació en un contenidor de docker, i comprovar que està funcionant

Executem les comandes seguents:
```
cd ProjecteLogin
docker-compose up -d --build
docker logs loginapi
```
En el log del contenidor, haurem de veure els missatges de èxit o error en la comprovació de la base de dades.


## Informació addiccional:

### Taules de la base de dades:

Les taules requerides són:
```
mysql -u root -p -h 127.0.0.1 -e "
CREATE DATABASE IF NOT EXISTS loginapi;
USE loginapi;
CREATE TABLE IF NOT EXISTS usuaris (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_usuari VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    contrassenya VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    validat BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS passwords (flag VARCHAR(100));
INSERT INTO passwords (flag) VALUES ('It was good that all beautiful things were also a little sad. It made them seem more real.');
"
```

### Servidor de correu de proves mailhog

Si observem el docker-compose.yaml, veurem que es crea un segon contenidor. És un servidor smtp per rebre els missatges de la api, i que té una interfície web per a veure'ls.

Utilitza el port 1025 com servidor smtp, i el 8025 com servidor web per veure els missatages.

Si voleu consultar els missatges enviats des de l'api, us heu de connectar al port 8025, hi ha 2 opcions:

#### Opció 1, obrir el port en aws

Com que hi ha un firewall en cada instància que bloqueja la majoria de ports, cal editar el Security Group corresponent i afegir el port 8025

#### Opció 2, utilitzar ssh local port forwarding.
**
El servei ssh permet crear un tunel d'un port local a un port remot, de la seguent manera:

ssh -i labuser.pem ubuntu@ip.del.servidor.ssh  -L **127.0.0.1:8025**:_127.0.0.1:8025_

Mentre duri la connexió ssh, el port del vostre ordinador local **127.0.0.1:8025** es redirigirà al port de l'ordinador remot _127.0.0.1:8025_
Per tant, mentre estigueu connectats per ssh amb el port forwarding, podeu apuntar el vostre navegador a 127.0.0.1:8025 i veureu el mailhog del servidor.
