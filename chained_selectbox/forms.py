from django import forms
from django.http import request
import json

# This can be used for django internal requests
from django.test.client import Client


class ChainedChoicesForm(forms.ModelForm):
    """
    Form class to be used with ChainedChoiceField and ChainedSelect widget
    If there is already an instance (i.e. editing) then the options will be
    loaded when the form is built.
    """
    def __init__(self, *args, **kwargs):
        super(ChainedChoicesForm, self).__init__(*args, **kwargs)
        if 'data' in kwargs:
            clie = Client()
            prefix = kwargs['prefix']
            for field_name, field in self.base_fields.items():
                if hasattr(field, 'parent_field'):
                    self.initial[field_name] = (
                        kwargs['data'][prefix + '-' + field_name])
                    parent_value = (
                        kwargs['data'][prefix + '-' + field.parent_field])
                    article = clie.get(field.ajax_url, {
                            'field_name': field_name,
                            'parent_value': parent_value
                            }, HTTP_HOST='localhost')
                    self.fields[field_name].choices = (
                        json.loads(article.content))
        elif 'instance' in kwargs:
            instance = kwargs['instance']
            clie = Client()

            for field_name, field in self.fields.items():
                if hasattr(field, 'parent_field'):
                    article = clie.get(field.ajax_url, {
                        'field_name': field_name,
                        'parent_value': getattr(instance, field.parent_field)
                    }, HTTP_HOST='localhost')
                    field.choices = json.loads(article.content)
        elif len(args) > 0 and type(args[0]) is request.QueryDict:
            instance = args[0]
            clie = Client()

            for field_name, field in self.fields.items():
                if hasattr(field, 'parent_field'):
                    article = clie.get(field.ajax_url, {
                        'field_name': field_name,
                        'parent_value': instance.get(field.parent_field, None)
                    }, HTTP_HOST='localhost')
                    field.choices = json.loads(article.content)
