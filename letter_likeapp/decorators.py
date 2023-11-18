from fromxoxo.decorators import Decorators


def Letter_likeDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=request.GET.get('letter_pk'))
        checks = [
            decorators.instance_owenership_required('related'),
            decorators.progress_required(['done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated
