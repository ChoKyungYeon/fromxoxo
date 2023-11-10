

@method_decorator(PhonenumberCreateDecorator, name='dispatch')
class PhonenumberCreateMixin(CreateView):
    model = Phonenumber
    form_class = PhonenumberCreateForm
    def form_valid(self, form):
        number = form.cleaned_data['number']
        phonenumbers = get_user_model().objects.values_list('phonenumber', flat=True)
        with transaction.atomic():
            if len(number) <11 or number[:3] != '010':
                form.add_error('number', '정확한 전화번호를 입력해 주세요')
                return self.form_invalid(form)
            if self.condition(number, phonenumbers):
                form.add_error('number', self.error_message)
                return self.form_invalid(form)
            try:  # deploy check
                import fromxoxo.settings.local
                form.instance.verification_code=111111
            except:
                form.instance.verification_code=random.randint(100000, 999999)
            form.instance.save()
            to = form.instance.number
            content = f'{self.sms_message} {form.instance.verification_code}를 3분 내에 입력해 주세요'
            Send_SMS(to, content, True)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(self.reverse_url, kwargs={'pk': self.object.pk})

    def condition(self, number, usernames):
        raise NotImplementedError()


@method_decorator(UnauthenticatedDecorator, name='dispatch')
class PhonenumberSignupCreateView(PhonenumberCreateMixin):
    template_name = 'phonenumberapp/signupcreate.html'
    reverse_url = 'phonenumberapp:signupverify'
    sms_message = '인증번호'
    error_message = '이미 존재하는 전화번호입니다.'

    def condition(self, number, usernames):
        return number in usernames


@method_decorator(login_required, name='dispatch')
class PhonenumberUpdateCreateView(PhonenumberCreateMixin):
    form_class = PhonenumberUpdateForm
    template_name = 'phonenumberapp/updatecreate.html'
    reverse_url = 'phonenumberapp:updateverify'
    sms_message = '인증번호'
    error_message = '이미 존재하는 전화번호입니다.'

    def condition(self, number, usernames):
        return number in usernames

@method_decorator(UnauthenticatedDecorator, name='dispatch')
class PhonenumberSearchCreateView(PhonenumberCreateMixin):
    template_name = 'phonenumberapp/searchcreate.html'
    reverse_url = 'phonenumberapp:searchverify'
    sms_message = '인증번호'
    error_message = '가입되지 않은 전화번호 입니다.'

    def condition(self, number, usernames):
        return number not in usernames
