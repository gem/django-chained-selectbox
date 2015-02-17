from chained_selectbox.forms import ChainedChoicesForm
from django import forms
from example2.models import C
from chained_selectbox.form_fields import ChainedChoiceField


class CForm(ChainedChoicesForm):
    class Meta:
        model = C

    name = forms.CharField(label="name", max_length=255)

    field_one = forms.ChoiceField(label="field one", choices=(
            ('', '------------'), (1, '1'), (2, '2'),
            (3, '3'), (4, '4'), (5, '5'), ))
    field_two = ChainedChoiceField(label="field two",
                                   parent_field='field_one',
                                   ajax_url='/chainedselectchoices')
    field_three = ChainedChoiceField(label="field three",
                                     parent_field='field_two',
                                     ajax_url='/chainedselectchoices')
