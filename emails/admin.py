import json
import requests
from collections import defaultdict
from django.contrib import admin
from django.core.mail import send_mail

from .models import City, Subscriber

admin.site.register(City)


class SubscriberAdmin(admin.ModelAdmin):
    actions = ['email_subscribers']

    def get_weather(self, city):
        city_name = city.name
        state = city.state

        url = "http://api.wunderground.com/api/14947de5db2ee190/{type}/q/{state}/{city}.json"
        conditions_url = url.format(type='conditions', state=state, city=city_name)
        almanac_url = url.format(type='almanac', state=state, city=city_name)

        conditions = json.loads(requests.get(conditions_url, timeout=5).content)['current_observation']
        almanac = json.loads(requests.get(almanac_url, timeout=5).content)['almanac']

        return {'conditions': conditions, 'almanac': almanac}

    def record_weather(self, city):
        weather = self.get_weather(city)
        conditions = weather['conditions']

        current_temp = int(conditions['temp_f'])
        average_temp = int(weather['almanac']['temp_high']['normal']['F'])
        temp_difference = average_temp - current_temp

        warm = (temp_difference >= 5)
        cold = (temp_difference <= -5)

        general_weather = conditions['weather']

        sunny = (general_weather == 'Sunny')
        rainy = bool(conditions['precip_today_in'])

        if warm or sunny:
            niceness = 'nice'
        elif rainy or cold:
            niceness = 'cold'
        else:
            niceness = 'neutral'

        return {'niceness': niceness,
                'temp': conditions['temperature_string'],
                'general_weather': general_weather}

    def generate_email(self, weather_data, city_display):
        subject_converter = {'nice': "It's nice out! Enjoy a discount on us.",
                             'cold': "Not so nice out? That's okay, enjoy a discount on us.",
                             'neutral': "Enjoy a discount on us."}

        message = "Weather for today in {city}:\n{weather} and {temp}".format(
            city=city_display,
            weather=weather_data['general_weather'],
            temp=weather_data['temp'])

        return {'subject': subject_converter[weather_data['niceness']],
                'message': message}

    def email_subscribers(self, request, subscribers):
        email_content_by_city = defaultdict(dict)

        for subscriber in subscribers:
            city = subscriber.city
            city_display = city.display_name

            if city_display not in email_content_by_city:
                email_content_by_city[city_display] = self.record_weather(city)

            email = self.generate_email(email_content_by_city[city_display], city_display)

            send_mail(email['subject'], email['message'], "mjswartz.develop@gmail.com", [subscriber.email])

admin.site.register(Subscriber, SubscriberAdmin)
