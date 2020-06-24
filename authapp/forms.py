from django.contrib.auth.forms import AuthenticationForm

from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['onfocus'] = "this.placeholder = ''"
            field.widget.attrs['onblur'] = f"this.placeholder = '{field.label}'"

        self.html_class_attr = 'class = "col-md-12 form-group"'

    def as_div(self):
        "Return this form rendered as HTML <div>s."
        return self._html_output(
            normal_row=f'<div {self.html_class_attr}> %(field)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True,
        )
