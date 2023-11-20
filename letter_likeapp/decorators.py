from fromxoxo.decorators import Decorators


def Letter_likeDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.role_required('related'),
            decorators.progress_required(['done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated
