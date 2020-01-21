
from django import forms


class FormAliment(forms.Form):
    aliments = forms.CharField(label="aliments", max_length=200, required=False)

    def __repr__(self):
        return self.aliments

    class Meta:
        ordering = ['id']