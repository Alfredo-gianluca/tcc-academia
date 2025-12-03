import re
from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):

    senha = forms.CharField(
        widget=forms.PasswordInput(),
        help_text="A senha deve conter no mínimo 8 caracteres, incluindo letra maiúscula, minúscula e número."
    )

    Confirmar_Senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'})
    )

    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.TextInput(attrs={'placeholder': 'dd/mm/aaaa'}),
            'genero': forms.Select(),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
            'fotoperfil': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control'
            }),
        }

    def clean_senha(self):
        senha = self.cleaned_data.get("senha")

        if len(senha) < 8:
            raise forms.ValidationError("A senha deve ter no mínimo 8 caracteres.")
        if not re.search(r"[A-Z]", senha):
            raise forms.ValidationError("A senha deve conter pelo menos 1 letra maiúscula.")
        if not re.search(r"[a-z]", senha):
            raise forms.ValidationError("A senha deve conter pelo menos 1 letra minúscula.")
        if not re.search(r"[0-9]", senha):
            raise forms.ValidationError("A senha deve conter pelo menos 1 número.")

        return senha

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar = cleaned_data.get('Confirmar_Senha')

        if senha and confirmar and senha != confirmar:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data