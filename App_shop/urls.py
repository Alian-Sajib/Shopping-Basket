from django.urls import path
from App_shop  import views
app_name = 'App_shop'

urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    
]
