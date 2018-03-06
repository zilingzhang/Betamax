from django import forms

from .models import Room


class CreateFrom(forms.ModelForm):

	room = forms.ChoiceField(choices=[(rm.id,str(rm)) for rm in Room.objects.all()])

	class Meta:
		model = Room
		fields = ('roomnumber',)