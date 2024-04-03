from django.db import models
from django.db.models.query import QuerySet
from django.forms import fields, widgets
import django_filters
from .models import FAQ, Cat
from django import forms

class FAQFilter(django_filters.FilterSet):
    cat = django_filters.ModelChoiceFilter(
        queryset = Cat.objects.all(),
        label = "Category"
    )
    class Meta:
        models = FAQ
        fields = {
            'cat' : ['exact']
        }
        field_labels={
            'cat': 'Category',
        }