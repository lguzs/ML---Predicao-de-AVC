from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import mlflow
import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MLRUNS_PATH = PROJECT_ROOT / "mlruns"

MODEL_URI = "models:/previsor_avc_stroke@production"

model = None
model_load_error = None


class PacienteInput(BaseModel):
    gender: str = Field(..., example="Female")
    age: float = Field(..., example=67.0)
    hypertension: int = Field(..., example=0)
    heart_disease: int = Field(..., example=1)
    ever_married: str = Field(..., example="Yes")
    work_type: str = Field(..., example="Private")
    Residence_type: str = Field(..., example="Urban")
    avg_glucose_level: float = Field(..., example=228.69)
    bmi: Optional[float] = Field(None, example=36.6)
    smoking_status: str = Field(..., example="formerly smoked")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, model_load_error

    try:
        tracking_uri = f"file://{MLRUNS_PATH}"

        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_registry_uri(tracking_uri)

        model = mlflow.pyfunc.load_model(MODEL_URI)
        model_load_error = None

        print(f"Modelo carregado com sucesso: {MODEL_URI}")

    except Exception as error:
        model = None
        model_load_error = str(error)
        print(f"Erro ao carregar modelo: {model_load_error}")

    yield


app = FastAPI(
    title="API de Previsão de AVC",
    description="Endpoint para previsão de AVC usando modelo registrado no MLflow.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/saude")
def saude():
    if model is None:
        raise HTTPException(
            status_code=500,
            detail={
                "ok": False,
                "modelo": MODEL_URI,
                "erro": model_load_error
            }
        )

    return {
        "ok": True,
        "modelo": MODEL_URI
    }


@app.post("/predict")
def predict(dados: PacienteInput):
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Modelo não foi carregado corretamente."
        )

    try:
        input_df = pd.DataFrame([dados.model_dump()])

        prediction = model.predict(input_df)

        prediction_value = int(prediction[0])

        label = "Com AVC" if prediction_value == 1 else "Sem AVC"

        return {
            "prediction": prediction_value,
            "label": label,
            "modelo": MODEL_URI
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao realizar predição: {str(error)}"
        )