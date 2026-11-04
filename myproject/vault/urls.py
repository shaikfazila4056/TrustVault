from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_doc, name='upload_doc'),
    path('download/<int:doc_id>/', views.secure_download, name='secure_download'),
    path('permissions/<int:doc_id>/', views.manage_permissions, name='manage_permissions'),
    path('revoke/<int:perm_id>/', views.revoke_permission, name='revoke_permission'),
]
