from django.urls import path
from .views import review_history, add_review, dashboard,update_status,test_redir

urlpatterns = [
    path("", test_redir, name="test_redir"),
    path("reviews/history/", review_history, name="review_history"),
    path("reviews/add/", add_review, name="add_review"),
    path("dashboard/", dashboard, name="dashboard"),
    path("reviews/update-status/", update_status, name="update_status"),
]
