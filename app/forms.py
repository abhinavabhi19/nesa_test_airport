from django import forms
from app.models import Airport, AirportRoute


class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['code', 'name']


class AirportRouteForm(forms.ModelForm):
    class Meta:
        model = AirportRoute
        fields = ['source', 'destination', 'position', 'distance_km']


class AddRouteSimpleForm(forms.Form):
    source_code = forms.CharField(max_length=10, label='Source Airport Code')
    destination_code = forms.CharField(max_length=10, label='Destination Airport Code')
    position = forms.ChoiceField(choices=AirportRoute.POSITION_CHOICES)
    distance_km = forms.IntegerField(min_value=1)

    def clean(self):
        cleaned = super().clean()
        source_code = cleaned.get('source_code')
        destination_code = cleaned.get('destination_code')
        if source_code and destination_code and source_code == destination_code:
            raise forms.ValidationError('Source and destination airports must be different')
        return cleaned


class ShortestRouteForm(forms.Form):
    start = forms.ModelChoiceField(queryset=Airport.objects.all())
    end = forms.ModelChoiceField(queryset=Airport.objects.all())


class NthRouteForm(forms.Form):
    start = forms.ModelChoiceField(queryset=Airport.objects.all())
    direction = forms.ChoiceField(choices=AirportRoute.POSITION_CHOICES)
    n = forms.IntegerField(min_value=1, help_text='Nth hop in chosen direction')
