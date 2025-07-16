from django import forms
from tables.models import Table


class TableForm(forms.ModelForm):
    
    class Meta:
        model = Table
        fields = '__all__'