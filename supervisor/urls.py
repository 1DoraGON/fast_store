
from django.urls import path, include

from supervisor.views import CreateSupervisorView, ItemList, add_category, CreateItemView, dashboard, get_email,CategoryListView

app_name='supervisor'

urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('add-supervisor/',CreateSupervisorView.as_view(),name='add-supervisor'),
    path('add-category/',add_category,name='add-category'),
    path('get-email/',get_email,name='get-email'),
    path('tables/',ItemList.as_view(),name='tables'),
    path('add-item/',CreateItemView.as_view(),name='add-item'),
    path('tables/categories/',CategoryListView.as_view(),name='categories'),
]
