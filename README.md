Travel Expense Calculator
Live App: https://travel-expense-calculator.streamlit.app/
A Streamlit app for manually entering round-trip travel mileage and projecting travel reimbursements.
Main features
Editable mileage reimbursement rate
Editable per diem categories
Manual round-trip mileage
Route/location notes
Duplicate trips
Weekly, biweekly, semi-monthly, and monthly pay frequencies
Weekdays-only or include-weekends setting
Eligible travel-day safeguard
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
Streamlit App
The deployed Travel Expense Calculator is available here:
https://travel-expense-calculator.streamlit.app/
Streamlit Community Cloud
To manage or redeploy the app:
https://share.streamlit.io/
Sign in with GitHub.
Select the GitHub repository for this project.
Set the main file path to `app.py`.
Deploy or reboot the app as needed.
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
For the selected pay period, the app calculates the number of eligible travel days based on the pay-period dates and whether weekends are included.
The combined total of all `Times this pay period` entries cannot exceed the eligible-day count. If it does:
the app displays an error
the pay-period calculation is blocked
Excel export is disabled until the entries are corrected
