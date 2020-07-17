from django.contrib.auth.decorators import login_required

from basketapp.models import Basket


@login_required
def get_basket(request):

    if request.user:
        basket = Basket.objects.filter(user=request.user)
    else:
        basket = [1, 2, 3]
    return {'basket': basket}
