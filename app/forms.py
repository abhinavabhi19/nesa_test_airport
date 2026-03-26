from django import forms
from app.models import Airport, AirportRoute


# Common CSS class (reuse for consistency)
INPUT_CLASS = "border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"


class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['code', 'name']
        widgets = {
            'code': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }


class AirportRouteForm(forms.ModelForm):
    class Meta:
        model = AirportRoute
        fields = ['source', 'destination', 'position', 'distance_km']
        widgets = {
            'source': forms.Select(attrs={'class': INPUT_CLASS}),
            'destination': forms.Select(attrs={'class': INPUT_CLASS}),
            'position': forms.Select(attrs={'class': INPUT_CLASS}),
            'distance_km': forms.NumberInput(attrs={'class': INPUT_CLASS}),
        }


class AddRouteSimpleForm(forms.Form):
    source_code = forms.CharField(
        max_length=10,
        label='Source Airport Code',
        widget=forms.TextInput(attrs={'class': INPUT_CLASS})
    )
    destination_code = forms.CharField(
        max_length=10,
        label='Destination Airport Code',
        widget=forms.TextInput(attrs={'class': INPUT_CLASS})
    )
    position = forms.ChoiceField(
        choices=AirportRoute.POSITION_CHOICES,
        widget=forms.Select(attrs={'class': INPUT_CLASS})
    )
    distance_km = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASS})
    )

    def clean(self):
        cleaned = super().clean()
        source_code = cleaned.get('source_code')
        destination_code = cleaned.get('destination_code')

        if source_code and destination_code and source_code == destination_code:
            raise forms.ValidationError('Source and destination airports must be different')

        return cleaned


class ShortestRouteForm(forms.Form):
    start = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        widget=forms.Select(attrs={'class': INPUT_CLASS})
    )
    end = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        widget=forms.Select(attrs={'class': INPUT_CLASS})
    )


class NthRouteForm(forms.Form):
    start = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        widget=forms.Select(attrs={'class': INPUT_CLASS})
    )
    direction = forms.ChoiceField(
        choices=AirportRoute.POSITION_CHOICES,
        widget=forms.Select(attrs={'class': INPUT_CLASS})
    )
    n = forms.IntegerField(
        min_value=1,
        help_text='Nth hop in chosen direction',
        widget=forms.NumberInput(attrs={'class': INPUT_CLASS})
    )