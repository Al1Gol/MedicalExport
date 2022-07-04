from http import client
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, mixins
import pandas as pd
from django.conf import settings
from rest_framework.response import Response

from modules.classifier import classifier
from modules.detector import detector
from .serializers import ClientSerializer, BillsSerializer
from .models import Clients, Organizations, Bills

#Вьюсет импорта данных из таблиц Excel
class ImportViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = BillsSerializer
    queryset = Bills.objects.all()

    def get_queryset(self):

        #Обновление списка клиентов
        df = pd.read_excel(rf'{settings.BASE_DIR}\client_org.xlsx', sheet_name='client')

        for el in df.values.tolist():
            if not Clients.objects.filter(name = el[0]):
                create_client = Clients(name = el[0])
                create_client.save()

        #Обновление списка организаций   
        df = pd.read_excel(rf'{settings.BASE_DIR}\client_org.xlsx', sheet_name='organization')
  
        for el in df.values.tolist():
            if not Organizations.objects.filter(name = el[1]).filter(client_name__name=el[0]):
                create_org = Organizations(
                    client_name = Clients.objects.get(name = el[0]),
                    name = el[1],
                    address = el[2])
                create_org.save()

        '''На данный момент при появлении совпадений по полю "№",
        API оставляет в БД исходную запись, игнорируя последующие дубликаты.
        В зависимости от требований к проекту можно доработать/изменить данный 
        функционал(например настроить обработку исключений, оповещать о событии в логах и т.д.)'''

        #Обновление списка счетов
        df = pd.read_excel(rf'{settings.BASE_DIR}\bills.xlsx', sheet_name='Лист1')

        for el in df.values.tolist():
            if not Bills.objects.filter(num = el[2]).filter(client_org__name = el[1]): 
                service_classifier = classifier(el[5])
                create_bills = Bills(
                        client_name = Clients.objects.get(name = el[0]),
                        client_org = Organizations.objects.get(name = el[1]),
                        num = el[2],
                        sum = el[3],
                        date = el[4],
                        service = el[5],
                        fraud_score = detector(el[1]),
                        service_class = service_classifier['service_class'],
                        service_name = service_classifier['service_name'])
                create_bills.save()

        return Bills.objects.all().order_by('client_name').order_by('num')

#Вьюсет просмотра списка клиентов
class ClientsViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = ClientSerializer
    queryset = Clients.objects.all()

#Вьюсет просмотра списка счетов c фильтрацией
class BillsViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = BillsSerializer
    queryset = Bills.objects.all()

    def get_queryset(self):
        client_name = self.request.query_params.get('client_name', None)
        client_org = self.request.query_params.get('client_org', None)
        #Фильтрация по клиенту и организации
        if client_name and client_org:
            return Bills.objects.all().filter(client_name__name__contains=client_name).filter(client_org__name=client_org)
        #Фильтрация по клиенту
        elif client_name:
            return Bills.objects.all().filter(client_name__name__contains=client_name)
        #Фильтрация по организации
        elif client_org: 
            return Bills.objects.all().filter(client_org__name__contains=client_org)
        #Вывод без фильртрации
        else:
            return Bills.objects.all()