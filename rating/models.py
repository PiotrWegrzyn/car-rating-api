from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    rating_sum = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)

    @property
    def avg_rating(self):
        if self.rating_count:
            return self.rating_sum/self.rating_count

        return 0
