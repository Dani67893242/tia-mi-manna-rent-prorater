import streamlit as st
import calendar
from dataclasses import dataclass

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

@dataclass
class ProratedRentResult:
    month: str
    year: int
    monthly_rent: float
    move_in_day: int
    days_in_month: int
    days_occupied: int
    daily_rate: float
    prorated_rent: float


def calculate_prorated_rent(monthly_rent: float, year: int, month_index: int, move_in_day: int) -> ProratedRentResult:
    """
    month_index: 1-12
    move_in_day: 1 - days_in_month
    """
    days_in_month = calendar.monthrange(year, month_index)[1]

    if not (1 <= move_in_day <= days_in_month):
        raise ValueError(f"Move-in day must be between 1 and {days_in_month} for that month.")

    days_occupied = days_in_month - move_in_day + 1
    daily_rate = monthly_rent / days_in_month
    prorated_rent = daily_rate * days_occupied

    return ProratedRentResult(
        month=MONTHS[month_index - 1],
        year=year,
        monthly_rent=monthly_rent,
        move_in_day=move_in_day,
        days_in_month=days_in_month,
        days_occupied=days_occupied,
        daily_rate=daily_rate,
        prorated_rent=prorated_rent
    )


# ------------------- Streamlit App -------------------
st.title("Tia Mi Manna's Prorator")

monthly_rent = st.number_input("Monthly Rent ($)", min_value=0.0, value=1750.0, step=50.0)

year = st.number_input("Year", min_value=1900, max_value=2100, value=2026, step=1)

month_name = st.selectbox("Month", MONTHS)
month_index = MONTHS.index(month_name) + 1

days_in_month = calendar.monthrange(int(year), month_index)[1]
move_in_day = st.number_input(
    f"Move-in Day (1–{days_in_month})",
    min_value=1,
    max_value=days_in_month,
    value=min(18, days_in_month),
    step=1
)

if st.button("Calculate"):
    result = calculate_prorated_rent(float(monthly_rent), int(year), month_index, int(move_in_day))

    st.subheader("Results")
    st.write(f"**Month:** {result.month} {result.year}")
    st.write(f"**Days in month:** {result.days_in_month}")
    st.write(f"**Days occupied:** {result.days_occupied}")
    st.write(f"**Daily rate:** ${result.daily_rate:.2f}")
    st.write(f"✅ **Prorated rent owed:** ${result.prorated_rent:.2f}")

    # Optional: show the exact fraction form (nice for explaining to clients)
    st.caption(f"Calculation: ${result.monthly_rent:.2f} × ({result.days_occupied}/{result.days_in_month})")