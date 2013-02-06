from alternativa.ambiente import ambiente


def add_ambiente(request):
    """
    Devuelve los datos del ambiente
    """
    return {'ambiente': ambiente }
