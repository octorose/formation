from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import easyocr
import tempfile
from fastapi.responses import JSONResponse

app = FastAPI()

# Configuration CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Adresse de votre frontend React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

reader = easyocr.Reader(['fr'])

@app.post("/extract-ocr/")
async def extract_ocr(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            image_path = tmp.name

        image = cv2.imread(image_path)
        resultats = reader.readtext(image)

        text_image = ""
        for resultat in resultats:
            text_image += resultat[1] + "\n"

        lignes = text_image.splitlines()
        nom = ""
        prenom = ""
        date_naissance = ""
        cin = ""

        if len(lignes) > 12:
            nom = lignes[4].strip()
            prenom = lignes[5].strip()
            
            for ligne in lignes:
                if '/' in ligne:  
                    date_naissance = ligne.strip()
                    break
            cin = lignes[11].strip()

        # Remplacer les espaces par des underscores dans le login
        login = f"{nom.lower().replace(' ', '_')}{prenom.lower().replace(' ', '_')}{cin}@gmail.com"
        password = cin

        return {
            "nom": nom,
            "prenom": prenom,
            "date_naissance": date_naissance,
            "cin": cin,
            "email": login,
            "username": nom,
            "password": password
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
