from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
from datetime import datetime, time
import tempfile
import os

app = FastAPI()

# CORS (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_excel(file: UploadFile):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files allowed")

    try:
        df = pd.read_excel(file.file)

        required_cols = {"Date", "In-Time", "Out-Time"}
        if not required_cols.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail="Excel must contain Date, In-Time, Out-Time columns"
            )

        total_actual = 0
        total_expected = 0
        leaves = 0
        monthly_summary = {}

        for _, row in df.iterrows():
            date = pd.to_datetime(row["Date"])
            month = date.strftime("%B %Y")
            day = date.day_name()

            # Expected hours
            if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                expected = 8.5
            elif day == "Saturday":
                expected = 4
            else:
                expected = 0

            total_expected += expected
            monthly_summary.setdefault(month, {"Expected": 0, "Actual": 0})
            monthly_summary[month]["Expected"] += expected

            if pd.isna(row["In-Time"]) or pd.isna(row["Out-Time"]):
                leaves += 1
                continue

            in_t, out_t = row["In-Time"], row["Out-Time"]

            if isinstance(in_t, time):
                in_time = datetime.combine(date.date(), in_t)
                out_time = datetime.combine(date.date(), out_t)
            else:
                in_time = pd.to_datetime(in_t)
                out_time = pd.to_datetime(out_t)

            if out_time <= in_time:
                leaves += 1
                continue

            worked = (out_time - in_time).seconds / 3600
            total_actual += worked
            monthly_summary[month]["Actual"] += worked

        productivity = (total_actual / total_expected) * 100 if total_expected else 0

        #  Productivity Grade
        if productivity >= 90:
            grade = "A"
        elif productivity >= 75:
            grade = "B"
        else:
            grade = "C"

        # Create downloadable Excel report
        report_df = pd.DataFrame.from_dict(monthly_summary, orient="index")
        report_df["Productivity (%)"] = (
            report_df["Actual"] / report_df["Expected"] * 100
        ).round(2)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        report_df.to_excel(tmp.name)

        return {
            "Expected Hours": round(total_expected, 2),
            "Actual Hours": round(total_actual, 2),
            "Leaves Used": leaves,
            "Productivity (%)": round(productivity, 2),
            "Grade": grade,
            "Monthly Summary": monthly_summary,
            "report_path": tmp.name
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download")
def download_report(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        path,
        filename="Attendance_Report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

