from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import json


# {
#         "id": 11,
#         "name": "Adnan Abdullah",
#         "gender": "Male",
#         "email": "adnan@example.com",
#         "phone": 1234567890,
#         "age": 25,
#         "weight": 68.5,
#         "height": 1.75,
#         "bmi": 22.37,
#         "bmi_verdict": "Normal weight"
# }


class Update_Patient(BaseModel):
    name: Optional[str] = Field(None, max_length=100, title="Name of the Patient", description="Name of the patient")
    email: Optional[EmailStr] = Field(None, title="Email of the Patient", description="Email of the patient")
    phone: Optional[int] = Field(None, title="Phone Number", description="Phone number of the patient")
    age: Optional[int] = Field(None, ge=0, le=120, title="Age of the Patient", description="Age of the patient")
    weight: Optional[float] = Field(None, ge=0, description="Weight of the patient in kg")
    height: Optional[float] = Field(None, gt=0, description="Height of the patient in m")




def load_data() :
    with open('lecture_02_demoData.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)




app = FastAPI()
@app.put("/update/{patient_id}")
def update_patient(patient_id: int, patient: Update_Patient):

    data = load_data()
    if patient_id < 0 or patient_id >= len(data):
        raise HTTPException(status_code=404, detail="Patient not found")
    patient_data = data[patient_id]
    update_data = patient.dict(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            patient_data[key] = value

    patient_data['id'] = patient_id
    data[patient_id] = patient_data
    save_data(data)
    return {"message": "Patient updated successfully", "updated_patient": patient_data}






@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: int):
    data = load_data()
    if patient_id < 0 or patient_id >= len(data):
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})



