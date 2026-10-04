
import io
import calendar
from copy import deepcopy
from datetime import date, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Travel Expense Calculator",
    page_icon="🚗",
    layout="wide",
)

DEFAULT_PER_DIEM = pd.DataFrame(
    [
        {"Category": "Short day", "Rate": 12.75},
        {"Category": "Long day", "Rate": 34.00},
        {"Category": "Overnight - return next day", "Rate": 85.00},
        {"Category": "Full overnight", "Rate": 100.00},
    ]
)

PAY_PERIODS_PER_YEAR = {
    "Weekly": 52,
    "Biweekly": 26,
    "Semi-monthly": 24,
    "Monthly": 12,
}

if "mileage_rate" not in st.session_state:
    st.session_state.mileage_rate = 0.76
if "per_diem_df" not in st.session_state:
    st.session_state.per_diem_df = DEFAULT_PER_DIEM.copy()
if "trips" not in st.session_state:
    st.session_state.trips = []
if "next_trip_id" not in st.session_state:
    st.session_state.next_trip_id = 1


def money(value):
    return f"${value:,.2f}"


def new_trip(seed=None):
    seed = seed or {}
    trip_id = st.session_state.next_trip_id
    st.session_state.next_trip_id += 1
    return {
        "id": trip_id,
        "name": seed.get("name", f"Trip {trip_id}"),
        "route_notes": seed.get("route_notes", ""),
        "round_trip_miles": float(seed.get("round_trip_miles", 0.0)),
        "times_pay_period": int(seed.get("times_pay_period", 1)),
        "times_per_week": float(seed.get("times_per_week", 1.0)),
        "per_diem_category": seed.get("per_diem_category", "Short day"),
    }


if not st.session_state.trips:
    st.session_state.trips.append(new_trip())


def pay_period_dates(anchor_date, frequency):
    if frequency == "Weekly":
        return anchor_date, anchor_date + timedelta(days=6)
    if frequency == "Biweekly":
        return anchor_date, anchor_date + timedelta(days=13)
    if frequency == "Semi-monthly":
        if anchor_date.day <= 15:
            return anchor_date.replace(day=1), anchor_date.replace(day=15)
        last_day = calendar.monthrange(anchor_date.year, anchor_date.month)[1]
        return anchor_date.replace(day=16), anchor_date.replace(day=last_day)
    if frequency == "Monthly":
        first = anchor_date.replace(day=1)
        last_day = calendar.monthrange(anchor_date.year, anchor_date.month)[1]
        return first, anchor_date.replace(day=last_day)
    return anchor_date, anchor_date


def eligible_days(start_date, end_date, include_weekends):
    days = []
    d = start_date
    while d <= end_date:
        if include_weekends or d.weekday() < 5:
            days.append(d)
        d += timedelta(days=1)
    return days


def per_diem_rate_map():
    df = st.session_state.per_diem_df.copy()
    df["Category"] = df["Category"].astype(str).str.strip()
    df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce").fillna(0.0)
    df = df[df["Category"] != ""]
    return dict(zip(df["Category"], df["Rate"]))


def build_pay_period_rows(mileage_rate):
    rates = per_diem_rate_map()
    rows = []
    for trip in st.session_state.trips:
        miles_per_trip = float(trip["round_trip_miles"])
        occurrences = max(0, int(trip["times_pay_period"]))
        per_diem_rate = float(rates.get(trip["per_diem_category"], 0.0))
        total_miles = miles_per_trip * occurrences
        mileage_reimbursement = total_miles * mileage_rate
        per_diem_total = per_diem_rate * occurrences
        rows.append(
            {
                "Trip": trip["name"],
                "Round-trip miles": miles_per_trip,
                "Occurrences": occurrences,
                "Total miles": total_miles,
                "Mileage reimbursement": mileage_reimbursement,
                "Per diem": per_diem_total,
                "Total": mileage_reimbursement + per_diem_total,
            }
        )
    return rows


def build_weekly_rows(mileage_rate):
    rates = per_diem_rate_map()
    rows = []
    for trip in st.session_state.trips:
        miles_per_trip = float(trip["round_trip_miles"])
        occurrences = max(0.0, float(trip["times_per_week"]))
        per_diem_rate = float(rates.get(trip["per_diem_category"], 0.0))
        total_miles = miles_per_trip * occurrences
        mileage_reimbursement = total_miles * mileage_rate
        per_diem_total = per_diem_rate * occurrences
        rows.append(
            {
                "Trip": trip["name"],
                "Weekly occurrences": occurrences,
                "Weekly miles": total_miles,
                "Mileage reimbursement": mileage_reimbursement,
                "Per diem": per_diem_total,
                "Weekly total": mileage_reimbursement + per_diem_total,
            }
        )
    return rows


def summarize(rows, miles_key, mileage_key, per_diem_key, total_key):
    return {
        "miles": sum(float(r[miles_key]) for r in rows),
        "mileage": sum(float(r[mileage_key]) for r in rows),
        "per_diem": sum(float(r[per_diem_key]) for r in rows),
        "total": sum(float(r[total_key]) for r in rows),
    }


def annual_projection_from_weekly(mileage_rate):
    weekly_rows = build_weekly_rows(mileage_rate)
    weekly = summarize(
        weekly_rows,
        "Weekly miles",
        "Mileage reimbursement",
        "Per diem",
        "Weekly total",
    )
    return {
        "weekly": weekly,
        "annual_miles": weekly["miles"] * 52,
        "annual_mileage": weekly["mileage"] * 52,
        "annual_per_diem": weekly["per_diem"] * 52,
        "annual_total": weekly["total"] * 52,
    }


def build_future_rate_projection(base_rate, annual_increase, years):
    rows = []
    for i in range(years + 1):
        year = date.today().year + i
        rate = base_rate + annual_increase * i
        annual = annual_projection_from_weekly(rate)
        rows.append(
            {
                "Year": year,
                "Mileage rate": rate,
                "Weekly miles": annual["weekly"]["miles"],
                "Weekly mileage reimbursement": annual["weekly"]["mileage"],
                "Weekly per diem": annual["weekly"]["per_diem"],
                "Weekly total": annual["weekly"]["total"],
                "Projected annual miles": annual["annual_miles"],
                "Projected annual mileage reimbursement": annual["annual_mileage"],
                "Projected annual per diem": annual["annual_per_diem"],
                "Projected annual total": annual["annual_total"],
            }
        )
    return rows


def make_excel_export(
    pay_period_rows,
    weekly_rows,
    future_rows,
    pay_frequency,
    period_start,
    period_end,
    include_weekends,
    taxable_per_diem,
):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        wb = writer.book

        header_fmt = wb.add_format(
            {
                "bold": True,
                "bg_color": "#1F4E78",
                "font_color": "white",
                "border": 1,
            }
        )
        money_fmt = wb.add_format({"num_format": "$#,##0.00"})
        miles_fmt = wb.add_format({"num_format": "0.0"})
        rate_fmt = wb.add_format({"num_format": "$0.000"})

        pay_df = pd.DataFrame(pay_period_rows)
        weekly_df = pd.DataFrame(weekly_rows)
        future_df = pd.DataFrame(future_rows)

        pay_summary = summarize(
            pay_period_rows,
            "Total miles",
            "Mileage reimbursement",
            "Per diem",
            "Total",
        )
        annual = annual_projection_from_weekly(st.session_state.mileage_rate)

        summary_df = pd.DataFrame(
            [
                ["Pay frequency", pay_frequency],
                ["Pay period start", period_start],
                ["Pay period end", period_end],
                ["Weekends included", include_weekends],
                ["Mileage rate", st.session_state.mileage_rate],
                ["Total miles in pay period", pay_summary["miles"]],
                ["Mileage reimbursement", pay_summary["mileage"]],
                [
                    "Per diem" + (" (taxable)" if taxable_per_diem else ""),
                    pay_summary["per_diem"],
                ],
                ["Expense check total", pay_summary["total"]],
                ["Projected weekly miles", annual["weekly"]["miles"]],
                ["Projected weekly total", annual["weekly"]["total"]],
                ["Projected annual miles", annual["annual_miles"]],
                ["Projected annual mileage reimbursement", annual["annual_mileage"]],
                ["Projected annual per diem", annual["annual_per_diem"]],
                ["Projected annual total", annual["annual_total"]],
            ],
            columns=["Metric", "Value"],
        )

        trip_setup = pd.DataFrame(
            [
                {
                    "Trip": t["name"],
                    "Route / notes": t["route_notes"],
                    "Round-trip miles": t["round_trip_miles"],
                    "Times this pay period": t["times_pay_period"],
                    "Times per week for projection": t["times_per_week"],
                    "Per diem category": t["per_diem_category"],
                }
                for t in st.session_state.trips
            ]
        )

        settings_df = st.session_state.per_diem_df.copy()

        summary_df.to_excel(writer, index=False, sheet_name="Summary")
        trip_setup.to_excel(writer, index=False, sheet_name="Trip Setup")
        pay_df.to_excel(writer, index=False, sheet_name="Pay Period Trips")
        weekly_df.to_excel(writer, index=False, sheet_name="Weekly Projection")
        future_df.to_excel(writer, index=False, sheet_name="Future Rate Projection")
        settings_df.to_excel(writer, index=False, sheet_name="Per Diem Settings")

        for sheet_name, df in [
            ("Trip Setup", trip_setup),
            ("Pay Period Trips", pay_df),
            ("Weekly Projection", weekly_df),
            ("Future Rate Projection", future_df),
            ("Per Diem Settings", settings_df),
        ]:
            ws = writer.sheets[sheet_name]
            for col_num, col_name in enumerate(df.columns):
                ws.write(0, col_num, col_name, header_fmt)
                width = max(len(str(col_name)) + 2, 14)
                ws.set_column(col_num, col_num, min(width, 34))

        ws = writer.sheets["Summary"]
        ws.write(0, 0, "Metric", header_fmt)
        ws.write(0, 1, "Value", header_fmt)
        ws.set_column("A:A", 38)
        ws.set_column("B:B", 22)

        if not pay_df.empty:
            ws = writer.sheets["Pay Period Trips"]
            ws.set_column("B:B", 18, miles_fmt)
            ws.set_column("D:D", 16, miles_fmt)
            for col in ["E", "F", "G"]:
                ws.set_column(f"{col}:{col}", 21, money_fmt)

        if not weekly_df.empty:
            ws = writer.sheets["Weekly Projection"]
            ws.set_column("C:C", 16, miles_fmt)
            for col in ["D", "E", "F"]:
                ws.set_column(f"{col}:{col}", 21, money_fmt)

        if not future_df.empty:
            ws = writer.sheets["Future Rate Projection"]
            ws.set_column("B:B", 14, rate_fmt)
            ws.set_column("C:C", 16, miles_fmt)
            ws.set_column("G:G", 19, miles_fmt)
            for col in ["D", "E", "F", "H", "I", "J"]:
                ws.set_column(f"{col}:{col}", 24, money_fmt)

    output.seek(0)
    return output.getvalue()


st.title("🚗 Travel Expense Calculator")
st.caption(
    "Manual-mileage Streamlit app for mileage reimbursement, per diem, pay-period checks, "
    "weekly projections, annual projections, and future mileage-rate scenarios."
)

with st.container(border=True):
    st.subheader("1. Reimbursement & pay settings")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.session_state.mileage_rate = st.number_input(
            "Mileage reimbursement rate ($/mile)",
            min_value=0.0,
            value=float(st.session_state.mileage_rate),
            step=0.01,
            format="%.3f",
        )
    with c2:
        pay_frequency = st.selectbox(
            "Pay frequency",
            ["Weekly", "Biweekly", "Semi-monthly", "Monthly"],
            index=2,
        )
    with c3:
        anchor_date = st.date_input("Pay-period anchor date", value=date.today())
    with c4:
        include_weekends = st.toggle("Include weekends", value=False)

    c5, c6, c7 = st.columns(3)
    with c5:
        taxable_per_diem = st.toggle(
            "Label per diem as taxable",
            value=True,
            help="Display setting only. Actual tax treatment depends on your reimbursement arrangement.",
        )
    with c6:
        annual_rate_increase = st.number_input(
            "Future mileage rate increase ($/mile/year)",
            min_value=0.0,
            value=0.02,
            step=0.01,
            format="%.3f",
        )
    with c7:
        future_years = st.slider("Future-rate projection years", 1, 10, 5)

    period_start, period_end = pay_period_dates(anchor_date, pay_frequency)
    allowed_days = eligible_days(period_start, period_end, include_weekends)

    st.info(
        f"Current {pay_frequency.lower()} expense period: "
        f"**{period_start:%b %d, %Y} – {period_end:%b %d, %Y}** "
        f"({len(allowed_days)} eligible travel day(s))."
    )

    st.markdown("#### Per diem categories")
    st.session_state.per_diem_df = st.data_editor(
        st.session_state.per_diem_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Category": st.column_config.TextColumn("Category", required=True),
            "Rate": st.column_config.NumberColumn(
                "Rate ($)", min_value=0.0, step=0.25, format="$%.2f"
            ),
        },
        key="per_diem_editor",
    )

with st.container(border=True):
    st.subheader("2. Trips")
    st.caption(
        "Enter the full round-trip mileage yourself. Use the route/notes box for places visited or multi-stop notes."
    )

    if st.button("➕ Add trip", type="primary"):
        st.session_state.trips.append(new_trip())
        st.rerun()

    pd_map = per_diem_rate_map()
    pd_names = list(pd_map.keys()) or ["No per diem"]

    for idx, trip in enumerate(st.session_state.trips):
        with st.expander(
            f"{trip['name']} — {trip['round_trip_miles']:,.1f} round-trip miles",
            expanded=True,
        ):
            a, b, c = st.columns([2, 1, 1])

            with a:
                trip["name"] = st.text_input(
                    "Trip name",
                    value=trip["name"],
                    key=f"name_{trip['id']}",
                )
            with b:
                trip["times_pay_period"] = int(
                    st.number_input(
                        "Times this pay period",
                        min_value=0,
                        value=int(trip["times_pay_period"]),
                        step=1,
                        key=f"times_period_{trip['id']}",
                    )
                )
            with c:
                trip["times_per_week"] = float(
                    st.number_input(
                        "Times per week for projection",
                        min_value=0.0,
                        value=float(trip["times_per_week"]),
                        step=0.5,
                        key=f"times_week_{trip['id']}",
                    )
                )

            trip["route_notes"] = st.text_area(
                "Route / locations / notes",
                value=trip["route_notes"],
                placeholder="Example: Troy → Union Springs → Troy",
                key=f"route_notes_{trip['id']}",
                height=80,
            )

            d, e = st.columns(2)
            with d:
                trip["round_trip_miles"] = st.number_input(
                    "Full round-trip mileage",
                    min_value=0.0,
                    value=float(trip["round_trip_miles"]),
                    step=1.0,
                    key=f"miles_{trip['id']}",
                )
            with e:
                selected = trip["per_diem_category"]
                if selected not in pd_names:
                    selected = pd_names[0]
                trip["per_diem_category"] = st.selectbox(
                    "Per diem category",
                    pd_names,
                    index=pd_names.index(selected),
                    key=f"pd_{trip['id']}",
                )

            f, g = st.columns([1, 1])
            with f:
                if st.button(
                    "Duplicate trip",
                    key=f"dup_{trip['id']}",
                    use_container_width=True,
                ):
                    seed = deepcopy(trip)
                    seed.pop("id", None)
                    seed["name"] = f"{trip['name']} Copy"
                    st.session_state.trips.insert(idx + 1, new_trip(seed))
                    st.rerun()

            with g:
                if len(st.session_state.trips) > 1:
                    if st.button(
                        "🗑 Delete trip",
                        key=f"delete_{trip['id']}",
                        use_container_width=True,
                    ):
                        st.session_state.trips.pop(idx)
                        st.rerun()

            pd_rate = float(pd_map.get(trip["per_diem_category"], 0.0))
            total_miles = trip["round_trip_miles"] * trip["times_pay_period"]
            mileage_amt = total_miles * st.session_state.mileage_rate
            pd_amt = pd_rate * trip["times_pay_period"]

            st.markdown(
                f"**Pay-period miles:** {total_miles:,.1f}  \n"
                f"**Mileage reimbursement:** {money(mileage_amt)}  \n"
                f"**Per diem:** {money(pd_amt)}  \n"
                f"**Trip total:** {money(mileage_amt + pd_amt)}"
            )

pay_period_rows = build_pay_period_rows(st.session_state.mileage_rate)
weekly_rows = build_weekly_rows(st.session_state.mileage_rate)

pay_summary = summarize(
    pay_period_rows,
    "Total miles",
    "Mileage reimbursement",
    "Per diem",
    "Total",
)
weekly_summary = summarize(
    weekly_rows,
    "Weekly miles",
    "Mileage reimbursement",
    "Per diem",
    "Weekly total",
)
annual = annual_projection_from_weekly(st.session_state.mileage_rate)
future_rows = build_future_rate_projection(
    st.session_state.mileage_rate,
    annual_rate_increase,
    future_years,
)

with st.container(border=True):
    st.subheader("3. Expense check & projection")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Total miles — pay period", f"{pay_summary['miles']:,.1f}")
    r2.metric("Mileage reimbursement", money(pay_summary["mileage"]))
    r3.metric(
        "Per diem" + (" (taxable)" if taxable_per_diem else ""),
        money(pay_summary["per_diem"]),
    )
    r4.metric("Projected expense check", money(pay_summary["total"]))

    st.markdown("#### Weekly projection")
    w1, w2, w3, w4 = st.columns(4)
    w1.metric("Weekly miles", f"{weekly_summary['miles']:,.1f}")
    w2.metric("Weekly mileage reimbursement", money(weekly_summary["mileage"]))
    w3.metric("Weekly per diem", money(weekly_summary["per_diem"]))
    w4.metric("Weekly total", money(weekly_summary["total"]))

    st.markdown("#### Annual projection")
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Projected annual miles", f"{annual['annual_miles']:,.1f}")
    a2.metric("Annual mileage reimbursement", money(annual["annual_mileage"]))
    a3.metric(
        "Annual per diem" + (" (taxable)" if taxable_per_diem else ""),
        money(annual["annual_per_diem"]),
    )
    a4.metric("Projected annual expense reimbursements", money(annual["annual_total"]))

    with st.expander("Trip-by-trip pay-period breakdown"):
        st.dataframe(
            pd.DataFrame(pay_period_rows),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("#### Future mileage-rate scenario")
    st.caption(
        "Miles stay based on your weekly travel pattern while the user-entered reimbursement rate changes."
    )

    future_df = pd.DataFrame(future_rows)
    st.dataframe(
        future_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Mileage rate": st.column_config.NumberColumn(format="$%.3f"),
            "Weekly miles": st.column_config.NumberColumn(format="%.1f"),
            "Weekly mileage reimbursement": st.column_config.NumberColumn(format="$%.2f"),
            "Weekly per diem": st.column_config.NumberColumn(format="$%.2f"),
            "Weekly total": st.column_config.NumberColumn(format="$%.2f"),
            "Projected annual miles": st.column_config.NumberColumn(format="%.1f"),
            "Projected annual mileage reimbursement": st.column_config.NumberColumn(format="$%.2f"),
            "Projected annual per diem": st.column_config.NumberColumn(format="$%.2f"),
            "Projected annual total": st.column_config.NumberColumn(format="$%.2f"),
        },
    )

with st.container(border=True):
    st.subheader("4. Export")

    export_bytes = make_excel_export(
        pay_period_rows=pay_period_rows,
        weekly_rows=weekly_rows,
        future_rows=future_rows,
        pay_frequency=pay_frequency,
        period_start=period_start,
        period_end=period_end,
        include_weekends=include_weekends,
        taxable_per_diem=taxable_per_diem,
    )

    st.download_button(
        "⬇️ Download Excel report",
        data=export_bytes,
        file_name="travel_expense_projection.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
    )

st.caption(
    "Enter round-trip mileage manually. No map service or API key is required."
)
