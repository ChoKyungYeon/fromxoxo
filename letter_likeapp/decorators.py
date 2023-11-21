from fromxoxo.decorators import Decorators
from letterapp.models import Letter


def Letter_likeDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('related'),
            decorators.progress_required(['done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated
