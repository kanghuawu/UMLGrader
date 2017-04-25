from django import forms
from .models import TenantData, TenantFields
import django_tables2 as tables

class GradeForm(forms.ModelForm):
	class Meta:
		model = TenantData
		TF = TenantFields.objects.filter(tenant_id='khwu').order_by('field_column')
		TF_length = TF.count()
		TF_name = list(TF.values_list('field_name', flat=True))
		fields = [f.name for f in TenantData._meta.get_fields()][3:TF_length+3]
		labels = dict(zip(fields, TF_name))
		
class ClassSeqDiagram(forms.Form):
	DIA_CHOICES = ((1, 'Class'), (2, 'Sequence'))
	choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=DIA_CHOICES)