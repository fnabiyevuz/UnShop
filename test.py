
from api.models import Filial

fil = Filial.objects.all()

for f in fil:
    print(f.name)