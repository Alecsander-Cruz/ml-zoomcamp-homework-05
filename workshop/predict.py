import pickle

from typing import Dict, Any

import uvicorn
from fastapi import FastAPI

from pydantic import BaseModel, Field, conint, confloat
from typing import Literal


# request

class Customer(BaseModel):
    """
    A single Pydantic class to validate telecom customer data
    using Literal types based on provided statistics.
    """
    
    # --- Customer Demographics ---
    gender: Literal["male", "female"]
    seniorcitizen: Literal[0, 1]
    partner: Literal["yes", "no"]
    dependents: Literal["yes", "no"]
    
    # --- Account & Services ---
    phoneservice: Literal["yes", "no"]
    multiplelines: Literal["no", "yes", "no_phone_service"]
    internetservice: Literal["fiber_optic", "dsl", "no"]
    onlinesecurity: Literal["no", "yes", "no_internet_service"]
    onlinebackup: Literal["no", "yes", "no_internet_service"]
    deviceprotection: Literal["no", "yes", "no_internet_service"]
    techsupport: Literal["no", "yes", "no_internet_service"]
    streamingtv: Literal["no", "yes", "no_internet_service"]
    streamingmovies: Literal["no", "yes", "no_internet_service"]
    
    # --- Contract & Billing ---
    contract: Literal["month-to-month", "two_year", "one_year"]
    paperlessbilling: Literal["yes", "no"]
    paymentmethod: Literal[
        "electronic_check",
        "mailed_check",
        "bank_transfer_(automatic)",
        "credit_card_(automatic)"
    ]
    
    # --- Charges & Tenure ---
    # Using Field validation based on the statistical minimums
    tenure: conint(ge=0)
    monthlycharges: confloat(ge=0.0)
    totalcharges: confloat(ge=0.0)


#response

class PredictResponse(BaseModel):
    churn_probability: float
    churn: bool


app = FastAPI(title='churn-prediction')



with open('model.bin', 'rb') as f_in:
   pipeline = pickle.load(f_in)


def predict_single(customer):
    
    result = pipeline.predict_proba(customer)[0,1]
    return float(result)


@app.post('/predict')
def predict(customer:Customer) -> PredictResponse:
    
    prob = predict_single(customer.dict())

    return PredictResponse(
        churn_probability=prob,
        churn=bool(prob>=0.5)
    )

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9696)
