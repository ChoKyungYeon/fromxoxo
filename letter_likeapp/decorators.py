from plancoach.decorators import Decorators
from profile_likeapp.models import Profile_like


def Profile_likeDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student= 'all', allow_superuser= False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated