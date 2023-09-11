"""Like Url Pathways"""
from django.urls import path
from like import views

urlpatterns = [
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view())
]
