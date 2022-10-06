from tablib import Dataset
from api.models import Product

def Productcreate(request):
    file = request.FILES['data']

    data = tablib.Dataset()
    data.load(fh, xlsx)