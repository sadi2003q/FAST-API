from fastapi import FastAPI, Path, HTTPException, Query
import json




app = FastAPI();

def load_data() :
    with open('lecture_02_demoData.json', 'r') as f:
        data = json.load(f)
    return data;

# HTTP GET method to retrieve a list of patients
@app.get("/view/{patient_id}")
def view_patient(patient_id: int=Path(..., title="Patient ID", description="The ID of the patient to view", example=1)):
    data = load_data()
    if patient_id < 0 or patient_id >= len(data):
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"patient": data[patient_id]}

@app.get("/sort")
def sort_patient(
        sort_by:str = Query(..., title="Sort By", description="The field to sort patients by", example="age"), 
        order:str = (Query('asc', title="Order", description="Sort order: asc or desc", example="asc"))
    ):
    data = load_data()
    vield_field = ['age', 'name']
    if sort_by not in vield_field:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order")
    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=(order == 'desc'))
    return {"sorted_patients": sorted_data}
    






