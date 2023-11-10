from django.http import HttpResponseForbidden
from fromxoxo.decorators import Decorators


def PhonenumberCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        decorators.phonenumber_update()
        return func(request, *args, **kwargs)
    return decorated

def UnauthenticatedDecorator(func):
    def decorated(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated


def PhonenumberVerifyDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        decorators.phonenumber_update()
        return func(request, *args, **kwargs)
    return decorated