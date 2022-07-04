from http import client
from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField
from django.db.models import Sum

from .models import Clients, Organizations, Bills

#Cпискок клиентов
class ClientSerializer(ModelSerializer):
    count_organisations = SerializerMethodField('get_count_orgs')
    sum_bills = SerializerMethodField('get_sum_bills')
    class Meta:
        model = Clients
        fields = ['name', 'count_organisations', 'sum_bills']

    #Количество организаций для каждого клиента
    def get_count_orgs(self, obj):
        get_orgs = Organizations.objects.filter(client_name = obj.id)
        return len(get_orgs)

    #Сумма по всем счетам
    def get_sum_bills(self, obj):
        get_bills = Bills.objects.filter(client_name = obj.id)
        result = get_bills.aggregate(sum_of_bills=Sum('sum'))
        return result["sum_of_bills"]
       
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
