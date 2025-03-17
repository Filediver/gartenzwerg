# start.py
import os
import subprocess
from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn

app = FastAPI()

# Einfacher GET-Endpunkt zum Testen
@app.get("/")
async def root():
    return {"message": "Hallo Welt"}

# Pfad zur Workflow-Datei
WORKFLOW_FILE = "comfyui/gartenzwerg_workflow.json"

def run_workflow(image_path: str) -> str:
    """
    Führt den ComfyUI-Workflow aus.
    Aktuell simuliert diese Funktion den Workflow-Aufruf.
    Später können hier zusätzliche Parameter (z. B. den Bildpfad) übergeben werden.
    """
    # Prüfen, ob die Workflow-Datei existiert
    if not os.path.exists(WORKFLOW_FILE):
        raise Exception(f"Workflow-Datei '{WORKFLOW_FILE}' wurde nicht gefunden!")
    
    try:
        print("Starte den Workflow...")
        # Starte das Launch-Skript in comfyui mit dem Workflow als Argument.
        result = subprocess.run(
            ["python3", "comfyui/launch.py", "--workflow", WORKFLOW_FILE],
            check=True,
            capture_output=True,
            text=True
        )
        print("Workflow-Ausgabe:")
        print(result.stdout)
        
        # Simulation: Wir gehen davon aus, dass das Ergebnisbild unter "output_image.jpg" gespeichert wird.
        output_image_path = "output_image.jpg"
        return output_image_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Fehler beim Starten des Workflows: {e.stderr}")

@app.post("/generate")
async def generate(file: UploadFile = File(...)):
    """
    Endpunkt, um ein Bild zu empfangen und den Workflow auszulösen.
    """
    print("POST /generate empfangen!")
    # Speichern des hochgeladenen Bildes in einer temporären Datei
    temp_image_path = "temp_input.jpg"
    try:
        with open(temp_image_path, "wb") as f:
            content = await file.read()
            f.write(content)
        print("Datei gespeichert:", temp_image_path)
    except Exception as ex:
        print("Fehler beim Speichern der Datei:", ex)
        raise HTTPException(status_code=500, detail=f"Fehler beim Speichern des Bildes: {str(ex)}")
    
    # Workflow ausführen
    try:
        output_path = run_workflow(temp_image_path)
        print("Workflow ausgeführt, Ergebnis:", output_path)
    except Exception as ex:
        print("Fehler im Workflow:", ex)
        raise HTTPException(status_code=500, detail=str(ex))
    
    return {"output_image": output_path}

if __name__ == "__main__":
    # Starte den HTTP-Server auf Port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
