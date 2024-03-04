from rest_framework import serializers
from tickets.models import Guest,  Moive, Reservation



class MovieSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Moive
        fields = '__all__'




class ReservationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Reservation
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Guest
        fields = ['pk' , "name","mobile","reservation"]
        # uuid slug -> prefered in real life projects over pk
