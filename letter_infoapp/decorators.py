from fromxoxo.decorators import *
from letter_infoapp.models import Letter_info


def Letter_infoUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter_info'),
            decorators.instance_owenership_required('writer'),
            decorators.state_required(['unchecked']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated
