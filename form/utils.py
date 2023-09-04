# utils.py or helpers.py

from datetime import datetime, timedelta

def generate_time_slots(start_time, end_time):
    time_slots = []
    current_time = start_time

    while current_time <= end_time:
        time_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=10)

    return time_slots
