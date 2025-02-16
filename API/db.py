import mysql.connector
import os
from dotenv import load_dotenv

# Carregar variables d'entorn
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
}

def get_db():
    """ Retorna una connexió a la base de dades MariaDB """
    return mysql.connector.connect(**DB_CONFIG)

def insert_user(nom_usuari, email, hashed_password, token_validacio):
    """ Insereix un nou usuari a la base de dades """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuaris (nom_usuari, email, contrassenya, token_validacio, validat) VALUES (%s, %s, %s, %s, %s)",
        (nom_usuari, email, hashed_password, token_validacio, False),
    )
    db.commit()
    db.close()

def get_user_by_email(email):
    """ Retorna un usuari donat un email """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuaris WHERE email = %s", (email,))
    user = cursor.fetchone()
    db.close()
    return user

def validate_user(token):
    """ Marca un usuari com a validat si el token és correcte """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE usuaris SET validat = TRUE WHERE token_validacio = %s AND validat = FALSE", (token,))
    db.commit()
    db.close()
    return cursor.rowcount > 0  # Retorna True si s'ha validat correctament
