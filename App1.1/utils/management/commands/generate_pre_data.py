import json


from django.core.management.base import BaseCommand
from django.conf import settings

from utils.models import City, State, Country


class Command(BaseCommand):
    help = """Generate Pre Data"""

    def add_location(self):

        with open('./static/location.json') as f:
            data = json.load(f)
        country, created = Country.objects.get_or_create(
            name="India",
            code="IN"
        )
        for state in data['state']:
            state_obj, created = State.objects.get_or_create(
                name=state['name'],
                code=state['code'],
                country=country
            )

            for city in state['city']:
                city_obj, created = City.objects.get_or_create(
                    name=city,
                    state=state_obj
                )

    def handle(self, *args, **kwargs):
        self.add_location()
