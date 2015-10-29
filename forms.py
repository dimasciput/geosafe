__author__ = 'ismailsunni'
from datetime import datetime
import logging

from django.forms import models
from django import forms

from geonode.layers.models import Layer

from geosafe.models import Metadata, Analysis

LOG = logging.getLogger(__name__)


class MetadataUploadForm(models.ModelForm):
    """A form for creating an event."""

    class Meta:
        model = Metadata
        fields = (
            'layer',
            'metadata_file'
        )

    layer = forms.ModelChoiceField(
        label='Layer',
        help_text='Layer for the Metadata',
        required=True,
        queryset=Layer.objects.order_by(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    metadata_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MetadataUploadForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(MetadataUploadForm, self).save(commit=False)
        LOG.error(instance)
        instance.user = self.user
        instance.date_created = datetime.utcnow()
        instance.save()
        return instance


class MetadataUpdateForm(models.ModelForm):
    """A form for creating an event."""

    class Meta:
        model = Metadata
        fields = (
            'metadata_file',
        )

    metadata_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MetadataUpdateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(MetadataUpdateForm, self).save(commit=False)
        LOG.error(instance)
        instance.user = self.user
        # instance.date_created = datetime.utcnow()
        instance.save()
        return instance


class AnalysisCreationForm(models.ModelForm):
    """A form for creating an event."""

    class Meta:
        model = Analysis

    exposure_layer = forms.ModelChoiceField(
        label='Exposure Layer',
        required=True,
        queryset=Layer.objects.filter(metadata__layer_purpose='exposure'),
        widget=forms.Select(
            attrs={'class': 'form-control'})
    )

    hazard_layer = forms.ModelChoiceField(
        label='Exposure Layer',
        required=True,
        queryset=Layer.objects.filter(metadata__layer_purpose='hazard'),
        widget=forms.Select(
            attrs={'class': 'form-control'})
    )

    aggregation_layer = forms.ModelChoiceField(
        label='Exposure Layer',
        required=True,
        queryset=Layer.objects.filter(metadata__layer_purpose='aggregation'),
        widget=forms.Select(
            attrs={'class': 'form-control'})
    )