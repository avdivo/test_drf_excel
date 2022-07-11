from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import BaseParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from detect_fraud import detect_fraud
from service_classifier import service_classifier
from .models import *
from .serializers import *

import re
import json
import pandas


class FileUploadViewSet(viewsets.ViewSet):
    """ Класс для загрузки файлов XLSX """

    def create(self, request):
        print(request)
        serializer_class = FileSerializer(data=request.data)
        if 'file' not in request.FILES or not serializer_class.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # Принимаем файлы только с именем bills.xlsx или client_org.xlsx
            if request.FILES['file'].name == 'bills.xlsx':
                # Читаем счета
                excel_data_df = pandas.read_excel(request.FILES['file'])
                bills = json.loads(excel_data_df.to_json(date_format='iso'))

                # Заполняем таблицу счетов
                for i in range(len(bills['client_name'])):
                    client = Client.objects.get(name=bills['client_name'][str(i)])
                    organization = Organization.objects.get(name=bills['client_org'][str(i)])
                    serv = service_classifier('')
                    key = list(serv.keys())[0]
                    Bill.objects.create(client=client, organization=organization,
                                        number=bills['№'][str(i)], sum=bills['sum'][str(i)],
                                        date=str(bills['date'][str(i)]),
                                        fraud_score=detect_fraud(bills['service'][str(i)]),
                                        service_class=key, service_name=serv[key])

            elif request.FILES['file'].name == 'client_org.xlsx':
                # Читаем клиентов и организации
                excel_data_df = pandas.read_excel(request.FILES['file'], sheet_name='client')
                clients = json.loads(excel_data_df.to_json())
                excel_data_df = pandas.read_excel(request.FILES['file'], sheet_name='organization')
                organizations = json.loads(excel_data_df.to_json())

                # # Заполняем таблицу клиентов
                for row in clients['name'].values():
                    Client.objects.create(name=row)

                # Заполняем таблицу организаций
                for i in range(len(organizations['client_name'])):
                    client = Client.objects.get(name=organizations['client_name'][str(i)])
                    re.match(r'^\s|-*$', 'd')
                    Organization.objects.create(client=client, name=organizations['name'][str(i)],
                                                address='Адрес: ' + organizations['address'][str(i)] if not re.match(
                                                    r'^\s|-*$',
                                                    organizations['address'][str(i)]) else '')

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_201_CREATED)


class ClientAPIView(generics.ListAPIView):
    """ Информация о клиентах """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class BillAPIView(generics.ListAPIView):
    """ Информация о клиентах """
    queryset = Bill.objects.all()
    serializer_class = BillsSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['client__name', 'organization__name']





# ----------------------------------------------------------

class PlainTextParser(MultiPartParser):
    """
    Plain text parser.
    """
    media_type = 'multipart/form-data'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        if result.files['file'].content_type == 'text/plain':
            ret_dict = result.data.copy()
            ret_dict.__setitem__('text', result.files['file'].read())
        return ret_dict



class TextAPIView(generics.CreateAPIView):
    """ Загрузка текстового файла и вывод егона экран """
    parser_classes = (PlainTextParser,)
    serializer_class = TextSerializer

    def create(self, request):
        return Response(request.data)
