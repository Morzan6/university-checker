
from services_model.models import *


Dict = Service.status.values("name", "url")
print(Dict)
