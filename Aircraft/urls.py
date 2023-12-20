from django.urls import path

from .views import (
    # aircraft
    AircraftListCreateView,
    AircraftGetUpdateDelete,

    # Airport
    AirportListCreateView,
    AirportGetUpdateDel,

    # Flight
    FlightListCreateView,
    FlightGetUpdateDelete,
    SearchFlight,
    Flight_Report,
)

urlpatterns = [
    # Aircraft
    path('Aircraft_create_list/',AircraftListCreateView.as_view()),
    path('Aircraft_get_update_delete/<int:pk>',AircraftGetUpdateDelete.as_view()),

    # Airport
    path('Airport_create_list/',AirportListCreateView.as_view()),
    path('Airport_get_update_del/<int:pk>/',AirportGetUpdateDel.as_view()),
    
    # Flight
    path('Flight_create_list/',FlightListCreateView.as_view()),
    path('Flight_get_update_del/<int:pk>',FlightGetUpdateDelete.as_view()),
    path("search_flight/",SearchFlight.as_view()),
    path("Flight_report/",Flight_Report.as_view()),
]
