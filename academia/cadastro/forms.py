from django import forms
from .models import UsuarioC

class UsuarioCForm(forms.ModelForm):
    class Meta:
        model = UsuarioC
        fields = '__all__'

    widgets = {
        'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        'genero': forms.Select(),
        'observacao': forms.Textarea(attrs={'rows': 4}),
    }

    senha = forms.CharField(widget=forms.PasswordInput())
    ConfirmarSenha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'}))

    # Validação de campos de senha
    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        ConfirmarSenha = cleaned_data.get('ConfirmarSenha')

        # Valida se as senhas coincidem
        if senha and ConfirmarSenha:
            if senha != ConfirmarSenha:
                raise forms.ValidationError("As senhas não coincidem")

        return cleaned_data