from django.db import models
from django.contrib.auth.models import User


class Filial(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Filial'


class UserProfile(models.Model):
    staffs = [
        (1, 'director'),
        (2, 'manager'),
        (3, 'saler'),
        (4, 'warehouse')
    ]
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    staff = models.IntegerField(choices=staffs, default=3)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name_plural = 'User'


class Groups(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Group'


class Deliver(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Deliver'


class Product(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True)
    preparer = models.CharField(max_length=255, null=True, blank=True)
    som = models.FloatField(default=0)
    dollar = models.FloatField(default=0, null=True, blank=True)
    kurs = models.FloatField(default=0, null=True, blank=True)
    quantity = models.FloatField(default=0, null=True, blank=True)
    barcode = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Product'


class ProductFilial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    debt_price = models.FloatField()
    quantity = models.FloatField(default=0)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=255)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'Product Filial'


class Recieve(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    deliver = models.ForeignKey(Deliver, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    som = models.FloatField(default=0)
    dollar = models.FloatField(default=0)
    status = models.IntegerField(default=0)

    # difference = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Recieve'


class RecieveItem(models.Model):
    recieve = models.ForeignKey(Recieve, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    som = models.FloatField(default=0)
    dollar = models.FloatField(default=0)
    kurs = models.FloatField(default=0)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'RecieveItem'


class Faktura(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    summa = models.FloatField(default=0)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    difference = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Faktura'


class FakturaItem(models.Model):
    name = models.CharField(max_length=255)
    faktura = models.ForeignKey(Faktura, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    debt_price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    barcode = models.CharField(max_length=255)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'FakturaItem'


class Otkaz(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Otkaz'


class OtkazItem(models.Model):
    otkaz = models.ForeignKey(Otkaz, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    barcode = models.CharField(max_length=255)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'OtkazItem'


class WoodFaktura(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    summa = models.FloatField(default=0)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    difference = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'WoodFaktura'


class WoodFakturaItem(models.Model):
    woodfaktura = models.ForeignKey(WoodFaktura, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    debt_price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    barcode = models.CharField(max_length=255)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'WoodFakturaItem'


class Shop(models.Model):
    summa = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    naqd = models.FloatField(default=0)
    plastik = models.FloatField(default=0)
    nasiya = models.FloatField(default=0)
    transfer = models.FloatField(default=0)
    difference = models.FloatField(default=0)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    saler = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Shop'


class Cart(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductFilial, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()
    total = models.FloatField(blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     self.total = int(self.quantity) * self.product.price
    #     super().save(*args, **kwargs)

    def __str__(self):
        try:
            return self.product.product.name
        except:
            return 'Deleted Product'

    class Meta:
        verbose_name_plural = 'Cart'


class Debtor(models.Model):
    fio = models.CharField(max_length=255)
    phone1 = models.CharField(max_length=13)
    phone2 = models.CharField(max_length=13, blank=True, null=True)
    debts = models.FloatField(default=0)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name_plural = 'Nasiyachilar'


#
# class DebtHistory(models.Model):
#     debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE)
#     product = models.ForeignKey(ProductFilial, on_delete=models.CASCADE)
#     price = models.IntegerField(default=0)
#     debt_quan = models.IntegerField(default=0)
#     pay_quan = models.IntegerField(default=0)
#     debt = models.IntegerField(default=0)
#     pay = models.IntegerField(default=0)
#     difference = models.IntegerField(default=0)
#
#     class Meta:
#         verbose_name_plural = '8) Nasiya Tarixi'


class Debt(models.Model):
    debtorr = models.ForeignKey(Debtor, on_delete=models.CASCADE)
    debt = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.debtorr.fio

    class Meta:
        verbose_name_plural = 'Qarz Tarixi'


class PayHistory(models.Model):
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    sum = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.debtor.fio

    class Meta:
        verbose_name_plural = 'Tolov Tarixi'


class CartDebt(models.Model):
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductFilial, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    given_quan = models.FloatField(default=0)
    total = models.FloatField(default=0)
    return_quan = models.FloatField(default=0)
    return_sum = models.FloatField(default=0)
    debt_quan = models.FloatField(default=0)
    debt_sum = models.FloatField(default=0)
    difference = models.FloatField(default=0)

    def __str__(self):
        return self.debtor.fio + " / " + self.product.product.name

    class Meta:
        verbose_name_plural = 'CartDebt'


class ReturnProduct(models.Model):
    product = models.ForeignKey(ProductFilial, on_delete=models.CASCADE)
    return_quan = models.FloatField(default=0)
    summa = models.FloatField(default=0)
    difference = models.FloatField(default=0)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(default=0)
    barcode = models.CharField(max_length=255)

    def __str__(self):
        return self.product.product.name

    class Meta:
        verbose_name_plural = 'Return Product'
