from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, F, Value
from django.views.generic import TemplateView
from api.models import *
from django.db.models import Q
from datetime import datetime
from django.http.response import JsonResponse
import json
from django.contrib.auth.mixins import LoginRequiredMixin


def monthly():
    date = datetime.today()
    year = date.year
    if date.month == 12:
        gte = datetime(year, date.month, 1, 0, 0, 0)
        lte = datetime(year + 1, 1, 1, 0, 0, 0)
    else:
        gte = datetime(year, date.month, 1, 0, 0, 0)
        lte = datetime(year, date.month + 1, 1, 0, 0, 0)

    return gte, lte


def ChartHome(request):
    kirim = []
    chiqims = []
    chiqimd = []
    for i in range(1, 13):
        date = datetime.today()
        year = date.year
        if i == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = i + 1
            year2 = year
        gte = str(year) + '-' + str(i) + '-01 00:00:00'
        lte = str(year2) + '-' + str(month2) + '-01 00:00:00'
        # kirr = Shop.objects.filter(date__gte=gte, date__lte=lte).aggregate(kir = Sum('naqd')+Sum('plastik')+Sum('nasiya'))
        kirr = Shop.objects.filter(date__gte=gte, date__lte=lte)
        payhis = PayHistory.objects.filter(date__gte=gte, date__lte=lte)
        p = 0
        for pi in payhis:
            p += pi.sum
        k = 0
        for kir in kirr:
            k += kir.naqd + kir.plastik
        k = k + p
        chs = 0
        chd = 0
        chiqq = Recieve.objects.filter(date__gte=gte, date__lte=lte)
        for chiq in chiqq:
            chs += chiq.som
            chd += chiq.dollar
        kirim.append(k)
        chiqims.append(chs)
        chiqimd.append(chd)
    # data = [kirim, chiqim]
    dt = {
        # 'data': data,
        'kirim': kirim,
        'chiqims': chiqims,
        'chiqimd': chiqimd,
    }
    return JsonResponse(dt)


def FilialKirim(request):
    fil1 = []
    fil2 = []
    for i in range(1, 13):
        date = datetime.today()
        year = date.year
        if i == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = i + 1
            year2 = year
        gte = str(year) + '-' + str(i) + '-01 00:00:00'
        lte = str(year2) + '-' + str(month2) + '-01 00:00:00'
        a = Shop.objects.filter(date__gte=gte, date__lte=lte).values('filial').annotate(
            num=Sum('naqd') + Sum('plastik'))
        try:
            fil1.append(a[0]['num'])
        except:
            fil1.append('0')
        try:
            fil2.append(a[1]['num'])
        except:
            fil2.append('0')

    dt = {
        # 'data': data,
        'filial1': fil1,
        'filial2': fil2,
    }
    return JsonResponse(dt)


def SalerKirim(request):
    saler1 = []
    saler2 = []
    saler3 = []
    for i in range(1, 13):
        date = datetime.today()
        year = date.year
        if i == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = i + 1
            year2 = year
        gte = str(year) + '-' + str(i) + '-01 00:00:00'
        lte = str(year2) + '-' + str(month2) + '-01 00:00:00'
        a = Shop.objects.filter(date__gte=gte, date__lte=lte).values('saler').annotate(num=Sum('naqd') + Sum('plastik'))
        try:
            saler1.append(a[0]['num'])
        except:
            saler1.append('0')
        try:
            saler2.append(a[1]['num'])
        except:
            saler2.append('0')
        try:
            saler3.append(a[2]['num'])
        except:
            saler3.append('0')

    dt = {
        # 'data': data,
        'saler1': saler1,
        'saler2': saler2,
        'saler3': saler3,
    }
    return JsonResponse(dt)


def Summa(request):
    gte, lte = monthly()
    shops = Shop.objects.filter(date__gte=gte, date__lte=lte)
    naqd = 0
    plastik = 0
    nasiya = 0
    transfer = 0
    for shop in shops:
        naqd = naqd + shop.naqd
        plastik = plastik + shop.plastik
        nasiya = nasiya + shop.nasiya
        transfer = transfer + shop.transfer
    summ = naqd + plastik + nasiya + transfer
    dt = {
        'naqd': naqd,
        'plastik': plastik,
        'nasiya': nasiya,
        'transfer': transfer,
        'summ': summ,
    }
    return JsonResponse(dt)


def Qoldiq(request):
    fil = Filial.objects.extra(
        select={
            'qol': 'select sum(api_productfilial.price * api_productfilial.quantity) from api_productfilial where api_productfilial.filial_id = api_filial.id'
        }
    )
    fils = []
    for f in fil:
        fils.append(f.name)
    filq = []
    for f in fil:
        if f.qol:
            filq.append(f.qol)
        else:
            filq.append(0)
    dt = {
        'qoldiq': filq,
        'filial': fils
    }
    return JsonResponse(dt)


def DataHome(request):
    data = json.loads(request.body)
    date1 = data['date1']
    date2 = data['date2']
    salers = UserProfile.objects.extra(
        select={
            'naqd': 'select sum(api_shop.naqd) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                date1, date2),
            'plastik': 'select sum(api_shop.plastik) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                date1, date2),
            'nasiya': 'select sum(api_shop.nasiya) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                date1, date2),
            'transfer': 'select sum(api_shop.transfer) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                date1, date2)
        }
    )
    filials = Filial.objects.extra(
        select={
            'naqd': 'select sum(api_shop.naqd) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                date1, date2),
            'plastik': 'select sum(api_shop.plastik) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                date1, date2),
            'nasiya': 'select sum(api_shop.nasiya) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                date1, date2),
            'transfer': 'select sum(api_shop.transfer) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                date1, date2),
            'pay': 'select sum(api_payhistory.sum) from api_payhistory where api_payhistory.filial_id = api_filial.id and api_payhistory.date > "{}" and api_payhistory.date < "{}"'.format(
                date1, date2)
        }
    )
    shops = Shop.objects.filter(date__gte=date1, date__lte=date2)
    naqd = 0
    plastik = 0
    nasiya = 0
    transfer = 0
    for shop in shops:
        naqd = naqd + shop.naqd
        plastik = plastik + shop.plastik
        nasiya = nasiya + shop.nasiya
        transfer = transfer + shop.transfer
    summ = naqd + plastik + nasiya + transfer
    print("transfer" , transfer)
    if summ > 0:
        se = []
        for saler in salers:
            s = {
                'name': saler.first_name,
                'staff': saler.staff,
                'filial': saler.filial.name,
                'naqd': saler.naqd,
                'plastik': saler.plastik,
                'nasiya': saler.nasiya,
                'transfer': saler.transfer,
            }

            se.append(s)

        fl = []
        for filial in filials:
            t = {
                'name': filial.name,
                'naqd': filial.naqd,
                'plastik': filial.plastik,
                'nasiya': filial.nasiya,
                'transfer': filial.transfer,
                'pay': filial.pay,
            }
            fl.append(t)
        dt1 = {
            'salers': se,
            'filials': fl,
            'naqd': naqd,
            'plastik': plastik,
            'nasiya': nasiya,
            'transfer': transfer,
            'summ': summ,
            'naqdf': round(naqd / summ * 100, 2),
            'plastikf': round(plastik / summ * 100, 2),
            'nasiyaf': round(nasiya / summ * 100, 2),
            'transferf': round(transfer / summ * 100, 2),
        }
    else:
        se = []
        for saler in salers:
            s = {
                'name': saler.first_name,
                'staff': saler.staff,
                'filial': saler.filial.name,
                'naqd': 0,
                'plastik': 0,
                'nasiya': 0,
                'transfer': 0,
            }
            se.append(s)
        fl = []
        for filial in filials:
            t = {
                'name': filial.name,
                'naqd': 0,
                'plastik': 0,
                'nasiya': 0,
                'transfer': 0,
            }
            fl.append(t)

        dt1 = {
            'salers': se,
            'filials': fl,
            'naqd': 0,
            'plastik': 0,
            'nasiya': 0,
            'transfer': 0,
            'summ': 0,
            'plastikf': 0,
            'nasiyaf': 0,
            'naqdf': 0,
            'transferf': 0,
        }
    return JsonResponse(dt1)


def DataWare(request):
    data = json.loads(request.body)
    date1 = data['date1']
    date2 = data['date2']
    wares = Recieve.objects.filter(date__gte=date1, date__lte=date2)
    wr = []
    for w in wares:
        t = {
            'id': w.id,
            'name': w.name,
            'deliver': w.deliver,
            'som': w.som,
            'dollar': w.dollar,
            'date': w.date.strftime("%d-%m-%y %I:%M")

        }
        wr.append(t)
    dt1 = {
        'wares': wr
    }
    return JsonResponse(dt1)


def GetItem(request):
    data = json.loads(request.body)
    id = data['id']
    items = RecieveItem.objects.filter(recieve_id=id)
    it = []
    for i in items:
        its = {
            'id': i.id,
            'product': i.product.name,
            'som': i.som,
            'dollar': i.dollar,
            'kurs': i.kurs,
            'quantity': i.quantity
        }
        it.append(its)
    dt1 = {
        'items': it
    }
    return JsonResponse(dt1)


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        gte, lte = monthly()
        salers = UserProfile.objects.extra(
            select={
                'naqd': 'select sum(api_shop.naqd) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'plastik': 'select sum(api_shop.plastik) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'nasiya': 'select sum(api_shop.nasiya) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'transfer': 'select sum(api_shop.transfer) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte)
            }
        )
        filials = Filial.objects.extra(
            select={
                'naqd': 'select sum(api_shop.naqd) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'plastik': 'select sum(api_shop.plastik) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'nasiya': 'select sum(api_shop.nasiya) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'transfer': 'select sum(api_shop.transfer) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'pay': 'select sum(api_payhistory.sum) from api_payhistory where api_payhistory.filial_id = api_filial.id and api_payhistory.date > "{}" and api_payhistory.date < "{}"'.format(
                    gte, lte)
            }
        )
        shops = Shop.objects.filter(date__gte=gte, date__lte=lte)
        naqd = 0
        plastik = 0
        nasiya = 0
        transfer = 0
        for shop in shops:
            naqd = naqd + shop.naqd
            plastik = plastik + shop.plastik
            nasiya = nasiya + shop.nasiya
            transfer = transfer + shop.transfer
        summ = naqd + plastik + nasiya + transfer

        jami = 0
        try:
            for f in filials:
                jami += f.naqd + f.plastik + f.nasiya + f.pay + f.transfer
        except:
            pass
        context = super(Home, self).get_context_data(*args, **kwargs)
        context['home'] = 'active'
        context['home_t'] = 'true'
        context['salers'] = salers
        context['filials'] = filials
        context['jami'] = jami

        if summ != 0:
            context['naqd'] = naqd
            context['plastik'] = plastik
            context['nasiya'] = nasiya
            context['transfer'] = transfer
            context['summ'] = summ
            context['naqdf'] = round(naqd / summ * 100, 2)
            context['plastikf'] = round(plastik / summ * 100, 2)
            context['nasiyaf'] = round(nasiya / summ * 100, 2)
            context['transferf'] = round(transfer / summ * 100, 2)
        else:
            context['naqd'] = 0
            context['plastik'] = 0
            context['nasiya'] = 0
            context['summ'] = 0
            context['naqdf'] = 0
            context['plastikf'] = 0
            context['nasiyaf'] = 0
        return context


class Products(LoginRequiredMixin, TemplateView):
    template_name = 'product.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Products, self).get_context_data(*args, **kwargs)
        context['productfilials'] = ProductFilial.objects.all()
        context['product'] = 'active'
        context['product_t'] = 'true'

        return context


class Filials(LoginRequiredMixin, TemplateView):
    template_name = 'filial.html'

    def get_context_data(self, *args, **kwargs):
        gte, lte = monthly()
        jami = 0
        filials = Filial.objects.extra(
            select={
                'naqd': 'select sum(api_shop.naqd) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'plastik': 'select sum(api_shop.plastik) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'nasiya': 'select sum(api_shop.nasiya) from api_shop where api_shop.filial_id = api_filial.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'pay': 'select sum(api_payhistory.sum) from api_payhistory where api_payhistory.filial_id = api_filial.id and api_payhistory.date > "{}" and api_payhistory.date < "{}"'.format(
                    gte, lte)
            }
        )
        try:
            for f in filials:
                jami += f.naqd + f.plastik + f.nasiya + f.pay
        except:
            pass
        context = super(Filials, self).get_context_data(*args, **kwargs)
        context['filial'] = 'active'
        context['filial_t'] = 'true'
        context['jami'] = jami
        context['filials'] = filials

        return context


class Saler(LoginRequiredMixin, TemplateView):
    template_name = 'saler.html'

    def get_context_data(self, *args, **kwargs):
        gte, lte = monthly()
        salers = UserProfile.objects.extra(
            select={
                'naqd': 'select sum(api_shop.naqd) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'plastik': 'select sum(api_shop.plastik) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte),
                'nasiya': 'select sum(api_shop.nasiya) from api_shop where api_shop.saler_id = api_userprofile.id and api_shop.date > "{}" and api_shop.date < "{}"'.format(
                    gte, lte)
            }
        )
        jami = 0
        for s in salers:
            try:
                jami += s.naqd + s.plastik + s.nasiya
            except:
                pass
        context = super(Saler, self).get_context_data(*args, **kwargs)
        context['saler'] = 'active'
        context['saler_t'] = 'true'
        context['salers'] = salers
        context['jami'] = jami
        return context


class Ombor(LoginRequiredMixin, TemplateView):
    template_name = 'ombor.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Ombor, self).get_context_data(*args, **kwargs)
        context['ombor'] = 'active'
        context['ombor_t'] = 'true'
        context['ombors'] = Product.objects.all()

        return context


class OmborQabul(LoginRequiredMixin, TemplateView):
    template_name = 'omborqabul.html'

    def get_context_data(self, *args, **kwargs):
        gte, lte = monthly()
        context = super(OmborQabul, self).get_context_data(*args, **kwargs)
        context['ombor'] = 'active'
        context['ombor_t'] = 'true'
        context['wares'] = Recieve.objects.filter(date__gte=gte, date__lte=lte)
        # for r in Recieve.objects.filter(date__gte=gte, date__lte=lte):
        return context


class OmborMinus(LoginRequiredMixin, TemplateView):
    template_name = 'omborminus.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OmborMinus, self).get_context_data(*args, **kwargs)
        context['ombor'] = 'active'
        context['ombor_t'] = 'true'
        context['ombors'] = Product.objects.filter(quantity__lte=100).order_by('quantity')

        return context


class Fakturas(LoginRequiredMixin, TemplateView):
    template_name = 'faktura.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Fakturas, self).get_context_data(*args, **kwargs)
        context['ombor'] = 'active'
        context['ombor_t'] = 'true'
        context['fakturas'] = Faktura.objects.filter(status=1)
        context['fakturaitems'] = FakturaItem.objects.all()

        return context


class FakturaTarix(LoginRequiredMixin, TemplateView):
    template_name = 'fakturatarix.html'

    def get_context_data(self, *args, **kwargs):
        gte, lte = monthly()
        context = super(FakturaTarix, self).get_context_data(*args, **kwargs)
        context['ombor'] = 'active'
        context['ombor_t'] = 'true'
        context['fakturas'] = Faktura.objects.filter(date__gte=gte, date__lte=lte)

        return context


class WareFakturas(LoginRequiredMixin, TemplateView):
    template_name = 'warefaktura.html'

    def get_context_data(self, request, *args, **kwargs):
        context = super(WareFakturas, self).get_context_data(*args, **kwargs)
        context['warefakturas'] = 'active'
        context['warefakturas_t'] = 'true'
        context['fakturas'] = Faktura.objects.filter(status=1)
        context['fakturaitems'] = FakturaItem.objects.all()

        return context


class WareFakturaTarix(LoginRequiredMixin, TemplateView):
    template_name = 'warefakturatarix.html'

    def get_context_data(self, *args, **kwargs):
        gte, lte = monthly()
        context = super(WareFakturaTarix, self).get_context_data(*args, **kwargs)
        context['warefakturatarix'] = 'active'
        context['warefakturatarix_t'] = 'true'
        context['fakturas'] = Faktura.objects.filter(date__gte=gte, date__lte=lte)

        return context


def GetFakturaItem(request):
    data = json.loads(request.body)
    id = data['id']
    items = FakturaItem.objects.filter(faktura_id=id)
    it = []
    for i in items:
        its = {
            'id': i.id,
            'product': i.product.name,
            'price': i.price,
            'debt': i.debt_price,
            'quantity': i.quantity
        }
        it.append(its)
    dt1 = {
        'items': it
    }
    return JsonResponse(dt1)


def DataFak(request):
    data = json.loads(request.body)
    date1 = data['date1']
    date2 = data['date2']
    wares = Faktura.objects.filter(date__gte=date1, date__lte=date2)
    wr = []
    for w in wares:
        t = {
            'id': w.id,
            'summa': w.summa,
            'filial': w.filial.name,
            'difference': w.difference,
            'date': w.date.strftime("%d-%m-%y %I:%M")

        }
        wr.append(t)
    dt1 = {
        'wares': wr
    }
    return JsonResponse(dt1)


class Table(TemplateView):
    template_name = 'table.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Table, self).get_context_data(*args, **kwargs)
        context['table'] = 'active'
        context['table_t'] = 'true'

        return context


class DataTable(TemplateView):
    template_name = 'datatable.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DataTable, self).get_context_data(*args, **kwargs)
        context['datatable'] = 'active'
        context['datatable_t'] = 'true'

        return context


class Hodim(LoginRequiredMixin, TemplateView):
    template_name = 'hodim.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Hodim, self).get_context_data(*args, **kwargs)
        context['hodim'] = 'active'
        context['hodim_t'] = 'true'
        context['salers'] = UserProfile.objects.filter(~Q(staff=1))
        context['filials'] = Filial.objects.all()

        return context


class Debtors(LoginRequiredMixin, TemplateView):
    template_name = 'debtor.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Debtors, self).get_context_data(*args, **kwargs)
        context['debtor'] = 'active'
        context['debtor_t'] = 'true'
        context['debtors'] = Debtor.objects.all()

        return context


def DebtorHistory(request):
    gte, lte = monthly()
    d_id = request.GET.get('d')
    pays = PayHistory.objects.filter(date__gte=gte, date__lte=lte, debtor_id=d_id)
    debts = Debt.objects.filter(date__gte=gte, date__lte=lte, debtorr_id=d_id)
    psum = 0
    dsum = 0
    for p in pays:
        psum += p.sum
    for d in debts:
        dsum += d.debt

    context = {
        'psum': psum,
        'dsum': dsum,
        'pays': pays,
        'debts': debts,
        'd_id': d_id,
        'debtor': "active",
        'debtor_t': "true"
    }

    return render(request, 'nasiyahistory.html', context)

def NasiyaTarix(request):
    data = json.loads(request.body)
    date1 = data['date1']
    date2 = data['date2']
    d_id = data['d_id']
    # print(date1, date2, d_id)
    pays = PayHistory.objects.filter(date__gte=date1, date__lte=date2, debtor_id=d_id)
    debts = Debt.objects.filter(date__gte=date1, date__lte=date2, debtorr_id=d_id)
    psum = 0
    dsum = 0
    for p in pays:
        psum += p.sum
    for d in debts:
        dsum += d.debt
    pay = []
    for w in pays:
        print("p")
        t = {
            # 'id': w.id,
            'sum': w.sum,
            'date': w.date,
        }
        pay.append(t)
    debt = []
    for w in debts:
        print("d")
        t = {
            # 'id': w.id,
            'sum': w.debt,
            'date': w.date,
        }
        debt.append(t)
    dt1 = {
        'psum': psum,
        'dsum': dsum,
        'pays': pay,
        'debts': debt,
    }
    return JsonResponse(dt1)


class Profile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Profile, self).get_context_data(*args, **kwargs)
        context['home_t'] = 'true'
        # context['user'] = UserProfile.objects.get(username)

        return context


class ProfileSetting(TemplateView):
    template_name = 'profile-setting.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileSetting, self).get_context_data(*args, **kwargs)
        context['home_t'] = 'true'

        return context


class SweetAlert(TemplateView):
    template_name = 'sweet-alert.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SweetAlert, self).get_context_data(*args, **kwargs)
        context['sweet_alert'] = 'active'
        context['sweet_alert_t'] = 'true'

        return context


class Date(TemplateView):
    template_name = 'date.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Date, self).get_context_data(*args, **kwargs)
        context['date'] = 'active'
        context['date_t'] = 'true'

        return context


class Widget(TemplateView):
    template_name = 'widget.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Widget, self).get_context_data(*args, **kwargs)
        context['widget'] = 'active'
        context['widget_t'] = 'true'

        return context


def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login yoki Parol notogri kiritildi!')
            return redirect('login')
    else:
        return render(request, 'login.html')


def Logout(request):
    logout(request)
    messages.success(request, "Tizimdan chiqish muvaffaqiyatli yakunlandi!")
    return redirect('login')
