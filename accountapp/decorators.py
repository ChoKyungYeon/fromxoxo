from fromxoxo.decorators import *

def AccountOwnershipDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.user_owenership_required(),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated


def AccountLetterListDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.user_update(),
            decorators.user_owenership_required(),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated
