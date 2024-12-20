from django.urls import path
from .views import AgentView  # Import your API view

# Define app-specific URLs
urlpatterns = [
    path('agent/', AgentView.as_view(), name='agent-api'),
]
