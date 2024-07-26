from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError, Field
from typing import Dict, Optional

app = FastAPI()

# Route qui gère les requêtes GET
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API"}

# Route qui gère les requêtes POST
@app.post("/")
def post_root(data: Dict[str, str]):
    return {"message": "Vous avez posté", "data": data}

# Route qui prend un nombre dans la requête et retourne ce nombre multiplié par 2
@app.get("/multiply/{number}")
def multiply_by_two(number: int):
    return {"result": number * 2}

# Modèle de données pour le calcul du salaire
class SalaryData(BaseModel):
    salary: float
    bonus: float
    taxes: float

# Route POST qui prend un dictionnaire et retourne le calcul de salary + bonus - taxes
@app.post("/compute")
def compute_salary(data: SalaryData):
    return {"result": data.salary + data.bonus - data.taxes}

# Gestionnaire d'exceptions pour les erreurs de validation
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    errors = exc.errors()
    missing_fields = [e['loc'][0] for e in errors if e['type'] == 'value_error.missing']
    if missing_fields:
        return JSONResponse(
            status_code=400,
            content={"error": f"3 champs attendus (salary, bonus, taxes). Vous avez oublié: {', '.join(missing_fields)}."}
        )
    
    # Gestion des types incorrects (ex: chaînes au lieu de nombres)
    incorrect_fields = [e['loc'][0] for e in errors if e['type'] == 'type_error.float']
    if incorrect_fields:
        return JSONResponse(
            status_code=400,
            content={"error": "Champs attendus comme des nombres, mais des chaînes ont été fournies."}
        )
    
    return JSONResponse(
        status_code=422,
        content={"error": "Erreur de validation des données."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
