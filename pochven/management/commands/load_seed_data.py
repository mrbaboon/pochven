from django.core.management import BaseCommand

from pochven.models import Constellation, SolarSystem
from pochven.systems import SYSTEMS


class Command(BaseCommand):
    def handle(self, *args, **options):

        for constellation_name in SYSTEMS.keys():
            constellation, _ = Constellation.objects.get_or_create(
                name=constellation_name
            )

            systems = SYSTEMS[constellation_name]

            for idx, record in enumerate(systems):
                system_name, is_home = record
                system, _ = SolarSystem.objects.get_or_create(
                    constellation=constellation,
                    name=system_name,
                    defaults=dict(
                        order=idx,
                        home=is_home,
                    ),
                )

                if system.order != idx:
                    system.order = idx

                if system.home != is_home:
                    system.home = is_home

                system.save()
