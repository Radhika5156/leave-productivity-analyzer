Frontend: Simple HTML/CSS/JS interface for file upload and result display  
Backend: FastAPI + Pandas for attendance analysis and productivity calculation
# Leave & Productivity Analyzer

This project analyzes employee attendance and productivity using an uploaded Excel sheet.

## Features
- Upload Excel (.xlsx) attendance data
- Calculates total expected work hours
- Calculates total actual hours worked
- Counts leaves used
- Computes productivity percentage

## Technology Stack
- FastAPI (Python)
- Pandas
- HTML, CSS, JavaScript

## How to Run
1. Install dependencies: `pip install fastapi uvicorn pandas openpyxl python-multipart`
2. Run backend: `uvicorn app:app`
3. Open `index.html` in browser
4. Upload sample Excel and view results

## Sample Excel Format
| Date | In-Time | Out-Time |
|------|---------|----------|
| 2025-01-01 | 10:00 | 18:30 |
| 2025-01-02 | 10:15 | 18:45 |
| 2025-01-03 |       |        |

Missing in-time/out-time is treated as a leave.



