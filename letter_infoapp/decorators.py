from fromxoxo.decorators import *
from letter_infoapp.models import Letter_info


def Letter_infoUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter_info, redirect=False),
            decorators.role_required('writer'),
            decorators.state_required(['unchecked']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated
