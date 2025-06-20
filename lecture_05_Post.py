from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, AnyUrl, computed_field
from typing import Annotated, Optional, List, Dict, Any
import json



class Patient(BaseModel):
    id: Annotated[int, Field(..., ge=1, title="Patient ID", 
                             description="Unique identifier for the patient, must be a positive integer", 
                             examples=[1, 2, 3])]
    
    name: Annotated[str, Field(..., max_length=100, 
                               title="Name of the Patient", 
                               description="Name of the patient, must be a string with max length 100", 
                               examples=["Adnan Abdullah Sadi"])]
    
    gender : Annotated[str, Field(..., max_length=10)]
    email: EmailStr
    phone: Annotated[int, Field(..., ge=1000000000, le=9999999999, 
                                title="Phone Number", 
                                description="Phone number of the patient, must be a 10-digit integer", 
                                examples=[1234567890])]
    age: Annotated[int, Field(default=20, ge=0, le=120, 
                              description="Age of the patient, must be between 0 and 120", examples=[25])]
    
    weight: Annotated[Optional[float], 
                      Field(default=None, ge=0,
                             description="Weight of the patient in kg, must be a non-negative float", strict=True, examples=[70.5])]
    
    height: Annotated[float, 
                      Field(default=None, gt=0, 
                            description="Height of the patient in m, must be a non-negative float", strict=True, examples=[1.64])]
    
    

    @computed_field
    @property
    def bmi(self) -> float:
        if self.weight is None or self.height is None:
            return None # type: ignore
        return round(self.weight / (self.height ** 2), 2)

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
        

app = FastAPI()

def load_data() :
    with open('lecture_02_demoData.json', 'r') as f:
        data = json.load(f)
    return data

@app.post("/create")
def create_patient(patient: Patient):
    """
    Create a new patient record.
    """
    # check if the patient ID already exists in the database (for demonstration, we will use a simple JSON file)

    try:
        data = load_data()

        if any(p['id'] == patient.id for p in data):
            return HTTPException(status_code=400, detail="Patient ID already exists")
        data.append(patient.dict())
        with open('lecture_02_demoData.json', 'w') as f:
            json.dump(data, f, indent=4)
        return {"message": "Patient created successfully", "patient": patient}


    except FileNotFoundError:
        data = []  



    
dummy_patient = Patient(
    id=11,
    name="Adnan Abdullah",
    gender="Male",
    email="adnan@example.com",
    phone=1234567890,
    age=25,
    weight=68.5,
    height=1.75
)

result = create_patient(dummy_patient)
print(result)