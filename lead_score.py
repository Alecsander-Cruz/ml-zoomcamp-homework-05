import requests

url='https://fragrant-meadow-3771.fly.dev/predict_lead_score'

customer = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}

response = requests.post(url, json=customer)

score = response.json()

print(f'lead score = {score}')