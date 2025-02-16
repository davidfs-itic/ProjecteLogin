from fastapi import FastAPI, HTTPException, Depends
import bcrypt
import uuid
import os
import jwt
import datetime
from dotenv import load_dotenv
import aiosmtplib
from email.mime.text import MIMEText
from db import insert_user, get_user_by_email, validate_user
from fastapi.security import OAuth2PasswordBearer

# Carregar variables d'entorn
load_dotenv()

# Configuració JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Configuració del correu electrònic
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Inicialitzar FastAPI
app = FastAPI()

# Funció per enviar correus electrònics
async def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    await aiosmtplib.send(
        msg,
        hostname=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_USER,
        password=EMAIL_PASS,
        use_tls=True,
    )

# Endpoint per a registrar un usuari
@app.post("/register/")
async def register_user(nom_usuari: str, email: str, contrassenya: str):
    existing_user = get_user_by_email(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Aquest email ja està registrat.")

    hashed_password = bcrypt.hashpw(contrassenya.encode("utf-8"), bcrypt.gensalt())
    validation_token = str(uuid.uuid4())

    insert_user(nom_usuari, email, hashed_password, validation_token)

    validation_link = f"http://localhost:8000/validate/{validation_token}"
    await send_email(email, "Validació del compte", f"Fes clic per validar el teu compte: {validation_link}")

    return {"message": "Usuari registrat! Comprova el teu correu per validar-lo."}

# Endpoint per a validar un usuari
@app.get("/validate/{token}")
def validate_user_endpoint(token: str):
    if validate_user(token):
        return {"message": "Usuari validat correctament!"}
    else:
        raise HTTPException(status_code=400, detail="Token invàlid o usuari ja validat.")

# Endpoint per a iniciar sessió i obtenir un token JWT
@app.post("/login/")
def login(email: str, contrassenya: str):
    user = get_user_by_email(email)
    if not user or not user["validat"]:
        raise HTTPException(status_code=401, detail="Usuari no validat o inexistent.")

    if not bcrypt.checkpw(contrassenya.encode("utf-8"), user["contrassenya"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Credencials incorrectes.")

    # Generar token JWT
    token_data = {
        "sub": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}


# Endpoint on cal estar autenticat per accedir-hi
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Desxifra el token JWT i retorna l'email de l'usuari autenticat"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token caducat")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invàlid")

@app.get("/perfil/")
def perfil_usuari(email: str = Depends(get_current_user)):
    """Endpoint protegit: només es pot accedir si es té un token vàlid"""
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return {"nom_usuari": user["nom_usuari"], "email": user["email"]}