from rest_framework import serializers

from myapi.models import Client, Bill


class FileSerializer(serializers.Serializer):
    """ Проверка загружаемого файла """

    file = serializers.FileField(max_length=None, allow_empty_file=False)


class ClientSerializer(serializers.ModelSerializer):
    """ Получение информации о клиенте """

    class Meta:
        model = Client
        fields = ['name']


class BillsSerializer(serializers.Serializer):
    """ Получение информации о Счетах """

    # class Meta:
    #     model = Bill
    #     fields = ['client__name']


    client = serializers.CharField()
    organization = serializers.CharField()
    number = serializers.CharField()
    sum = serializers.IntegerField()
    date = serializers.DateTimeField()
    service_class = serializers.IntegerField()
    service_name = serializers.CharField()
    fraud_score = serializers.FloatField()