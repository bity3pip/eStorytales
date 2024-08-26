from .models import Card


def card_item_count(request):
    if request.user.is_authenticated:
        card, created = Card.objects.get_or_create(user=request.user)
        return {'card': card}
    return {'card': None}


def cart_context(request):
    if request.user.is_authenticated:
        card, created = Card.objects.get_or_create(user=request.user)
        return {'card': card}
    return {'card': None}
