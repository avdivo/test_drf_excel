from django.db import models


# Клиенты
class Client(models.Model):
    name = models.CharField(max_length=32, blank=False, unique=True, verbose_name=u'Клиент')  # Название клиента

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


# Организации
class Organization(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Связь с таблицей Клиенты
    name = models.CharField(max_length=32, blank=False, unique=True, verbose_name=u'Организация')
    address = models.CharField(max_length=256, verbose_name=u'Адрес организации')
    fraud_weight = models.IntegerField(blank=False, default=0, verbose_name=u'Мошенничество')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


# Счета организаций
class Bill(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Связь с таблицей Клиенты
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)  # Связь с таблицей Организации
    number = models.CharField(max_length=32, verbose_name=u'Номер счета')
    sum = models.IntegerField(default=0, verbose_name=u'Сумма')
    date = models.DateTimeField(blank=True, verbose_name=u'Дата создания')
    service_class = models.IntegerField(blank=True, null=True, verbose_name=u'Номер')
    service_name = models.CharField(max_length=64, blank=True, verbose_name=u'Услуга')
    fraud_score = models.FloatField(blank=False, default=0, verbose_name=u'Показатель мошеничества')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def save(self, *args, **kwargs):
        """ Переопроеделение метода Save для рассчета суммы мошенничества """
        if self.fraud_score >= 0.9:
            self.organization.fraud_weight += 1
            self.organization.save()
        super(Bill, self).save(*args, **kwargs)


