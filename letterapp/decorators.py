from fromxoxo.decorators import *



def LetterWriteInfoDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter'),
            decorators.instance_owenership_required('writer'),
            decorators.progress_required(['done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterSaveInfoDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter'),
            decorators.instance_owenership_required('saver'),
            decorators.state_required(['saved']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterFinishDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter'),
            decorators.instance_owenership_required('writer'),
            decorators.state_required(['unchecked']),
            decorators.progress_required(['done']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterSavedDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter'),
            decorators.instance_owenership_required('saver'),
            decorators.state_required(['saved']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_owenership_required('writer'),
            decorators.state_required(['unchecked']),
            decorators.progress_required(['done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterProgressUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=request.GET.get('letter_pk'))
        checks = [
            decorators.instance_owenership_required('writer'),
            decorators.progress_required(['progress3'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterSaveDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=request.GET.get('letter_pk'))
        checks = [
            decorators.state_required(['checked']),
            decorators.instance_owenership_required('unrelated'),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterUnsaveDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=request.GET.get('letter_pk'))
        checks = [
            decorators.instance_owenership_required('saver'),
            decorators.state_required(['saved']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterResetDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=request.GET.get('letter_pk'))
        checks = [
            decorators.instance_owenership_required('writer'),
            decorators.state_required(['checked']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterIntroDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=request.GET.get('letter_pk'))
        checks = [
            decorators.instance_update('letter'),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated