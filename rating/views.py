from rest_framework import viewsets, status
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response

from rating.models import Car
from rating.serializers import CarSerializer, RateSerializer, PopularCarsSerializer


class CarViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class RateView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = RateSerializer

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PopularView(ListAPIView):
    queryset = Car.objects.all().order_by('-rating_count')
    serializer_class = PopularCarsSerializer


