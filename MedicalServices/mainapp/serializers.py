from rest_framework.serializers import ModelSerializer, StringRelatedField

from .models import Clients, Organizations, Bills

#Cпискок клиентов
class ClientSerializer(ModelSerializer):
    count_orgs = Organizations.objects.all()
    class Meta:
        model = Clients
        fields = ['name', 'count_orgs']

#Список организаций
class OrganizationSerializer(ModelSerializer):
    class Meta:
        client_name = StringRelatedField()
        model = Organizations
        fields = ['client_name', 'name', 'address']

#Cчета клиентов
class BillsSerializer(ModelSerializer):
    class Meta:
        client_name = StringRelatedField()
        model = Bills
        fields = ['client_name', 'client_org', 'num', 
                  'sum', 'date', 'service', 'fraud_score', 
                  'service_class', 'service_name']
