from django.core.management.base import BaseCommand
from pvta_data.models import Departure, Route, Stop

import datetime
import json
import pdb
import re
import urllib.request

class Command(BaseCommand):
    def parse_json_unix_timestamp(self, timestamp):
        matches = re.match('\/Date\((\d{13})-0\d00\)\/', timestamp)
        epoch_milliseconds = int(matches.group(1))
        epoch_seconds = epoch_milliseconds / 1000
        return datetime.datetime.fromtimestamp(epoch_seconds)
    
    def handle(self, **options):
        Route.objects.all().delete()
        routes_json = urllib.request.urlopen("http://bustracker.pvta.com/InfoPoint/rest/Routes/GetVisibleRoutes").read()
        routes_data = json.loads(routes_json)
        for route_data in routes_data:
            route = Route(id=route_data['RouteId'],
                          short_name=route_data['ShortName'],
                          long_name=route_data['LongName'],
                          route_abbreviation=route_data['RouteAbbreviation'],
                          color=route_data['Color'])
            route.save()
        
        Stop.objects.all().delete()
        stops_json = urllib.request.urlopen("http://bustracker.pvta.com/InfoPoint/rest/Stops/GetAllStops").read()
        stops_data = json.loads(stops_json)
        for stop_data in stops_data:
            stop = Stop(id=stop_data['StopId'],
                        name=stop_data['Name'],
                        latitude=stop_data['Latitude'],
                        longitude=stop_data['Longitude'],
                        is_time_point=stop_data['IsTimePoint'])
            stop.save()
        
        Departure.objects.all().delete()
        stop_departures_json = urllib.request.urlopen("http://bustracker.pvta.com/InfoPoint/rest/StopDepartures/GetAllStopDepartures").read()
        stop_departures_data = json.loads(stop_departures_json)
        for stop_departure_data in stop_departures_data:
            stop = Stop.objects.get(id=stop_departure_data['StopId'])
            for route_direction_data in stop_departure_data['RouteDirections']:
                route = Route.objects.get(id=route_direction_data['RouteId'])
                direction = route_direction_data['Direction']
                is_done = route_direction_data['IsDone']
                for departure_data in route_direction_data['Departures']:
                    trip_data = departure_data['Trip']
                    headsign = trip_data['InternetServiceDesc']
                    sdt = self.parse_json_unix_timestamp(departure_data['SDT'])
                    edt = self.parse_json_unix_timestamp(departure_data['EDT'])
                    departure = Departure(stop=stop,
                                          route=route,
                                          direction=direction,
                                          is_done=is_done,
                                          sdt=sdt,
                                          edt=edt,
                                          headsign=headsign)
                    departure.save()