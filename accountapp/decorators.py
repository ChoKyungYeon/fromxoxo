from fromxoxo.decorators import *

def AccountLoginDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        decorators.register_session('redirect_pk')
        return func(request, *args, **kwargs)
    return decorated


def AccountOwnershipDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        response =decorators.ownership_required()
        if response:
            return response
        return func(request, *args, **kwargs)
    return decorated

def AccountCharacterUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.ownership_required(),
            decorators.session_required(['heart', 'animal','christmas'])
        ]
        for check in checks:
            if check:
                return check

        return func(request, *args, **kwargs)
    return decorated

def AccountCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        response =decorators.verification_required()
        if response:
            return response
        return func(request, *args, **kwargs)
    return decorated


def AccountLetterListDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        decorators.update_user()
        response =decorators.ownership_required()
        if response:
            return response
        return func(request, *args, **kwargs)
    return decorated
