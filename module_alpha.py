import datetime as dt
import pytz


def get_local_current_datetime():
    local_current_datetime_raw = dt.datetime.now()
    local_current_datetime = local_current_datetime_raw.strftime("%Y-%m-%d %H:%M:%S")
    return f"Your current local date & time: {local_current_datetime}"


def get_city_current_datetime(city_name, city_tz, selected_temp):
    city_tzinfo = pytz.timezone(city_tz)
    city_current_datetime_raw = dt.datetime.now(tz=city_tzinfo)
    city_current_datetime = city_current_datetime_raw.strftime("%Y-%m-%d %H:%M:%S")
    return f"The current local date & time in {city_name}: {city_current_datetime}"