Travel Expense Calculator
A Streamlit app for manually entering round-trip travel mileage and projecting travel reimbursements.
Main features
Editable mileage reimbursement rate
Editable per diem categories
Manual round-trip mileage
Route/location notes
Duplicate trips
Weekly, biweekly, semi-monthly, and monthly pay frequencies
Weekdays-only or include-weekends setting
Pay-period expense-check estimate
Weekly reimbursement projection
Annual miles and reimbursement projection
Future mileage-rate scenarios
Excel export
Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
GitHub
Upload the project files to a GitHub repository. Keep `app.py` and `requirements.txt` at the repository root.
Streamlit Community Cloud
Sign in to Streamlit Community Cloud.
Create a new app.
Select this GitHub repository.
Set the main file path to `app.py`.
Deploy.
No API keys or secrets are required.
Calculation logic
For each trip:
`total miles = round-trip miles × occurrences`
`mileage reimbursement = total miles × mileage reimbursement rate`
`per diem = per diem rate × occurrences`
`expense total = mileage reimbursement + per diem`
Annual projections use the trip's separate `Times per week for projection` value × 52 weeks.
Future mileage-rate projections keep the mileage pattern constant and change only the assumed reimbursement rate.

Eligible travel-day safeguard
The combined total of all `Times this pay period` entries cannot exceed the number of eligible travel days in the selected period. If the total is too high, the app displays an error and disables the pay-period export until the entries are corrected.
