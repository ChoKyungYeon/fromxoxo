from django.forms import Select, RadioSelect


class NullSelect(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if index == 0:
            option['label'] = '선택'
        return option
