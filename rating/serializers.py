from rest_framework import serializers
import requests
from rest_framework.exceptions import NotFound

from rating.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'model', 'make', 'avg_rating']

    def validate(self, attrs):
        model = attrs['model']
        make = attrs['make']
        if self.is_duplicate(make, model):
            raise serializers.ValidationError({'message': 'Duplicate entry.'}, code=400)

        if self.car_is_fake(model, make):
            raise NotFound({'message': 'Car doesn\'t exists.'})

        return attrs

    def car_is_fake(self, tested_model, tested_make):
        response = requests.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{tested_make}?format=json')
        if response.status_code == 200:
            return self.is_model_in_results(tested_model, response)
        else:
            return True

    @staticmethod
    def is_duplicate(make, model):
        return Car.objects.filter(model__iexact=model, make__iexact=make)

    @staticmethod
    def is_model_in_results(tested_model, response):
        results = response.json()['Results']

        return not list(filter(lambda car: car['Model_Name'].lower() == tested_model.lower(), results))


class RateSerializer(serializers.ModelSerializer):
    rate = serializers.IntegerField()

    class Meta:
        model = Car
        fields = ['id', 'rate']

    def update(self, instance, validated_data):
        instance.rating_sum += validated_data['rate']
        instance.rating_count += 1

        return super().update(instance, validated_data)

    def validate(self, attrs):
        if attrs['rate'] < 1 or attrs['rate'] > 5:
            raise serializers.ValidationError('Rate should be between 1-5.', code=400)

        return attrs


class PopularCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'rating_count']
