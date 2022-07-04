from http import client
from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField, PrimaryKeyRelatedField, SlugRelatedField
from django.db.models import Sum

from .models import Clients, Organizations, Bills

#Cпискок клиентов
class ClientSerializer(ModelSerializer):
    count_organisations = SerializerMethodField('get_count_orgs')
    sum_bills = SerializerMethodField('get_sum_bills')
    client_name = StringRelatedField()
    client_org = StringRelatedField()
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
        if not result["sum_of_bills"]:
            result["sum_of_bills"] = 0
        return result["sum_of_bills"]
       
#Cчета клиентов
class BillsSerializer(ModelSerializer):
    client_name = StringRelatedField()
    client_org = StringRelatedField()
    class Meta:
        model = Bills
        fields = ['client_name', 'client_org', 'num', 
                  'sum', 'date', 'service', 'fraud_score', 
                  'service_class', 'service_name']
