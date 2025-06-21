from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import Optional, Annotated
from fastapi.responses import JSONResponse
import json 

app = FastAPI()

#     "id": 7,
#     "name": "Sarah Davis",
#     "age": 36,
#     "gender": "Female",
#     "height_cm": 162,
#     "weight_kg": 58,
#     "bmi": 22.10,
#     "diseases": ["Thyroid Disorder"],
#     "city": "San Antonio",
#     "admitted_date": "2023-10-20"

class Patient(BaseModel):
    id: Annotated[int, Field(..., ge=1, title="Patient ID", description="Unique identifier for the patient")]
    name: Annotated[str, Field(..., max_length=100, title="Name of the Patient", description="Name of the patient")]
    age: Annotated[int, Field(..., ge=0, le=120, title="Age of the Patient", description="Age of the patient")]
    gender: Annotated[str, Field(..., max_length=10, title="Gender of the Patient" )]
    height_cm: Annotated[float, Field(..., gt=0, title="Height in cm", description="Height of the patient in centimeters")]
    weight_kg: Annotated[float, Field(..., gt=0, title="Weight in kg", description="Weight of the patient in kilograms")]
    diseases: Optional[list[str]] = Field(default=None, title="List of Diseases", description="List of diseases the patient has")
    city: Annotated[str, Field(..., max_length=100, title="City of Residence", description="City where the patient resides")]
    admitted_date: Annotated[Optional[str], Field(..., title="Date of Admission", description="Date when the patient was admitted to the hospital in YYYY-MM-DD format")]


    # Computed fields for BMI and BMI verdict
    @computed_field
    @property
    def bmi(self) -> float:
        if self.weight_kg is None or self.height_cm is None:
            return None # type: ignore
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)
    
    # Computed field for BMI verdict
    @computed_field
    @property
    def bmi_verdict(self) -> str:
        if self.bmi is None:
            return "BMI not available"
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"









# class for create new Patient
class Create_patient(BaseModel):
    name: Annotated[Optional[str], Field(..., max_length=100, title="Name of the Patient", description="Name of the patient")]
    age: Annotated[Optional[int], Field(..., ge=0, le=120, title="Age of the Patient", description="Age of the patient")]
    gender: Annotated[Optional[str], Field(..., max_length=10, title="Gender of the Patient" )]
    height_cm: Annotated[Optional[float], Field(..., gt=0, title="Height in cm", description="Height of the patient in centimeters")]
    weight_kg: Annotated[Optional[float], Field(..., gt=0, title="Weight in kg", description="Weight of the patient in kilograms")]
    diseases: Annotated[Optional[list[str]], Field(default=None, title="List of Diseases", description="List of diseases the patient has")]
    city: Annotated[Optional[str], Field(..., max_length=100, title="City of Residence", description="City where the patient resides")]
    admitted_date: Annotated[Optional[str], Field(..., title="Date of Admission", description="Date when the patient was admitted to the hospital in YYYY-MM-DD format")]












# loading data from json file
def load_data():
    with open('database.json', 'r') as f:
        data = json.load(f)
    return data


# saving data to json file
def save_data(data):
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=4)


# Retrieve Data from Database
@app.get("/show")
def show_data():
    data = load_data()
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
    return {"data": data}


# create ne patient
@app.post("/create")
def create_patient(patient: Patient):
    """
    Create a new patient record.
    """
    data = load_data()
    
    # Check if the patient ID already exists in the database
    if any(p['id'] == patient.id for p in data):
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    
    # Append the new patient data to the existing data
    data.append(patient.dict())
    
    # Save the updated data back to the JSON file
    save_data(data)
    
    return {"message": "Patient created successfully", "patient": patient}



# update existing patient
@app.put("/update/{patient_id}")
def update_patient(patient_id: int, patient: Create_patient):
    """
    Update an existing patient record.
    """
    data = load_data()
    
    # Check if the patient ID exists in the database
    if patient_id < 1 or patient_id > len(data):
        raise HTTPException(status_code=404, detail="Patient not found")
    
    current_patient = data[patient_id]
    update_data = patient.dict(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            current_patient[key] = value
    current_patient['id'] = patient_id


    patient_pydandic_obj = Patient(**existing_patient_info)
    existing_patient_info = patient_pydandic_obj.model_dump()
    data[patient_id] = existing_patient_info



    # Save the updated data back to the JSON file
    save_data(data)
    return {"message": "Patient updated successfully", "updated_patient": current_patient}



# delete existing patient
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: int):
    """
    Delete an existing patient record.
    """
    data = load_data()
    
    # Check if the patient ID exists in the database
    if patient_id < 1 or patient_id > len(data):
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Remove the patient from the data
    del data[patient_id]
    
    # Save the updated data back to the JSON file
    save_data(data)
    
    return {"message": "Patient deleted successfully"}