from django import forms
from .models import Profession, LaborFunction, LaborAction, RequiredKnowledge, RequiredSkill,    GeneralizedLaborFunction, OKSO
from django.forms import inlineformset_factory

LaborActionFormSet = inlineformset_factory(
    LaborFunction,
    LaborAction,
    fields=('description',),
    extra=1,
    can_delete=True
)

RequiredKnowledgeFormSet = inlineformset_factory(
    LaborFunction,
    RequiredKnowledge,
    fields=('description',),
    extra=1,
    can_delete=True
)

RequiredSkillFormSet = inlineformset_factory(
    LaborFunction,
    RequiredSkill,
    fields=('description',),
    extra=1,
    can_delete=True
)

class ProfessionForm(forms.ModelForm):
    class Meta:
        model = Profession
        fields = ['name', 'code', 'okpdtr_code']

class LaborFunctionForm(forms.ModelForm):
    class Meta:
        model = LaborFunction
        fields = ['name', 'qualification_level', 'generalized_function']

class GeneralizedLaborFunctionForm(forms.ModelForm):
    class Meta:
        model = GeneralizedLaborFunction
        fields = ['code', 'name']

class OKSOForm(forms.ModelForm):
    class Meta:
        model = OKSO
        fields = ['code']