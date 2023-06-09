import datetime


def convert_period_to_set(time_start, time_end):
    time_set = set()
    while time_start <= time_end:
        time_set.add(time_start.replace(tzinfo=None))
        time_start += datetime.timedelta(minutes=15)
    return time_set


def calc_free_time_in_day(bookings, service_time, workdate_date, workday_time_start, workday_time_end):
    free_time = []
    busy_time = []
    for booking in bookings:
        booking_time_start = booking['date_time']
        booking_time_end = booking_time_start + datetime.timedelta(minutes=booking['service_time'])
        busy_time.append(convert_period_to_set(booking_time_start, booking_time_end))

    workday_time_start = datetime.datetime.combine(workdate_date, workday_time_start)
    workday_time_end = datetime.datetime.combine(workdate_date, workday_time_end)
    day_times = convert_period_to_set(workday_time_start, workday_time_end - datetime.timedelta(minutes=service_time))

    for time_start in day_times:
        possible_time = convert_period_to_set(time_start, time_start + datetime.timedelta(minutes=service_time))
        no_intersection = True
        for one_booking in busy_time:
            if len(possible_time.intersection(one_booking)) > 1:
                no_intersection = False
                break
        if no_intersection:
            free_time.append(time_start)
    return free_time
