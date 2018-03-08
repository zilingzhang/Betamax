from django import forms

from .models import Room


class CreateForm(forms.ModelForm):

	rooms = Room.objects.filter(active=True)
	room = forms.ModelChoiceField(queryset=rooms, required=True)
	class Meta:
		model = Room
		
		exclude = ('id','building','roomnumber','active')

	def clean(self):
		blding = self.cleaned_data['building']
		rm_numb = self.cleaned_data['roomnumber']
		room = Room.objects.filter(roomnumber=rm_numb, building=blding)
		if room is None:
			self._errors["building"] = "This room is currently not being tracked."
		if room.count() > 1:
			self._errors["building"] = "There are currently multple rooms with this designation,\n Please contact a Beta-max admin to solve this issue."
		if not room[0].active:
			self._errors["building"] = "Beta-Max is not currently operating in this room"


		return