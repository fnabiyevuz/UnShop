from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import BasePagination, PageNumberPagination
from datetime import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Sum


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


def month():
    date = datetime.today()
    year = date.year
    if date.month == 12:
        gte = datetime(year, date.month, 1, 0, 0, 0)
        lte = datetime(year + 1, 1, 1, 0, 0, 0)
    else:
        gte = datetime(year, date.month, 1, 0, 0, 0)
        lte = datetime(year, date.month + 1, 1, 0, 0, 0)

    return gte, lte


class TokenViewset(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer


class UserProfileViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class FilialViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Filial.objects.all()
    serializer_class = FilialSerializer


class GroupsViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer


class DeliverViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Deliver.objects.all()
    serializer_class = DeliverSerializer


class Product100Viewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['name', ]
    pagination_class = StandardResultsSetPagination


class ProductViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['name', ]

    # pagination_class = StandardResultsSetPagination

    @action(methods=['post'], detail=False)
    def add(self, request):
        r = request.data
        recieve = r['recieve']
        re = Recieve.objects.get(id=recieve)
        recieves = RecieveItem.objects.filter(recieve_id=recieve)
        for r in recieves:
            if Product.objects.filter(name=r.product.name, preparer=r.product.preparer, som=r.som, dollar=r.dollar,
                                      kurs=r.kurs):
                p = Product.objects.get(name=r.product.name, preparer=r.product.preparer, som=r.som, dollar=r.dollar,
                                        kurs=r.kurs)
                p.quantity += r.quantity
                p.save()
            else:
                Product.objects.create(name=r.product.name, group=r.product.group, preparer=r.product.preparer,
                                       quantity=r.quantity, barcode=r.product.barcode, som=r.som, dollar=r.dollar,
                                       kurs=r.kurs)
        re.status = 1
        re.save()
        return Response({'message': 'done'}, status=200)

    @action(methods=['post'], detail=False)
    def up(self, request):
        r = request.data
        name = r['name']
        g_id = int(r['g_id'])
        barcode = r['barcode']
        som = float(r['som'])
        # print(name, g_id, barcode, som)
        g = Groups.objects.get(id=g_id)
        p = Product.objects.create(name=name, group=g, som=som, barcode=barcode)

        # print(p)
        s = self.get_serializer_class()(p)

        return Response(s.data, status=200)

    @action(methods=['get'], detail=False)
    def stat(self, request):
        products = Product.objects.all()
        som = 0
        dollar = 0
        for p in products:
            som += p.som * p.quantity
            dollar += p.dollar * p.quantity
        return Response(
            {
                'som': som,
                'dollar': dollar
            }, status=200
        )
        # soms = Product.objects.all().aggregate(Sum('som'))
        # print(soms)
        # som = Product.objects.values_list('som', flat=True)
        # print(sum(som))
        # print(som[0][0]*som[0][1])
        # soms = sum(som[0][0]*som[0][1])
        # dollar = Product.objects.values_list('dollar', flat=True)
        # dollars = sum(dollar)
        # return Response(
        #     {
        #         'som':soms,
        #         'dollar':dollars
        #     }
        # )


class ProductFilialViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProductFilial.objects.all()
    serializer_class = ProductFilialSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        r = request.data
        filial = int(r['filial'])
        faktura = int(r['faktura'])
        print(filial, faktura)
        # difference = float(r['difference'])
        fakturaitems = FakturaItem.objects.filter(faktura_id=faktura)
        print(fakturaitems)
        dif = 0
        for fakturaitem in fakturaitems:
            product = ProductFilial.objects.filter(filial=filial, product__barcode=fakturaitem.barcode)
            if len(product) > 0:
                product = product.first()
                if product.price == fakturaitem.price:
                    product.quantity = product.quantity + fakturaitem.price
                else:
                    dif += (fakturaitem.price - product.price) * product.quantity
                    product.price = fakturaitem.price
                    product.debt_price = fakturaitem.debt_price
                    product.quantity = product.quantity + fakturaitem.quantity
                    product.save()
            else:
                ProductFilial.objects.create(product=fakturaitem.product, price=fakturaitem.price,
                                             debt_price=fakturaitem.debt_price, quantity=fakturaitem.quantity,
                                             filial_id=filial)
        faktur = Faktura.objects.get(id=faktura)
        faktur.difference = dif
        faktur.status = 2
        faktur.save()

        return Response({'message': 'done'}, status=200)

    @action(methods=['get'], detail=False)
    def stat(self, request):
        filial = Filial.objects.extra(
            select={
                'price': 'select sum(api_productfilial.price*api_productfilial.quantity) from api_productfilial where api_productfilial.filial_id = api_filial.id'
            }
        )
        dt = []
        for f in filial:
            t = {
                'name': f.name,
                'price': f.price
            }
            dt.append(t)

        return Response(dt, status=200)


class RecieveViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Recieve.objects.all()
    serializer_class = RecieveSerializer

    @action(methods=['get'], detail=False)
    def recieve0(self, request):
        recieve = Recieve.objects.filter(status=0)

        s = self.get_serializer_class()(recieve, many=True)
        return Response(s.data, status=200)

    @action(methods=['get'], detail=False)
    def recieve1(self, request):
        id = request.GET.get('id')
        r = Recieve.objects.get(id=id)
        r.status = 1
        r.save()

        return Response({'message': 'done'}, status=200)


class RecieveItemViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RecieveItem.objects.all()
    serializer_class = RecieveItemSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        r = request.data
        recieve = int(r['recieve'])
        product = int(r['product'])
        som = float(r['som'])
        dollar = float(r['dollar'])
        kurs = float(r['kurs'])
        quantity = float(r['quantity'])
        rec = Recieve.objects.get(id=recieve)
        try:
            r = RecieveItem.objects.create(recieve=rec, product_id=product, som=som, dollar=dollar, kurs=kurs,
                                           quantity=quantity)
            if som == 0:
                rec.dollar += dollar * quantity
                rec.save()
            else:
                rec.som += som * quantity
                rec.save()
            s = self.get_serializer_class()(r)
            return Response(s.data, status=201)
        except:
            return Response({'message': 'error'}, status=401)

    @action(methods=['get'], detail=False)
    def rv1(self, request):
        rec = request.GET.get('rec')
        revieve = RecieveItem.objects.filter(recieve_id=rec)

        s = self.get_serializer_class()(revieve, many=True)
        return Response(s.data, status=200)


class FakturaViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Faktura.objects.all()
    serializer_class = FakturaSerializer

    @action(methods=['post'], detail=False)
    def st(self, request):
        r = request.data
        faktura = int(r['faktura'])
        try:
            f = Faktura.objects.get(id=faktura)
            f.status = 1
            f.save()
            return Response({'message': 'status o`zgardi'}, status=200)
        except:
            return Response({'message': 'error'}, status=400)

    @action(methods=['get'], detail=False)
    def st1(self, request):
        fil = request.GET.get('fil')
        faktura = Faktura.objects.filter(filial_id=fil, status=1)

        s = self.get_serializer_class()(faktura, many=True)
        return Response(s.data, status=200)

    @action(methods=['get'], detail=False)
    def ombor1(self, request):
        faktura = Faktura.objects.filter(status=1)

        s = self.get_serializer_class()(faktura, many=True)
        return Response(s.data, status=200)

    @action(methods=['get'], detail=False)
    def ombor0(self, request):
        faktura = Faktura.objects.filter(status=0)

        s = self.get_serializer_class()(faktura, many=True)
        return Response(s.data, status=200)

    @action(methods=['get'], detail=False)
    def otkaz(self, request):
        fak = request.GET.get('fak')
        faktura = Faktura.objects.get(id=fak)
        items = FakturaItem.objects.filter(faktura_id=fak)
        try:
            for i in items:
                prod = Product.objects.get(id=i.product.id)
                prod.quantity += i.quantity
                prod.save()
            faktura.status = 3
            faktura.save()
            return Response({'message': 'done'}, status=200)
        except:
            return Response({'message': 'error'}, status=400)

    @action(methods=['get'], detail=False)
    def monthly(self, request):
        gte, lte = month()
        faks = Faktura.objects.filter(date__gte=gte, date__lte=lte)

        d = self.get_serializer_class()(faks, many=True)

        return Response(d.data, status=200)

    @action(methods=['get'], detail=False)
    def range(self, request):
        gte = request.GET.get('sana1')
        lte = request.GET.get('sana2')

        faks = Faktura.objects.filter(date__gte=gte, date__lte=lte)

        d = self.get_serializer_class()(faks, many=True)

        return Response(d.data, status=200)


class FakturaItemViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FakturaItem.objects.all()
    serializer_class = FakturaItemSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        r = request.data
        faktura = int(r['faktura'])
        product = int(r['product'])
        name = r['name']
        price = float(r['price'])
        debt_price = float(r['debt_price'])
        quantity = float(r['quantity'])
        barcode = r['barcode']
        try:
            prod = Product.objects.get(id=product)
            fak = Faktura.objects.get(id=faktura)
            f = FakturaItem.objects.create(faktura_id=faktura, name=name, product_id=product, price=price,
                                           debt_price=debt_price, quantity=quantity, barcode=barcode)
            fak.summa += price * quantity
            fak.save()
            prod.quantity -= quantity
            prod.save()
            s = self.get_serializer_class()(f)
            return Response(s.data, status=201)
        except:
            return Response({'message': 'error'}, status=401)

    @action(methods=['get'], detail=False)
    def st1(self, request):
        fak = request.GET.get('fak')
        faktura = FakturaItem.objects.filter(faktura_id=fak)

        s = self.get_serializer_class()(faktura, many=True)
        return Response(s.data, status=200)


class OtkazViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Otkaz.objects.all()
    serializer_class = OtkazSerializer


class OtkazItemViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = OtkazItem.objects.all()
    serializer_class = OtkazItemSerializer


class WoodFakturaViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = WoodFaktura.objects.all()
    serializer_class = WoodFakturaSerializer


class WoodFakturaItemViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = WoodFakturaItem.objects.all()
    serializer_class = WoodFakturaItemSerializer


class ShopViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        if request.method == 'POST':
            r = request.data
            summa = float(r['summa'])
            naqd = float(r['naqd'])
            plastik = float(r['plastik'])
            transfer = float(r['transfer'])
            saler = int(r['saler'])
            filial = int(r['filial'])
            difference = float(r['difference'])
            # print(summa, naqd, plastik, saler, filial, difference)
            try:
                nasiya = float(r['nasiya'])
                Shop.objects.create(summa=summa, naqd=naqd, plastik=plastik, nasiya=nasiya, transfer=transfer,
                                    saler_id=saler, difference=difference, filial_id=filial)
                fio = r['fio']
                phone1 = r['phone1']
                debts = float(r['debts'])

                try:
                    d = Debtor.objects.get(fio=fio, phone1=phone1)
                except:
                    try:
                        phone2 = r['phone2']
                        d = Debtor.objects.create(fio=fio, phone1=phone1, phone2=phone2)
                    except:
                        d = Debtor.objects.create(fio=fio, phone1=phone1)
                d.debts = debts
                d.save()
                Debt.objects.create(debtorr=d, debt=nasiya)
                return Response({'message': 'Shop qo`shildi. Debtor yangilandi'}, status=201)
            except:
                Shop.objects.create(summa=summa, naqd=naqd, plastik=plastik, transfer=transfer, difference=difference,
                                    saler_id=saler,
                                    filial_id=filial)
                return Response({'message': 'Shop qo`shildi.'}, status=201)


class CartViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class DebtorViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Debtor.objects.all()
    serializer_class = DebtorSerializer

    @action(methods=['post'], detail=False)
    def up(self, request):
        if request.method == 'POST':
            r = request.data
            try:
                fio = r['fio']
                phone1 = r['phone1']
                debts = float(r['debts'])
                d = Debtor.objects.get(fio=fio, phone1=phone1)
                d.debts = debts
                d.save()
                return Response({'message': 'Debtor update bo`ldi.'}, status=200)
            except:
                return Response({'message': 'data not found'}, status=400)
        else:
            return Response({'message': 'error'}, status=400)


class DebtViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer


class PayHistoryViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PayHistory.objects.all()
    serializer_class = PayHistorySerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        if request.method == 'POST':
            r = request.data
            try:
                fio = r['fio']
                phone1 = r['phone1']
                summa = float(r['summa'])
                filial = int(r['filial'])
                d = Debtor.objects.get(fio=fio, phone1=phone1)
                try:
                    PayHistory.objects.create(debtor=d, sum=summa, filial_id=filial)
                    d.debts = d.debts - summa
                    d.save()
                    return Response({'message': 'To`lov qabul qilindi.'}, 200)
                except:
                    return Response({'message': 'error'}, 401)
            except:
                return Response({'message': 'data not found'}, status=400)
        else:
            return Response({'message': 'error'}, 401)


class CartDebtViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CartDebt.objects.all()
    serializer_class = CartDebtSerializer


class ReturnProductViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ReturnProduct.objects.all()
    serializer_class = ReturnProductSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        if request.method == 'POST':
            r = request.data
            try:
                product = int(r['product'])
                return_quan = float(r['return_quan'])
                summa = float(r['summa'])
                filial = r['filial']
                difference = float(r['difference'])
                status = int(r['status'])
                barcode = r['barcode']
                try:
                    ReturnProduct.objects.create(product_id=product, filial_id=filial,
                                                 return_quan=return_quan, summa=summa, difference=difference,
                                                 status=status, barcode=barcode)
                    prod = ProductFilial.objects.filter(filial_id=filial, product__barcode=barcode).first()
                    prod.quantity += return_quan
                    prod.save()
                    if status == 1:
                        fio = r['fio']
                        phone1 = r['phone1']
                        d = Debtor.objects.get(fio=fio, phone1=phone1)
                        d.debts = d.debts - summa
                        d.save()
                    return Response({'message': 'done'}, 200)
                except:
                    return Response({'message': 'create qilishda xatolik'}, 401)
            except:
                return Response({'message': 'data not found'}, 401)
        else:
            return Response({'message': 'error'}, 401)
