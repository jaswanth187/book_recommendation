from django.urls import path,include
from home import views
urlpatterns = [
    path('',views.index),
    path('recommender',views.recommender)
]