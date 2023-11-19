from fromxoxo.decorators import *

def Letter_quizCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter'),
            decorators.instance_owenership_required('writer'),
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
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter'),
            decorators.instance_owenership_required('writer'),
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
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter_quiz'),
            decorators.instance_owenership_required('writer'),
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
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.instance_update('letter_quiz'),
            decorators.instance_owenership_required('related'),
            decorators.progress_required(['done'])
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated

def Letter_quizVerifyDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, object_pk=kwargs['pk'])
        checks = [
            decorators.letter_redirector('letter_quiz'),
            decorators.progress_required(['done']),
        ]
        for check in checks:
            if check:
                return check
        return func(request, *args, **kwargs)
    return decorated