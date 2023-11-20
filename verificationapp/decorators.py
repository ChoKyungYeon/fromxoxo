from fromxoxo.decorators import Decorators


def VerificationCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        decorators.update_verification()
        response=decorators.session_required(['update', 'search', 'signup'])
        if response:
            return response
        return func(request, *args, **kwargs)
    return decorated

def VerificationVerifyDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        decorators.update_verification()
        response=decorators.check_verification()
        if response:
            return response
        return func(request, *args, **kwargs)
    return decorated