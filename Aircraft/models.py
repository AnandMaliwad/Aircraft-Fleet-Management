from django.db import models

# Create your models here.


class Aircraft(models.Model):
    model_name = models.CharField(max_length=25)
    serial_number = models.CharField(max_length=8)
    manufacturer = models.CharField(max_length=50)
    manufactured_date = models.DateField()
    engine_type = models.CharField(max_length=50)
    total_seats = models.IntegerField()

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} - {self.serial_number}"


class Airport(models.Model):
    name = models.CharField(max_length=50)
    ICAO_code = models.CharField(max_length=4,unique=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ICAO_code} - {self.city} - {self.name}"


class Flight(models.Model):
    Airline = models.CharField(max_length=50)
    flight_code = models.CharField(max_length=50)
    aircraft = models.ForeignKey(Aircraft, null=True, blank=True, on_delete=models.SET_NULL)

    departure_airport = models.ForeignKey(Airport,
                                          related_name="departure",
                                          limit_choices_to={'is_active': True},
                                          null=True, blank=True,
                                          on_delete=models.SET_NULL)
    arrival_airport = models.ForeignKey(Airport,
                                        related_name="arrival",
                                        limit_choices_to={'is_active': True},
                                        null=True, blank=True,
                                        on_delete=models.SET_NULL)

    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    is_arrived = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flight_code}-{self.departure_airport}-{self.arrival_airport}"