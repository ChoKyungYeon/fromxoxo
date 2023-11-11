from datetime import datetime, timedelta
from django.shortcuts import redirect, get_object_or_404
from phonenumberapp.models import Phonenumber

class Decorators:
    def __init__(self, user, obj):
        self.user = user
        self.obj = obj

    def phonenumber_update(self): #deploy check
        for phonenumber in Phonenumber.objects.filter(is_verified=False):
            if datetime.now() - phonenumber.created_at > timedelta(minutes=3):
                phonenumber.delete()


def expire_redirector(pk, model, type):
    redirect_dict = {
        'application': 'applicationapp:expire',
        'consult': 'consultapp:expire',
        'teacherapply': 'teacherapplyapp:expire',
        'accountcreate': 'accountapp:login',
    }
    try:
        get_object_or_404(model, pk=pk)
        return None
    except:
        return redirect(redirect_dict[type]) if type in redirect_dict else None