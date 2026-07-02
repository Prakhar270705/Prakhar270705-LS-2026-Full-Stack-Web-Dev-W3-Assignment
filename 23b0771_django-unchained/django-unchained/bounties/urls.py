from django.urls import path

from .views import BountyListCreateView, BountyDetailView

urlpatterns = [
    path('bounties/', BountyListCreateView.as_view(), name='bounty-list-create'),
    path('bounties/<int:pk>/', BountyDetailView.as_view(), name='bounty-detail'),
]
