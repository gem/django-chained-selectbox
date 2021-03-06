from django.forms.widgets import Select
from django.contrib.admin.templatetags.admin_static import static
from django.utils.safestring import mark_safe
from django.conf import settings


class ChainedSelect(Select):
    """
    A ChoiceField widget where the options for the selectare dependant on the
    value of the parent select field.
    When the parent field is changed an ajax call is made to determine the
    options.

    Form must inherit from ChainedChoicesForm which loads the options when
    there is already an instance.

    class StandardModelForm(ChainedChoicesForm):
        field_one = forms.ChoiceField(choices=(('', '------------'), (1, '1'),
            (2, '2'), (3, '3'), (4, '4'), (5, '5'), ))
        field_two = ChainedChoiceField(parent_field='field_one',
                                       ajax_url='/chainedselectchoices')
        field_three = ChainedChoiceField(parent_field='field_two',
                                         ajax_url='/chainedselectchoices')

    """
    def __init__(self, parent_field=None, ajax_url=None, item_index=None,
                 *args, **kwargs):
        self.parent_field = parent_field
        self.ajax_url = ajax_url
        self.item_index = 0
        if item_index:
            self.item_index = item_index

        super(ChainedSelect, self).__init__(*args, **kwargs)

    class Media:
        extra = '' if settings.DEBUG else '.min'
        js = [static('admin/js/jquery%s.js' % extra),
              static('admin/js/jquery.init.js'),
              static('js/chained-select.js')]

    def render(self, name, value, attrs={}, choices=()):
        field_prefix = attrs['id'][:attrs['id'].rfind('-') + 1]

        if not field_prefix:
            paretnfield_id = "id_" + self.parent_field
        else:
            paretnfield_id = field_prefix + self.parent_field

        attrs['ajax_url'] = self.ajax_url

        output = super(ChainedSelect, self).render(name, value, attrs=attrs,
                                                   choices=choices)
        js = """
        <script type="text/javascript">
        //<![CDATA[
        (function($) {
            $(document).ready(function(){
                var parent_field = $("#%(paretnfield_id)s");
                parent_field.addClass('chained-parent-field');
                parent_field.attr('chained_id%(item_index)d',
                                  "%(chained_id)s");
                parent_field.on('change', function(e) {
                    $(this).loadChainedChoices();
                });
            })
        })(django.jQuery);
        //]]>
        </script>

        """ % {"paretnfield_id": paretnfield_id, 'item_index': self.item_index,
               'chained_id': attrs['id']}

        output += js

        return mark_safe(output)
