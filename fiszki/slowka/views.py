from django.http import JsonResponse, HttpRequest  # <-- Dodajemy HttpRequest do typowania


def szukaj_slowka(request: HttpRequest):
    """
    Endpoint wyszukiwania.
    """
    # Używamy requesta do logowania (teraz zmienna jest 'used')
    print(f"Szukam słówka dla metody: {request.method} na ścieżce: {request.path}")

    return JsonResponse({"message": "Wyszukiwarka w budowie"})


def ping(request: HttpRequest):
    """
    Healthcheck.
    """
    # Nawet w ping warto sprawdzić, czy request przyszedł
    if request.method == 'GET':
        return JsonResponse({"status": "pong"})
    return JsonResponse({"status": "error", "message": "Only GET allowed"}, status=405)