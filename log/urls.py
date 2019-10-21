from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from . import views

urlpatterns = [
    path('job/<int:pk>', login_required(views.LogDetail.as_view()), name='job_detail'),
    path('create', login_required(views.LogCreate.as_view()), name='job_create'),
    path('update/<int:pk>', login_required(views.LogUpdate.as_view()), name='job_update'),
    path('delete/<int:pk>', login_required(views.LogDelete.as_view()), name='job_delete'),
    path('', login_required(views.search), name='search'),
    path('chart', login_required(views.LogChart), name='job_chart'),
    ]