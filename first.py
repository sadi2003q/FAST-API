from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hello() :  
    return {"message" : "Hello"}


@app.get("/about")
def about():
    return {'message' : "I am learning fast API using python"}



