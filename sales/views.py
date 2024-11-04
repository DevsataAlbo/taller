from django.shortcuts import render

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class SaleListView(LoginRequiredMixin, ListView):
    template_name = 'sales/list.html'
    context_object_name = 'sales'
    
    def get_queryset(self):
        return []  
