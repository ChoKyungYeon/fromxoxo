from fromxoxo.decorators import *
from letter_quizapp.models import Letter_quiz


def Letter_quizCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.session_required(['choice','word','date']),
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('writer'),
            decorators.state_required(['unchecked']),
            decorators.progress_required(['progress3', 'done']),
            decorators.can_add_quiz()
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def Letter_quizListDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter, redirect=False),
            decorators.role_required('writer'),
            decorators.state_required(['unchecked']),
            decorators.progress_required(['progress3', 'done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated


def Letter_quizEditDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter_quiz, redirect=False),
            decorators.role_required('writer'),
            decorators.state_required(['unchecked']),
            decorators.progress_required(['progress3', 'done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def Letter_quizPreviewDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter_quiz, redirect=False),
            decorators.role_required('related'),
            decorators.progress_required(['done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def Letter_quizVerifyDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request, **kwargs)
        checks = [
            decorators.get_letter(Letter_quiz, redirect=True),
            decorators.progress_required(['done']),
            decorators.update_error(),
            decorators.is_locked(),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated