from django.urls import path
from . import views

urlpatterns = [
    path('mine_block/', views.mine_block),
    path('get_chain/', views.get_chain),
    path('is_valid/', views.is_valid),
    path('add_transaction/', views.add_transaction),
    path('connect_node/', views.connect_node),
    path('replace_chain/', views.replace_chain)
]