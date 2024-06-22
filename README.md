This is the first python project in BIU DS17

0. General:
   - The app is designed in such a way that the user can change the settings between searches with no need to refresh the page.
   - Reset favorites button is added for convenience with checking the app. 
   - Refresh button is there to smooth the user interaction in case he saves settings or set them as default.
     In these cases, without a refresh button, the updated list in the selection box will not be displayed until the user clicks another button.
     
1. The user can select a city from a list
   - Search input is not case sensitive
   - Input can be a city name or alternative name (example: 'ir david' will find 'Jerusalem')
   - If there are 2 or more cities with the same name, the user can select which one he was referring to.
     
2. The user can fetch weather data for his selection / typed input. The app will print a df with the relevant data

3. The user can save the current settings
   - Save settings button will show up only if there are new settings to save.

4. The user can set the current settings as default
   - Set as default button will only show up in the relevant situation
