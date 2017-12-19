from django import forms
from django.forms.formsets import formset_factory

class submitPollForm(forms.Form):
    '''
    A form for user to enter a question and two choices for the Create New Poll page
    '''
    question = forms.CharField(max_length=250)
    choice_1 = forms.CharField(max_length=250,required=True)
    extra_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(submitPollForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields
        print(extra_fields)


        for index in range(2,int(extra_fields)+4):
            # generate extra fields in the number specified via extra_fields
            self.fields['choice_{index}'.format(index=index)] = \
            forms.CharField(max_length=250,required=False)
