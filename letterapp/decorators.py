from fromxoxo.decorators import *


def LetterSessionDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        decorators.register_session('from')
        return func(request, *args, **kwargs)
    return decorated

def LetterExpireDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        response=decorators.session_required(['none','saved'])
        if response:
            return response
        return func(request, *args, **kwargs)
    return decorated

def LetterFinishDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('writer'),
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
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('saver'),
            decorators.state_required(['saved']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('writer'),
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
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('writer'),
            decorators.progress_required(['progress3'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterSaveDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.state_required(['checked']),
            decorators.role_required('unrelated'),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterUnsaveDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('saver'),
            decorators.state_required(['saved']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterResetDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('writer'),
            decorators.state_required(['checked']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterPreviewDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('related'),
            decorators.progress_required(['done']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def LetterResultDecorator(func):
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

def LetterIntroDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=True),
            decorators.progress_required(['done']),
            decorators.update_error(),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated


def LetterDetailDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=True),
            decorators.quiz_redirector(),
            decorators.progress_required(['done']),
            decorators.update_error(),
            decorators.is_locked(),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated