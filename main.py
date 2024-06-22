import geonamescache as gc
import requests
import pandas as pd
import streamlit as st


def get_typed_selection_cities(typed_selection):
    all_cities_cache = gc.GeonamesCache().get_cities()
    typed_selection_cities = [value for key, value in all_cities_cache.items() if (typed_selection.lower().title() == value['name'] or typed_selection in value['alternatenames'] or typed_selection.lower().title() in value['alternatenames'])]
    return typed_selection_cities


def get_typed_selection_settings(typed_selection):
    typed_selection_cities = get_typed_selection_cities(typed_selection)

    if len(typed_selection_cities) == 0:
        return None

    elif len(typed_selection_cities) == 1:
        typed_selection_city = typed_selection_cities[0]

    else:
        typed_selection_options = [f"{city['timezone']}/{city['name']}" for city in typed_selection_cities]
        selected_city = st.radio(f'Select which `{typed_selection}` you are referring to:', typed_selection_options)

        if selected_city != st.session_state['selected_city']:
            st.session_state['selected_city'] = selected_city

        for city in typed_selection_cities:
            if (city['timezone'] + '/' + city['name']) == selected_city:
                typed_selection_city = city
                break

    typed_selection_settings = [typed_selection_city['name'], typed_selection_city['timezone']]
    return typed_selection_settings


def fetch_data(name, tz, selected_temp):
    ow_api_key = '0f4470337016fe83612563095537bf7a'
    temp_units = 'standard' if (selected_temp == 'Kelvin') else (
        'metric' if (selected_temp == 'Celsius') else 'imperial')
    url_call = f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={ow_api_key}&units={temp_units}"
    city_owdata = requests.get(url_call)
    city_owdata = city_owdata.json()

    temp_unit = "C°" if temp_units == 'metric' else ("F°" if temp_units == 'imperial' else "K°")
    relevant_data = {
        'Weather Conditions': [f"{city_owdata['weather'][0]['main']}"],
        'Temperature': [f"{city_owdata['main']['temp']}{temp_unit}"],
        'Humidity Level': [f"{city_owdata['main']['humidity']}%"],
        'feels like': [f"{city_owdata['main']['feels_like']}{temp_unit}"]
        }

    df = pd.DataFrame(relevant_data, index=None)
    return df


