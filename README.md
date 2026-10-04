🚗 Travel Expense Calculator
Live App:  
https://travel-expense-calculator.streamlit.app/
A Streamlit application for calculating and projecting travel-related reimbursements, including mileage, per diem, pay-period totals, annual expense estimates, and future mileage-rate scenarios.
---
✨ Main Features
Editable mileage reimbursement rate
Editable per diem categories and rates
Manual round-trip mileage entry
Route and location notes
Duplicate-trip option
Weekly, biweekly, semi-monthly, and monthly pay frequencies
Weekdays-only or include-weekends settings
Eligible travel-day safeguard
Pay-period expense-check estimates
Weekly reimbursement projections
Annual mileage and reimbursement projections
Future mileage-rate scenarios
Excel export
---
🌐 Live App
The deployed Travel Expense Calculator is available here:
https://travel-expense-calculator.streamlit.app/
---
▶️ Run Locally
Install the required packages:
```bash
pip install -r requirements.txt
```
Then start the app:
```bash
streamlit run app.py
```
---
📁 GitHub Setup
Upload the project files to a GitHub repository.
Keep the main project files at the repository root:
```text
app.py
requirements.txt
README.md
config.toml
```
---
☁️ Streamlit Community Cloud
Manage or redeploy the app through Streamlit Community Cloud:
https://share.streamlit.io/
Deployment Steps
Sign in with your GitHub account.
Select the GitHub repository containing the app.
Set the main file path to:
```text
app.py
```
Deploy or reboot the app as needed.
No API keys or secrets are required.
---
🧮 Calculation Logic
For each trip, the app uses the following calculations.
Total Miles
```text
Total Miles = Round-Trip Miles × Number of Occurrences
```
Mileage Reimbursement
```text
Mileage Reimbursement = Total Miles × Mileage Reimbursement Rate
```
Per Diem
```text
Per Diem Total = Per Diem Rate × Number of Occurrences
```
Total Expense Reimbursement
```text
Expense Total = Mileage Reimbursement + Per Diem
```
---
📅 Weekly and Annual Projections
Each trip includes a separate Times per Week for Projection setting.
The app uses this value to calculate:
Projected weekly miles
Projected weekly mileage reimbursement
Projected weekly per diem
Projected weekly total
Projected annual miles
Projected annual mileage reimbursement
Projected annual per diem
Projected annual total
Annual projections are based on:
```text
Weekly Projection × 52 Weeks
```
---
📈 Future Mileage-Rate Scenarios
The app can also model future reimbursement rates.
For example, if the current mileage rate is:
```text
$0.76 per mile
```
and the user assumes the rate increases by:
```text
$0.02 per mile each year
```
the app projects future mileage reimbursement amounts while keeping the same travel pattern.
These are user-defined scenarios and are not official IRS forecasts.
---
🛡️ Eligible Travel-Day Safeguard
The app calculates the number of eligible travel days in the selected pay period based on:
Pay frequency
Pay-period dates
Whether weekends are included
The combined total of all Times this Pay Period entries cannot exceed the number of eligible travel days.
Example
If a pay period contains:
```text
11 eligible travel days
```
the total number of trip occurrences entered for that pay period cannot exceed:
```text
11
```
If the limit is exceeded:
The app displays an error
The pay-period reimbursement calculation is blocked
Excel export is disabled
The user must correct the trip entries before continuing
---
📊 Excel Export
The app can generate an Excel workbook containing:
Summary
Trip setup
Pay-period trip details
Weekly projection
Future mileage-rate projection
Per diem settings
---
ℹ️ Notes
Mileage is entered manually as full round-trip mileage.
No map service or API key is required.
