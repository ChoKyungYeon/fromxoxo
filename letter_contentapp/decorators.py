from fromxoxo.decorators import *
from letter_contentapp.models import Letter_content


def Letter_contentUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter_content'),
            decorators.instance_owenership_required('writer'),
            decorators.state_required(['unchecked']),
            decorators.progress_required(['progress2','progress3','done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated
