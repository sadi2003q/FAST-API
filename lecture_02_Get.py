from fastapi import FastAPI
import json


app = FastAPI()


def load_data() :
    with open('lecture_02_demoData.json', 'r') as f:
        data = json.load(f)
    return data;


@app.get("/")
def hello() :  
    return {"message" : "Hello"}


@app.get('/view')
def showInfo():
    data = load_data()
    return {'Data' : data}




