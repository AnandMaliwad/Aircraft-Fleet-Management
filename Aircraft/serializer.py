# rest framework
from rest_framework import serializers

# Regular Expression
import re

# django
from django.db.models import Q, Max

# date time
from datetime import datetime

from django.utils import timezone

# models
from .models import (
    Aircraft,
    Airport,
    Flight,
) 

"""
***********************************************************
                        Aircraft
***********************************************************
"""

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ["id","model_name","serial_number","manufacturer",
                  "manufactured_date","engine_type","total_seats"]
        read_only_fields = ['id',]

    def validate(self,validated_data):
        manufacturer_1 = validated_data.get("manufacturer")
        serial_number = validated_data.get("serial_number")
        total_seats = validated_data.get("total_seats")

        # exists
        if Aircraft.objects.filter(Q(manufacturer=manufacturer_1) & Q(serial_number=serial_number)):
            raise serializers.ValidationError({
                "data_exist": "The data is already exist."
            })
        elif len(serial_number) < 2 or len(serial_number) > 8:
            raise serializers.ValidationError("Length of serial number must be in the range of 2 to 8.")
        elif not serial_number.isalnum():
            raise serializers.ValidationError(
                "serial Number : It must contain alphanumeric characters."
            )
        elif total_seats < 0:
            raise serializers.ValidationError("Total seat cannot be Zero.")
    
        return validated_data
    


"""
***********************************************************
                        Airport
***********************************************************
"""

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["id","name","ICAO_code","city","country"]
        read_only_fields = ['id',]


"""
***********************************************************
                        Flight
***********************************************************
"""

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["id","Airline","flight_code","aircraft","departure_airport",
                  "arrival_airport","departure_time","arrival_time"]
        read_only_fields = ['id',]
    
    def validate(self,validated_data):
        aircraft = validated_data.get("aircraft")
        flight_code = validated_data.get("flight_code")
        departure_airport = validated_data.get("departure_airport")
        arrival_airport = validated_data.get("arrival_airport")
        departure_time = validated_data.get("departure_time")
        arrival_time = validated_data.get("arrival_time")
        
        # exists data
        flight_code_exists = Flight.objects.filter(flight_code=flight_code)

        current_time = timezone.now() 
        existing_Flight = Flight.objects.filter(
            aircraft=aircraft,
            departure_time__lte=arrival_time,
            arrival_time__gte=departure_time
        ).exclude(id=validated_data.get('id'))
        # print(f"\n\n\n data = {existing_Flight}\n\n\n")

        if Flight.objects.filter(aircraft=aircraft):
            if not departure_time and not arrival_time:
                pass
            else:
                arr_time = Flight.objects.filter(
                Q(aircraft=aircraft) & 
                Q(is_active=True)).aggregate(max_arr_time = Max("arrival_time"))
                arr_time_1 = arr_time["max_arr_time"]
                flight_interval_time = arr_time["max_arr_time"] + timezone.timedelta(minutes=30)

                if departure_time < flight_interval_time:
                    raise serializers.ValidationError({
                    "Departure time" : "Departure time must be after 30 minutes of last Arrival time."
                 })
                
                dep_center = Flight.objects.filter(
                    Q(aircraft=aircraft) &
                    Q(arrival_time=arr_time_1)
                ).values("arrival_airport")

                if departure_airport.id != dep_center[0]["arrival_airport"]:
                    raise serializers.ValidationError({
                        "Departure Airport" : "Departure airport should not be different from last arrival airport."
                    })
                
        elif flight_code_exists:
            raise serializers.ValidationError("This Flight already Exists.")
        elif departure_airport == arrival_airport:
            raise serializers.ValidationError(
                "Departure airport and Destination can not be same at same time."
            )
        elif departure_time <= current_time:
            raise serializers.ValidationError(
                {"Departure time :" : "It must be schedule in Future"}
            )
        elif arrival_time <= departure_time:
            raise serializers.ValidationError({
                "Arrival time" : "It must be not less than Departure time."
            })
        elif existing_Flight.exists():
            raise serializers.ValidationError(
                "Aircraft is already booked for this specified time period."
            )

        return validated_data