# bookings/utils.py
from datetime import datetime, timedelta

def generate_time_slots(start_time, end_time):
    time_slots = []
    current_time = start_time
    while current_time < end_time:
        end_current_slot = current_time + timedelta(hours=1)
        time_slot = f"{current_time.strftime('%H:%M')}-{end_current_slot.strftime('%H:%M')}"
        time_slots.append(time_slot)
        current_time = end_current_slot
    return time_slots

def fetch_available_times(selected_date):
    weekday = selected_date.weekday()
    time_slots = []

    if weekday < 4:  # Monday to Thursday
        start_time = datetime.combine(selected_date, datetime.strptime("10:00", '%H:%M').time())
        end_time = datetime.combine(selected_date, datetime.strptime("22:00", '%H:%M').time())
        time_slots = generate_time_slots(start_time, end_time)
    elif weekday == 4:  # Friday
        start_time = datetime.combine(selected_date, datetime.strptime("15:00", '%H:%M').time())
        end_time = datetime.combine(selected_date + timedelta(days=1), datetime.strptime("01:00", '%H:%M').time())
        time_slots = generate_time_slots(start_time, end_time)
    elif weekday == 5:  # Saturday
        start_time = datetime.combine(selected_date, datetime.strptime("15:00", '%H:%M').time())
        end_time = datetime.combine(selected_date + timedelta(days=1), datetime.strptime("01:00", '%H:%M').time())
        time_slots = generate_time_slots(start_time, end_time)
    elif weekday == 6:  # Sunday
        # Closed on Sundays
        time_slots = []

    return time_slots
