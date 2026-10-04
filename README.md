# Travel Expense Calculator

[Open the live app](https://travel-expense-calculator.streamlit.app/)

A Streamlit app for calculating mileage reimbursement, per diem, pay-period expense checks, and travel projections.

## Features

- Editable mileage reimbursement rate
- Editable per diem categories and rates
- Manual round-trip mileage entry
- Duplicate trips
- Route and location notes
- Weekly, biweekly, semi-monthly, and monthly pay frequencies
- Weekdays-only or weekend-inclusive travel
- Eligible travel-day safeguard
- Weekly and annual projections
- Future mileage-rate scenarios
- Excel export

## Calculation

**Total miles**  
Round-trip miles × number of trips

**Mileage reimbursement**  
Total miles × mileage rate

**Per diem**  
Per diem rate × number of trips

**Expense check**  
Mileage reimbursement + per diem

## Travel-Day Safeguard

The total number of trips entered for a pay period cannot exceed the number of eligible travel days.

If the limit is exceeded, the app will:

- Show an error
- Stop the pay-period calculation
- Disable Excel export until corrected

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Use [Streamlit Community Cloud](https://share.streamlit.io/) and select `app.py` as the main file.

No API keys are required.
