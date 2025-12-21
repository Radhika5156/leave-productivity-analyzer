from fastapi import FastAPI, UploadFile
import pandas as pd
from datetime import datetime

app = FastAPI()

@app.post("/upload")
async def upload_excel(file: UploadFile):
    df = pd.read_excel(file.file)

    total_actual_hours = 0
    total_expected_hours = 0
    leaves = 0

    for _, row in df.iterrows():
        date = pd.to_datetime(row['Date'])
        day = date.day_name()

        # Expected hours
        if day in ['Monday','Tuesday','Wednesday','Thursday','Friday']:
            expected = 8.5
        elif day == 'Saturday':
            expected = 4
        else:
            expected = 0

        total_expected_hours += expected

        # Leave check
        if pd.isna(row['In-Time']) or pd.isna(row['Out-Time']):
            leaves += 1
            continue

        # ✅ FIX: Combine date + time correctly
        in_time = datetime.combine(date.date(), row['In-Time'])
        out_time = datetime.combine(date.date(), row['Out-Time'])

        worked = (out_time - in_time).seconds / 3600
        total_actual_hours += worked

    productivity = (total_actual_hours / total_expected_hours) * 100 if total_expected_hours else 0

    return {
        "Expected Hours": round(total_expected_hours, 2),
        "Actual Hours": round(total_actual_hours, 2),
        "Leaves Used": leaves,
        "Productivity (%)": round(productivity, 2)
    }
