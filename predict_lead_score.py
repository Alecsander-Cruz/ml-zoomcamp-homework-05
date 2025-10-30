import pickle

from typing import Dict, Any

import uvicorn
from fastapi import FastAPI


app = FastAPI(title='lead-score-prediction')

with open('pipeline_v1.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)



@app.post('/predict_lead_score')
def predict_lead_score(customer: Dict[str, Any]) -> float:
    result = pipeline.predict_proba([customer])[0,1]
    return float(result)



if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9696)