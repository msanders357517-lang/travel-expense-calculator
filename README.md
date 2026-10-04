# Travel Expense Calculator

A Streamlit app for manually entering round-trip travel mileage and projecting travel reimbursements.

## Main features

- Editable mileage reimbursement rate
- Editable per diem categories
- Manual round-trip mileage
- Route/location notes
- Duplicate trips
- Weekly, biweekly, semi-monthly, and monthly pay frequencies
- Weekdays-only or include-weekends setting
- Pay-period expense-check estimate
- Weekly reimbursement projection
- Annual miles and reimbursement projection
- Future mileage-rate scenarios
- Excel export

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub

Upload the project files to a GitHub repository. Keep `app.py` and `requirements.txt` at the repository root.

## Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud.
2. Create a new app.
3. Select this GitHub repository.
4. Set the main file path to `app.py`.
5. Deploy.

No API keys or secrets are required.

## Calculation logic

For each trip:

`total miles = round-trip miles × occurrences`

`mileage reimbursement = total miles × mileage reimbursement rate`

`per diem = per diem rate × occurrences`

`expense total = mileage reimbursement + per diem`

Annual projections use the trip's separate `Times per week for projection` value × 52 weeks.

Future mileage-rate projections keep the mileage pattern constant and change only the assumed reimbursement rate.
