from openpyxl import load_workbook
import requests
workbook = load_workbook(filename="eski.xlsx")
sheet = workbook.active
# url = 'http://127.0.0.1:8000/ipa/product/up/'
url = 'http://unshop.backoffice.uz/ipa/product/up/'

for i in range(3255, 4495):
    if len(str(int(sheet["A{}".format(i)].value))) < 2:
        barcode = "000"+str(int(sheet["A{}".format(i)].value))
    elif len(str(int(sheet["A{}".format(i)].value))) < 3:
        barcode = "00" + str(int(sheet["A{}".format(i)].value))
    elif len(str(int(sheet["A{}".format(i)].value))) < 4:
        barcode = "0" + str(int(sheet["A{}".format(i)].value))

    else:
        barcode = "" + str(int(sheet["A{}".format(i)].value))

    name = str(sheet["B{}".format(i)].value)
    som = round(sheet["C{}".format(i)].value)
    g_id = int(sheet["D{}".format(i)].value)
    data = {'name':name, 'som':som, 'barcode':barcode, 'g_id':g_id}
    x = requests.post(url, data=data)
    print(x.text)
    # Product.objects.create(name=name, som=som, barcode=barcode)