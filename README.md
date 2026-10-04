Travel Expense Calculator
Live app: https://travel-expense-calculator.streamlit.app/
A simple Streamlit app for calculating mileage reimbursement, per diem, pay-period expense checks, and travel projections.
Features
Editable mileage reimbursement rate
Editable per diem categories and rates
Manual round-trip mileage entry
Trip duplication and route notes
Weekly, biweekly, semi-monthly, and monthly pay frequencies
Weekdays-only or weekend-inclusive travel
Eligible travel-day safeguard
Weekly and annual projections
Future mileage-rate scenarios
Excel export
How it works
For each trip:
Total miles = round-trip miles × occurrences
Mileage reimbursement = total miles × mileage rate
Per diem = per diem rate × occurrences
Expense total = mileage reimbursement + per diem
Annual projections use the trip's Times per Week for Projection value × 52 weeks.
Travel-day safeguard
The combined total of all Times this Pay Period entries cannot exceed the number of eligible travel days in the selected pay period.
If the limit is exceeded, the app:
shows an error
blocks the pay-period calculation
disables Excel export
Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Deploy
Streamlit Community Cloud: https://share.streamlit.io/
Use `app.py` as the main file.
No API keys or secrets are required.
