from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rating.models import Car


class CarsCreateViewTestCase(APITestCase):
    url = reverse('rating:cars-list')

    def test_create_todo(self):

        response = self.client.post(self.url, {'make': 'mercedes', 'model': 'cla-class'})
        self.assertEqual(201, response.status_code)

    def test_400_code_on_duplicate_car(self):
        self.client.post(self.url, {'make': 'mercedes', 'model': 'cla-class'})
        response = self.client.post(self.url, {'make': 'mercedes', 'model': 'cla-class'})
        self.assertEqual(400, response.status_code)

    def test_404_code_on_wrong_car(self):
        response = self.client.post(self.url, {'make': 'not_existing', 'model': 'not_existing'})
        self.assertEqual(404, response.status_code)


class RateViewTestCase(APITestCase):

    def test_correct_rate_status(self):

        car = Car.objects.create(make='mercedes', model='cla-class')
        car.save()

        url = reverse('rate', kwargs={'pk': car.id})

        response = self.client.post(url, {'id': car.id, 'rate': 5})

        self.assertEqual(200, response.status_code)

    def test_car_avg_rating(self):

        car = Car.objects.create(make='mercedes', model='cla-class')
        car.save()

        url = reverse('rate', kwargs={'pk': car.id})
        self.client.post(url, {'id': car.id, 'rate': 5})
        self.client.post(url, {'id': car.id, 'rate': 1})

        self.assertEqual(Car.objects.get(pk=car.id).avg_rating, 3)

    def test_400_code_on_incorrect_rate_value(self):
        car = Car.objects.create(make='mercedes', model='cla-class')
        car.save()

        url = reverse('rate', kwargs={'pk': car.id})

        response = self.client.post(url, {'id': car.id, 'rate': 0})

        self.assertEqual(400, response.status_code)

        response = self.client.post(url, {'id': car.id, 'rate': 6})

        self.assertEqual(400, response.status_code)


class PopularCarsViewTestCase(APITestCase):
    url = reverse('popular')

    def test_popular_list_correct_order(self):
        car1 = Car.objects.create(make='TestMake', model='TestModel1', rating_count=2)
        car1.save()
        car2 = Car.objects.create(make='TestMake', model='TestModel2', rating_count=1)
        car2.save()
        car3 = Car.objects.create(make='TestMake', model='TestModel3', rating_count=3)
        car3.save()
        car4 = Car.objects.create(make='TestMake', model='TestModel4', rating_count=7)
        car4.save()

        response = self.client.get(self.url)
        results_rating_count_in_order = tuple(el['rating_count'] for el in response.json())

        self.assertEqual((7, 3, 2, 1), results_rating_count_in_order)


class DeleteCarViewTestCase(APITestCase):

    def test_object_deleted(self):
        car = Car.objects.create(make='mercedes', model='cla-class')
        car.save()

        url = reverse('rating:cars-detail', kwargs={'pk': car.id})

        response = self.client.delete(url)

        self.assertEqual(204, response.status_code)

        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(pk=car.id)


class ListCarsViewTestCase(APITestCase):
    url = reverse('rating:cars-list')

    def test_lists_all_cars(self):
        car1 = Car.objects.create(make='TestMake', model='TestModel1', rating_count=2)
        car1.save()
        car2 = Car.objects.create(make='TestMake', model='TestModel2', rating_count=1)
        car2.save()
        car3 = Car.objects.create(make='TestMake', model='TestModel3', rating_count=3)
        car3.save()
        car4 = Car.objects.create(make='TestMake', model='TestModel4', rating_count=7)
        car4.save()

        response = self.client.get(self.url)

        self.assertEqual(4, len(response.json()))
