# users/context_processors.py
from pharmacy.utils import menu

def pharmacy_context(request):
    return {'mainmenu': menu}