from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import easyocr
from fastapi.responses import JSONResponse
import tempfile

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
        datenaissance = ""
        NumCin = ""

        if len(lignes) > 12:
            nom = lignes[4].strip()
            prenom = lignes[5].strip()

            for ligne in lignes:
                if '/' in ligne:  
                    datenaissance = ligne.strip()
                    break
            NumCin = lignes[11].strip()

        # Remplacer les espaces par des underscores dans le login
        login = f"{nom.lower().replace(' ', '_')}{prenom.lower().replace(' ', '_')}{NumCin}@gmail.com"
        password = f"{NumCin}{nom}"

        return {
            #"text_image": text_image,
            "nom": nom,
            "prenom": prenom,
            "Date Naissance": datenaissance,
            "Numero Cin": NumCin,
            "Email": login,
            "username": nom,
            "password": password
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
