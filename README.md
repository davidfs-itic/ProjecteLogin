# Projecte API Login:
https://github.com/davidfs-itic/ProjecteLogin


## Arxiu .env que cal copiar dins la carpeta API (no està en el git)
```
DB_USER=root
DB_PASSWORD=P@ssword
DB_HOST=mariadb
DB_NAME=loginapi
SECRET_KEY=230200495632927592
EMAIL_HOST=smtp
EMAIL_PORT=1025
EMAIL_USER=noreply@loginapi.net
EMAIL_PASSWORD=password_fake
TOKEN_CONFIRMATION_URL=https://loginapiIP:8443/validar
```

## Creació de la base de dades:
Es comprovarà que les taules existeixin en iniciar l'aplicació.
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

