from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import smtplib
import uuid
import mysql.connector
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from database import inicialitzar_base_dades  # Importa la funció

# Càrrega de variables d'entorn
load_dotenv()

# Configura la connexió a MariaDB
db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
    'collation': 'utf8mb4_general_ci'
}

# Inicialitza la base de dades
inicialitzar_base_dades(db_config)
    
# Configura la connexió a la base de dades
conn = conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

app = FastAPI()

# Clau secreta per a JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuració de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuració del servidor de correu
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TOKEN_CONFIRMATION_URL = os.getenv("TOKEN_CONFIRMATION_URL")

# Model per al registre d'usuaris
class UserCreate(BaseModel):
    nom_usuari: str
    email: EmailStr
    contrassenya: str

class UserLogin(BaseModel):
    email: EmailStr
    contrassenya: str

# Funció per encriptar contrasenyes
def hash_contrassenya(contrassenya: str) -> str:
    return pwd_context.hash(contrassenya)

# Funció per verificar contrasenyes
def verificar_contrassenya(contrassenya: str, hashed: str) -> bool:
    return pwd_context.verify(contrassenya, hashed)

# Generar token JWT
def crear_token_daccess(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Enviar correu de confirmació
def enviar_correu_confirmacio(email: str, token: str):
    missatge = f"Subject: Confirma el teu compte\n\nFeu clic aqui per validar el compte: {TOKEN_CONFIRMATION_URL}/{token}"
   
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            #server.starttls()
            #server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, email, missatge)
    except Exception as e:
        print("Error enviant correu:", e)

@app.post("/registre/")
def registre_usuari(usuari: UserCreate):
    token = str(uuid.uuid4())
    hashed_password = hash_contrassenya(usuari.contrassenya)
    try:
        cursor.execute(
            "INSERT INTO usuaris (nom_usuari, email, contrassenya, token, validat) VALUES (%s, %s, %s, %s, %s)",
            (usuari.nom_usuari, usuari.email, hashed_password, token, False)
        )
        conn.commit()
        enviar_correu_confirmacio(usuari.email, token)
        return {"missatge": "Usuari registrat. Comprova el teu correu per validar-lo."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    
# Endpoint per validar un usuari
@app.get("/validar/{token}")
def validar_usuari(token: str):
    cursor.execute(
        "SELECT id FROM usuaris WHERE token = %s AND validat = %s",
        (token, False)
    )
    usuari = cursor.fetchone()
    if not usuari:
        raise HTTPException(status_code=400, detail="Token invàlid o usuari ja validat")
    
    cursor.execute(
        "UPDATE usuaris SET validat = %s WHERE token = %s",
        (True, token)
    )
    conn.commit()
    return {"missatge": "Compte validat correctament."}


# Endpoint per iniciar sessió i obtenir token JWT
@app.post("/login/")
def iniciar_sessio(usuari: UserLogin):
    cursor.execute(
        "SELECT id, nom_usuari, email, contrassenya FROM usuaris WHERE email = %s AND validat = %s",
        (usuari.email, True)
    )
    usuari_db = cursor.fetchone()
    
    if not usuari_db or not verificar_contrassenya(usuari.contrassenya, usuari_db[3]):
        raise HTTPException(status_code=400, detail="Credencials incorrectes o usuari no validat")
    
    token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = crear_token_daccess({"sub": usuari_db[0]}, token_expire)
    
    return {
        "id": usuari_db[0],  # L'id és un Int (no cal convertir-lo a String)
        "nom_usuari": usuari_db[1],
        "email": usuari_db[2],
        "contrassenya": usuari_db[3],  # Incloem la contrasenya (encriptada)
        "access_token": token,  # El camp es diu "access_token" a la resposta JSON
        "token_type": "bearer"  # El camp es diu "token_type" a la resposta JSON
    }

# Endpoint protegit amb JWT
@app.get("/perfil/")
def perfil_usuari(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuari_id = payload.get("sub")
        if usuari_id is None:
            raise HTTPException(status_code=401, detail="Token invàlid")
        return {"missatge": f"Benvingut, usuari {usuari_id}"}
    except JWTError:
        raise HTTPException(status_code=401, detail="No autoritzat")
