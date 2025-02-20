# Projecte API Login:
https://github.com/davidfs-itic/ProjecteLogin


## Creació de la base de dades:
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

