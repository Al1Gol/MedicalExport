from http import client
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
import pandas as pd
from django.conf import settings
from rest_framework.response import Response

from .serializers import ClientSerializer, OrganizationSerializer
from .models import Clients, Organizations, Bills

#Импорт клиентов
class ClientsUpdateSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Clients.objects.all()

    def get_queryset(self):
        df = pd.read_excel(f'{settings.BASE_DIR}\client_org.xlsx', sheet_name='client')
        print(df.values.tolist())

        for el in df.values.tolist():
            print(el[0])
            if not Clients.objects.filter(name = el[0]):
                create_client = Clients(name = el[0])
                create_client.save()

        return Clients.objects.all()

class OrganizationUpdateSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organizations.objects.all()

    def get(self):
        df = pd.read_excel(f'{settings.BASE_DIR}\client_org.xlsx', sheet_name='organization')


        for el in df.values.tolist():
            if not Organizations.objects.filter(name = el[1]):
                create_org = Organizations(
                    client_name = Clients.objects.get(name = el[0]),
                    name = el[1],
                    address = el[2])
                create_org.save()
        return Organizations.objects.all()

   
