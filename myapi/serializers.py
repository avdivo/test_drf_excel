from rest_framework import serializers

from myapi.models import Client, Bill

from django.db.models import Sum


class FileSerializer(serializers.Serializer):
    """ Проверка загружаемого файла """

    file = serializers.FileField(max_length=None, allow_empty_file=False)


class ClientSerializer(serializers.ModelSerializer):
    """ Получение информации о клиенте """
    number_of_organization = serializers.SerializerMethodField()
    sum_all = serializers.SerializerMethodField()

    class Meta:
        model = Client
        exclude = ['id']

    def get_number_of_organization(self, obj):
        return Bill.objects.filter(client=obj).count()

    def get_sum_all(self, obj):
        return Bill.objects.filter(client=obj).aggregate(sum=Sum('sum'))['sum']


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



# ---------------------------------------------------------------
class TextSerializer(serializers.Serializer):
    """ --- """
    field1 = serializers.CharField()
    field2 = serializers.CharField()
    text = serializers.CharField()
