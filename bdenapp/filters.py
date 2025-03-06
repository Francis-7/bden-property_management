import django_filters
from .models import Property
from django.db.models import Q

class PropertyFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(label='Search by Location or description or type of property', method='filter_by_query')

    class Meta:
        model = Property
        fields = []

    def filter_by_query(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(location__icontains=value) |
                Q(description__icontains=value) |
                Q(typeChoice__icontains=value)
            )
        return queryset