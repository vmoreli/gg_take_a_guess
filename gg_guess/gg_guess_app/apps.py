from django.apps import AppConfig
import requests

COUNTRIES = []

class GgGuessAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gg_guess_app'

    def ready(self):
            global COUNTRIES
            url = "https://restcountries.com/v3.1/all"

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                for country in data:
                    country_info = {
                        'name': country.get('name', {}).get('common') if country.get('name') else None,
                        'hemisphere': 'Northern' if country.get('latlng') and len(country.get('latlng')) > 0 and country.get('latlng')[0] > 0 else 'Southern',
                        'continent': country.get('continents', [None])[0],
                        'language': list(country.get('languages', {}).values())[0] if country.get('languages') else None,
                        'currency': list(country.get('currencies', {}).keys())[0] if country.get('currencies') else None,
                        'area': country.get('area') if country.get('area') is not None else None,
                        'subregion': country.get('subregion') if country.get('subregion') is not None else None,
                        'capital': country.get('capital')[0] if country.get('capital') and len(country.get('capital')) > 0 else None
                    }
                    COUNTRIES.append(country_info)
                print("Fetched and stored country information.")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching country names: {e}")