from django.shortcuts import render
from django.views.generic import View
import urllib.request
import json

class HomeView(View):       
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            city = self.request.user.city
            try:
                source = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=25cbc478902e4cec447fa217ca54132d').read()
            except:
                city = 'London'
                source = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=25cbc478902e4cec447fa217ca54132d').read()
            list_of_data = json.loads(source)
           
            data = {
                'country_code' : str(list_of_data['sys']['country']),
                'coordinate' : str(list_of_data['coord']['lon']) +','+
                                str(list_of_data['coord']['lat']) ,                           
                'temp' : str(list_of_data['main']['temp']),
                'humidity': str(list_of_data['main']['humidity']),
                'wind' : str(list_of_data['wind']['speed']),
                'main' : str(list_of_data['weather'][0]['main']),
                'description' : str(list_of_data['weather'][0]['description']),
                'icon' : list_of_data['weather'][0]['icon'],
                'city':city
            }
        else : 
            city = 'London'
            source = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q=London&units=metric&appid=25cbc478902e4cec447fa217ca54132d').read()
            list_of_data = json.loads(source)

            data = {
                'country_code' : str(list_of_data['sys']['country']),
                'coordinate' : str(list_of_data['coord']['lon']) +','+
                                str(list_of_data['coord']['lat']) ,                           
                'temp' : str(list_of_data['main']['temp']),
                'humidity': str(list_of_data['main']['humidity']),
                'wind' : str(list_of_data['wind']['speed']),
                'main' : str(list_of_data['weather'][0]['main']),
                'description' : str(list_of_data['weather'][0]['description']),
                'icon' : list_of_data['weather'][0]['icon'],
                 'city':city
            }
        return render(self.request, 'base/home.html', data )










    






