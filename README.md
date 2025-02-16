# Projecte API Login:


## Creació de la base de dades:
```
CREATE TABLE usuaris (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_usuari VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contrassenya VARCHAR(255) NOT NULL,
    token_validacio VARCHAR(255) NOT NULL,
    validat BOOLEAN DEFAULT FALSE
); 

CREATE TABLE passwords(flag VARCHAR(100));
```

