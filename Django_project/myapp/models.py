from django.db import models

# Create your models here.
class  Person(models.Model):
    # max_length จำกัดจำนวนความยาว
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    date = models.DateField(auto_now_add=True)

#เเปลง object เป็น string
    def __str__(self):
        return self.name + "," + str(self.age)
