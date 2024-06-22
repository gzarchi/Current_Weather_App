import geonamescache as gc
import requests
import pandas as pd
import streamlit as st
import datetime as dt
import pytz
import json
import os
from main import get_typed_selection_cities, get_typed_selection_settings, fetch_data
from module_alpha import get_local_current_datetime, get_city_current_datetime
from module_a import save_settings, load_favorites, set_settings_as_default, reset_favorites


# Display Title
st.markdown('# Current Weather App')
st.markdown('#### By Gal Zarchi // BIU DS17')

# Set initial settings
initial_settings = [['Jerusalem', 'Asia/Jerusalem', '\U0001F64A Celsius'],
                    ['New York City', 'America/New_York', '\U0001F649 Fahrenheit']]
if load_favorites() is not None:
    initial_settings = load_favorites()

# Set temperature list
temp_list = ['\U0001F64A Celsius', '\U0001F649 Fahrenheit', '\U0001F648 Kelvin']

# Set cities list
cities_list = [item[0] for item in initial_settings]
cities_list.append('Other')

# Initialize session state
if 'selection' not in st.session_state:
    st.session_state['selection'] = None

if 'typed_selection' not in st.session_state:
    st.session_state['typed_selection'] = None

if 'selection_settings' not in st.session_state:
    st.session_state['selection_settings'] = None

if 'save_settings clicked' not in st.session_state:
    st.session_state['save_settings clicked'] = False

if 'last_selected_temp' not in st.session_state:
    st.session_state['last_selected_temp'] = None

if 'changed_selected_temp' not in st.session_state:
    st.session_state['changed_selected_temp'] = False

if 'selected_city' not in st.session_state:
    st.session_state['selected_city'] = None

# Display current local datetime
st.write(get_local_current_datetime())

# Display selection box for cities list
selection = st.selectbox('Select a City: ', cities_list)

# check if user selected already
if selection != st.session_state['selection']:
    st.session_state['selection'] = selection  # save value in st.session_state

# Extract selection settings
selection_settings = None if selection != 'Other' else st.session_state['selection_settings']
for settings in initial_settings:
    if settings[0] == selection:
        selection_settings = settings
        break

# Check if selection_settings has changed and update session_state
if selection_settings != st.session_state['selection_settings']:
    st.session_state['selection_settings'] = selection_settings

# Set typed input
typed_selection = st.text_input('City:') if selection == 'Other' else None

if typed_selection != st.session_state['typed_selection']:
    st.session_state['typed_selection'] = typed_selection  # save value in st.session_state
    st.session_state['selection_settings'] = None

# Determine default temperature
default_temp_index = temp_list.index(selection_settings[2]) if st.session_state['selection_settings'] is not None else 0

# Display temperature buttons
selected_temp = st.radio('Temperature Units: ', temp_list, index=default_temp_index)

# Control for change in selected_temp
if selected_temp != st.session_state['last_selected_temp']:
    st.session_state['last_selected_temp'] = selected_temp
    st.session_state['changed_selected_temp'] = True
else:
    st.session_state['changed_selected_temp'] = False


# End of user initial input
# ----------------------------------------------------------------------------------------------------

# Display fetch button
fetch_button = st.button('Fetch Data')
if fetch_button or st.session_state['selected_city'] is not None:

    # Process fetch_data() for an existing settings
    if selection != 'Other':
        df = fetch_data(selection_settings[0], selection_settings[1], selected_temp)

        # Display selected city local datetime
        st.write(get_city_current_datetime(selection_settings[0], selection_settings[1], selected_temp))

        st.table(df)

    # Ask for user typed input
    elif typed_selection == '':
        st.markdown(f'Enter ` City `')

    # Process get_typed_selection_settings() for a new typed_input
    else:
        typed_selection_settings = get_typed_selection_settings(typed_selection)

        if typed_selection_settings is not None:
            typed_selection_settings.append(selected_temp)

            # Set selection_settings as typed_selection_settings
            selection_settings = typed_selection_settings

            df = fetch_data(selection_settings[0], selection_settings[1], selected_temp)

            # Display selected city local datetime
            st.write(get_city_current_datetime(selection_settings[0], selection_settings[1], selected_temp))

            st.table(df)
        else:
            st.write(f'Sorry, we have no data for `{typed_selection}`...')

        # Save value in st.session_state
        if selection_settings != st.session_state['selection_settings']:
            st.session_state['selection_settings'] = typed_selection_settings

# Define terms to display buttons
selected = selection != 'Other'
empty_typed_selection = typed_selection == ''
found_typed_selection_settings = not selected and not empty_typed_selection and st.session_state['selection_settings'] is not None
changed_default_temp = selected and selected_temp != temp_list[default_temp_index]
selected_default = selection == cities_list[0]
changed_selected_temp = st.session_state['changed_selected_temp'] is True

# Display 'Set as Default' button
if selected and not selected_default and not changed_default_temp:
    set_as_default_button = st.button('Set as Default')

    # Process set_as_default_button
    if set_as_default_button:
        set_settings_as_default(selection_settings[0], selection_settings[1], selected_temp)

# Display 'Set as Default' button
if not selected_default and st.session_state['save_settings clicked'] is True:
    set_as_default_button = st.button('Set as Default')

    # Process set_as_default_button
    if set_as_default_button:
        set_settings_as_default(selection_settings[0], selection_settings[1], selected_temp)
        st.session_state['save_settings clicked'] = False

# Display 'Save to Favorites' button
if changed_default_temp or found_typed_selection_settings:
    save_settings_button = st.button('Save Settings')

    # reset to pre save settings stage
    if changed_selected_temp:
        st.session_state['save_settings clicked'] = False

    # Process save_to_favorites_button
    elif save_settings_button or st.session_state['save_settings clicked']:
        st.session_state['save_settings clicked'] = True
        save_settings(selection_settings[0], selection_settings[1], selected_temp, initial_settings)


if initial_settings != [['Jerusalem', 'Asia/Jerusalem', '\U0001F64A Celsius'], ['New York City', 'America/New_York', '\U0001F649 Fahrenheit']]:
    reset_favorites_button = st.button('Reset Favorites')
    if reset_favorites_button:
        reset_favorites([['Jerusalem', 'Asia/Jerusalem', '\U0001F64A Celsius'], ['New York City', 'America/New_York', '\U0001F649 Fahrenheit']])


st.link_button('New Search', 'https://currentweatherapp.streamlit.app')




