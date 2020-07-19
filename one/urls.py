from django.urls import path
from . import views

urlpatterns = [
    path('mine_block/', views.mine_block),
    path('get_chain/', views.get_chain),
    path('is_valid/', views.is_valid),
]