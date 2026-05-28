# users/context_processors.py
from pharmacy.utils import menu  # assuming you moved menu to pharmacy/utils.py

def pharmacy_context(request):
    return {'mainmenu': menu, 'categories': ... , 'tags': ...}