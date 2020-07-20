import hashlib
import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, SetPasswordForm, PasswordChangeForm

from authapp.models import ShopUser, UserProfile


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


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'password1', 'password2', 'age')

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

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Только для совершеннолетних")

        return data

    def save(self, commit=True):
        user = super().save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = forms.HiddenInput()
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


class ShopUserChangePassword(PasswordChangeForm):
    class Meta:
        model = ShopUser
        fields = ('old_password', )

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


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('tagline', 'aboutMe', 'gender')

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
