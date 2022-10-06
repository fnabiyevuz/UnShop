from openpyxl import load_workbook
import requests
workbook = load_workbook(filename="Jayhun1.xlsx")
sheet = workbook.active
# url = 'http://127.0.0.1:8000/ipa/product/up/'
url = 'http://jayhunelectro.backoffice.uz/ipa/product/up/'

for i in range(1, 2443):
    name = str(sheet["A{}".format(i)].value)
    quantity = str(sheet["B{}".format(i)].value)
    barcode = str(sheet["H{}".format(i)].value)
    g_id = int(sheet["G{}".format(i)].value)
    price = round(sheet["F{}".format(i)].value)
    try:
        som = round(sheet["D{}".format(i)].value)
        data = {'name':name, 'quantity':quantity, 'price':price, 'barcode':barcode, 'g_id':g_id, 'som':som}
        x = requests.post(url, data=data)
        print(x.text)
    except:
        dollar = str(sheet["C{}".format(i)].value)
        data = {'name':name, 'quantity':quantity, 'price':price, 'barcode':barcode, 'g_id':g_id, 'dollar':dollar}
        x = requests.post(url, data=data)
        print(x.text)
    # Product.objects.create(name=name, som=som, barcode=barcode)