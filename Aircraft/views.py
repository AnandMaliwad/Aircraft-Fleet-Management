from rest_framework import serializers
from django.shortcuts import render
from django.db.models import Q
from datetime import timedelta
# swagger
from drf_yasg.utils import swagger_auto_schema


# rest framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,DestroyModelMixin
)
from rest_framework.filters import SearchFilter

# models
from .models import (
    Aircraft,
    Airport,
    Flight,
)

# serializer
from .serializer import (
    AircraftSerializer,
    AirportSerializer,
    FlightSerializer,
)


# Create your views here.

"""
*************************************************************************
                            Aircraft
*************************************************************************
"""
class AircraftListCreateView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = AircraftSerializer

    @ swagger_auto_schema(tags=["Aircraft Details"],operation_description="",)
    def post(self,request,*args,**kwargs):
        try:
            serializer = self.serializer_class(
                data = request.data,context={"request":request}
            )
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response({
                    "response_code":201,
                    "response_message" : "Aircraft Created",
                    "response_data" : serializer.data
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "response_code":400,
                    "response_message" : serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "response_code":400,
                "response_message" : str(e),
            },status=status.HTTP_400_BAD_REQUEST)
    
    @ swagger_auto_schema(tags=["Aircraft Details"],operation_description="",)
    def get(self,request,format=None):
        details = Aircraft.objects.filter(is_active=True)
        serializer = self.serializer_class(
            details,
            many=True,
            context = {"request":request}
        )
        return Response({
            "response_code" : 200,
            "response_data" : serializer.data
        },status=status.HTTP_200_OK)

class AircraftGetUpdateDelete(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = AircraftSerializer

    @ swagger_auto_schema(tags=["Aircraft Details"],operation_description="",)
    def get_object(self,pk):    
        try:
            return Aircraft.objects.get(id=pk)
        except Aircraft.DoesNotExist:
            raise serializers.ValidationError("Data Not Found")
    
     
    @ swagger_auto_schema(tags=["Aircraft Details"],operation_description="",)
    def patch(self,request,pk,format=None):
        try:
            Details = self.get_object(pk)
            serializer = self.serializer_class(Details,data=request.data,partial=True,
                                               context={"request":request})
            if serializer.is_valid(raise_exception=False):
                serializer.save()

                return Response({
                    "response_code" : 200,
                    "response_data" : serializer.data},
                    status = status.HTTP_200_OK
                )
            else :
                return Response({"response_code":400,
                                 "responsive_message": serializer.errors},
                                 status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"code":400,"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    @ swagger_auto_schema(tags=["Aircraft Details"],operation_description="",)
    def delete(self,request,pk,format=None):            # its for soft delete......
        detail_del = self.get_object(pk)
        if detail_del.is_active == True:
            detail_del.is_active = False
            detail_del.save()
            return Response({
                "response_code":200,
                "response_Message" : "Successfully Deleted."
            },status=status.HTTP_200_OK)
        else :
            return Response({
                "response_code":400,
                "response_message" : "Already Deleted."
            },status=status.HTTP_400_BAD_REQUEST)
    
    @ swagger_auto_schema(tags=["Aircraft Details"],operation_description="",)
    def get(self,request,pk,format=None):
        detail = self.get_object(pk)
        if detail.is_active == True:
            serializer = self.serializer_class(detail,context={"request":request})
            return Response({
                "response_code" : 200,
                "response_data" : serializer.data 
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "response_coe":400,
                "response_message" : "No data found",
            },status=status.HTTP_404_NOT_FOUND)
        


"""
*************************************************************************
                            Airport
*************************************************************************
"""

class AirportListCreateView(GenericAPIView,ListModelMixin,CreateModelMixin):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = Airport.objects.filter(is_active=True)
    serializer_class = AirportSerializer

    @swagger_auto_schema(tags=["Airport"],operation_description=("Payload:",'..'),)
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    @swagger_auto_schema(tags=["Airport"],operation_description=("Payload:",'..'),)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    

class AirportGetUpdateDel(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = Airport.objects.filter(is_active=True)
    serializer_class = AirportSerializer

       
    @swagger_auto_schema(tags=["Airport"],operation_description=("Payload:", '..'),)
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    @swagger_auto_schema(tags=["Airport"],operation_description=("Payload:", '..'),)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    @swagger_auto_schema(tags=["Airport"],operation_description=("Payload:", '..'),)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


"""
*************************************************************************
                            Flights
*************************************************************************
"""

class FlightListCreateView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = FlightSerializer
    # filter_backends = [SearchFilter]
    # search_fields = ['departure_airport__name','arrival_airport__name']

    @ swagger_auto_schema(tags=["Flight Details"],operation_description="",)
    def post(self,request,*args,**kwargs):
        try:
            serializer = self.serializer_class(
                data = request.data,context={"request":request}
            )
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response({
                    "response_code":201,
                    "response_message" : "Flight Created",
                    "response_data" : serializer.data
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "response_code":400,
                    "response_message" : serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "response_code":400,
                "response_message" : str(e),
            },status=status.HTTP_400_BAD_REQUEST)
    
    @ swagger_auto_schema(tags=["Flight Details"],operation_description="",)
    def get(self,request,format=None):
        details = Flight.objects.filter(is_active=True)
        serializer = self.serializer_class(
            details,
            many=True,
            context = {"request":request}
        )
        return Response({
            "response_code" : 200,
            "response_data" : serializer.data
        },status=status.HTTP_200_OK)

class FlightGetUpdateDelete(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = FlightSerializer
    # filter_backends = [SearchFilter]
    # search_fields = ['departure_airport','arrival_airport']

    @ swagger_auto_schema(tags=["Flight Details"],operation_description="",)
    def get_object(self,pk):    
        try:
            return Flight.objects.get(id=pk)
        except Flight.DoesNotExist:
            raise serializers.ValidationError("Data Not Found")
    
     
    @ swagger_auto_schema(tags=["Flight Details"],operation_description="",)
    def patch(self,request,pk,format=None):
        try:
            Details = self.get_object(pk)
            serializer = self.serializer_class(Details,data=request.data,partial=True,
                                               context={"request":request})
            if serializer.is_valid(raise_exception=False):
                serializer.save()

                return Response({
                    "response_code" : 200,
                    "response_data" : serializer.data},
                    status = status.HTTP_200_OK
                )
            else :
                return Response({"response_code":400,
                                 "responsive_message": serializer.errors},
                                 status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"code":400,"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    @ swagger_auto_schema(tags=["Flight Details"],operation_description="",)
    def delete(self,request,pk,format=None):            # its for soft delete......
        detail_del = self.get_object(pk)
        if detail_del.is_active == True:
            detail_del.is_active = False
            detail_del.save()
            return Response({
                "response_code":200,
                "response_Message" : "Successfully Deleted."
            },status=status.HTTP_200_OK)
        else :
            return Response({
                "response_code":400,
                "response_message" : "Already Deleted."
            },status=status.HTTP_400_BAD_REQUEST)
    
    @ swagger_auto_schema(tags=["Flight Details"],operation_description="",)
    def get(self,request,pk,format=None):
        detail = self.get_object(pk)
        if detail.is_active == True:
            serializer = self.serializer_class(detail,context={"request":request})
            return Response({
                "response_code" : 200,
                "response_data" : serializer.data 
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "response_coe":400,
                "response_message" : "No data found",
            },status=status.HTTP_404_NOT_FOUND)


class SearchFlight(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    queryset = Flight.objects.filter(is_active=True)
    serializer_class = FlightSerializer
    filter_backends = [SearchFilter]
    search_fields = ['departure_airport__city','arrival_airport__city']




class Flight_Report(APIView):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['departure_time','arrival_time']

    def get(self, request, format=None):
        departure_time = request.query_params.get("departure_time", None)
        arrival_time = request.query_params.get("arrival_time", None)

        try:
            queryset = Flight.objects.select_related("aircraft", "departure_airport").filter(
                Q(departure_time__gte=departure_time) & Q(arrival_time__lte=arrival_time)
            ).order_by("departure_airport")
        except ValueError:
            return Response("Invalid query parameters", status=status.HTTP_400_BAD_REQUEST)

        flights = Flight.objects.filter(is_active=True)
        data = {}
        for flight in flights:
            airport_icao = flight.departure_airport.ICAO_code
            if airport_icao not in data:
                data[airport_icao] = {
                    "airport_name": flight.departure_airport.name,
                    "flights_count": 0,
                    "flight_time_for_each_aircraft": [],
                }

            data[airport_icao]["flights_count"] += 1
            flight_time = (flight.arrival_time - flight.departure_time).total_seconds() / 60
            data[airport_icao]["flight_time_for_each_aircraft"].append({
                "aircraft": AircraftSerializer(flight.aircraft).data,
                "flight_time": f"{flight_time} minutes",
            })

        response = {
            "status": 1,
            "message": "Successfully retrieved flights",
            "data": data,
        }

        return Response(response)
