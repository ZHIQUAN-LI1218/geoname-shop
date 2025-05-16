from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Feature

class FeatureListView(ListView):
    model = Feature
    paginate_by = 20
    template_name = 'features/feature_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(feature_type__icontains=q)
            )
        return queryset

class FeatureDetailView(DetailView):
    model = Feature
    template_name = 'features/feature_detail.html'

