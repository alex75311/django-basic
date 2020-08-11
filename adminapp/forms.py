from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from authapp.forms import forms

from authapp.models import ShopUser
from mainapp.models import Product, Category
from orderapp.models import Order, OrderItem


class RootAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['onfocus'] = "this.placeholder = ''"
            field.widget.attrs['onblur'] = f"this.placeholder = '{field.label}'"
            field.widget.attrs['style'] = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

        self.html_class_attr = 'class = "col-md-12 form-group"'

    def as_div(self):
        "Return this form rendered as HTML <div>s."
        return self._html_output(
            normal_row=f'<div {self.html_class_attr}> %(field_name)s<br> %(field)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True,
        )


class AdminShopCreateUser(RootAdminForm, UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'is_superuser', 'email', 'age', 'avatar', 'password1', 'password2')

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Несовершеннолетний')
        return data


class AdminEditUserProfile(RootAdminForm, UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'is_superuser', 'is_active', 'email', 'age', 'avatar', 'is_staff', 'password')

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Несовершеннолетний')
        return data


class AdminCategoryCreate(RootAdminForm):
    class Meta:
        model = Category
        fields = ('name',)


class AdminCategoryEdit(RootAdminForm):
    class Meta:
        model = Category
        fields = ('name',)


class AdminProductCreate(RootAdminForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image', 'quantity', 'category')


class AdminProductEdit(RootAdminForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image', 'quantity', 'category')


class AdminOrderEdit(RootAdminForm):
    class Meta:
        model = Order
        fields = '__all__'


class AdminOrderItemEdit(RootAdminForm):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ProductCategoryEditForm(RootAdminForm, forms.ModelForm):
    discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = Category
        fields = '__all__'
