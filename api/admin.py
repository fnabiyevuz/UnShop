from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *

admin.site.site_header = "UnShop Admin Panel"
admin.site.site_title = "UnShop API"
admin.site.index_title = "UnShop API"

admin.site.unregister(Group)


# admin.site.unregister(User)
# admin.site.register(Groups)


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'first_name', 'last_name', 'phone', 'filial')


@admin.register(Groups)
class Groups(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Deliver)
class Deliver(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'som', 'dollar', 'kurs', 'quantity', 'barcode', 'group',)
    search_fields = ('id', 'name', 'som', 'dollar', 'kurs', 'quantity', 'barcode', 'group__name',)
    list_filter = ('group',)
    list_display_links = ('id', 'name')


@admin.register(ProductFilial)
class ProductFilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'debt_price', 'quantity', 'filial', 'barcode')
    search_fields = ('id', 'product__product__name', 'price', 'debt_price', 'quantity', 'filial', 'barcode')
    list_filter = ('filial',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'naqd', 'plastik', 'nasiya', 'transfer', 'difference', 'summa', 'date', 'saler', 'filial')
    search_fields = (
    'id', 'naqd', 'plastik', 'nasiya', 'transfer', 'difference', 'summa', 'date', 'saler__first_name', 'filial__name')
    date_hierarchy = 'date'
    list_filter = ('filial', 'saler')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'product', 'quantity', 'total')
    search_fields = ('id', 'shop__id', 'product__product__name', 'quantity', 'total')


@admin.register(Recieve)
class RecieveAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'som', 'dollar', 'date')
    search_fields = ('id', 'name', 'som', 'dollar', 'date')
    date_hierarchy = 'date'
    list_display_links = ('id', 'name')


@admin.register(RecieveItem)
class RecieveItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'recieve', 'product', 'som', 'dollar', 'kurs', 'quantity')
    search_fields = ('id', 'recieve__id', 'product', 'som', 'dollar', 'kurs', 'quantity')


@admin.register(Faktura)
class FakturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'summa', 'filial', 'date', 'status')
    search_fields = ('id', 'summa', 'filial__name', 'date', 'status')
    date_hierarchy = 'date'
    list_filter = ('filial',)


@admin.register(FakturaItem)
class FakturaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'faktura', 'product', 'price', 'debt_price', 'quantity', 'barcode')
    search_fields = ('id', 'faktura__id', 'product__name', 'price', 'debt_price', 'quantity', 'barcode')
    list_filter = ('faktura',)


@admin.register(Otkaz)
class OtkazAdmin(admin.ModelAdmin):
    list_display = ('id', 'filial', 'date', 'status')
    search_fields = ('id', 'filial__name', 'date', 'status')
    date_hierarchy = 'date'
    list_filter = ('filial',)


@admin.register(OtkazItem)
class OtkazItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'otkaz', 'product', 'quantity', 'barcode')
    search_fields = ('id', 'otkaz__id', 'product__name', 'quantity', 'barcode')
    list_filter = ('otkaz',)


@admin.register(WoodFaktura)
class WoodFakturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'summa', 'filial', 'date', 'status')
    search_fields = ('id', 'summa', 'filial__name', 'date', 'status')
    date_hierarchy = 'date'
    list_filter = ('filial',)


@admin.register(WoodFakturaItem)
class WoodFakturaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'woodfaktura', 'product', 'price', 'debt_price', 'quantity', 'barcode')
    search_fields = ('id', 'woodfaktura__id', 'product__name', 'price', 'debt_price', 'quantity', 'barcode')
    list_filter = ('woodfaktura',)


@admin.register(Debtor)
class DebtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'phone1', 'phone2', 'debts')
    search_fields = ('id', 'fio', 'phone1', 'phone2', 'debts')


# @admin.register(DebtHistory)
# class DebtHistoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'debtor', 'product', 'debt_quan', 'pay_quan', 'debt', 'pay', 'difference')
#     search_fields = ('id', 'debtor', 'product', 'debt_quan', 'pay_quan', 'debt', 'pay', 'difference')
#     list_filter = ('debtor',)


@admin.register(PayHistory)
class PayHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'debtor', 'sum', 'date')
    search_fields = ('id', 'debtor__fio', 'sum', 'date')
    list_filter = ('debtor',)
    date_hierarchy = 'date'


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('id', 'debtorr', 'debt', 'date')
    search_fields = ('id', 'debtorr__fio', 'debt', 'date')
    list_filter = ('debtorr',)
    date_hierarchy = 'date'


#
# @admin.register(CartDebt)
# class CartDebtAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'debtor', 'product', 'price', 'given_quan', 'total', 'return_quan', 'return_sum', 'debt_quan', 'debt_sum',
#         'difference')
#     search_fields = (
#         'id', 'debtor', 'product', 'price', 'given_quan', 'total', 'return_quan', 'return_sum', 'debt_quan', 'debt_sum',
#         'difference')


@admin.register(ReturnProduct)
class ReturnProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'return_quan', 'summa', 'difference', 'date')
    search_fields = ('id', 'product__product__name', 'return_quan', 'summa', 'difference', 'date')
    date_hierarchy = 'date'
