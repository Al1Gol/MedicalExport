from django.db import models

#Клиентские организации
class Organizations(models.Model):
    client_name = models.ForeignKey('Clients', on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=300)
    address = models.CharField(max_length=1000)

#Клиенты
class Clients(models.Model):
    name = models.CharField(unique=True, max_length=300)

#Счета организации
class Org_bills(models.Model):
    client_name = models.ForeignKey('Clients', on_delete=models.CASCADE)
    client_org = models.ForeignKey('Organizations', on_delete=models.CASCADE)
    id = models.BigIntegerField(primary_key=True, default=None)
    sum = models.DecimalField(max_digits= 10,decimal_places=2)
    date = models.DateField()
    service = models.CharField(max_length=1000)
    fraud_score = models.FloatField()
    service_class = models.IntegerField()
    service_name = models.CharField(max_length=100)