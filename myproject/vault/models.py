from django.db import models
from django.contrib.auth.models import User

# User role choices (Requirement #1)
ROLE_CHOICES = (
    ('ADMIN', 'Administrator'),
    ('OWNER', 'Document Owner'),
    ('VIEWER', 'Viewer'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='VIEWER')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, default='General')
    file = models.FileField(upload_to='secure_vault/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_documents')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DocumentPermission(models.Model):
    PERMISSION_CHOICES = (
        ('READ', 'Read Only'),
        ('EDIT', 'Read and Edit'),
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_type = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='READ')

    class Meta:
        unique_together = ('document', 'user')

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('UPLOAD', 'Upload Document'),
        ('READ', 'Read/Download Document'),
        ('EDIT', 'Edit Document'),
        ('DELETE', 'Delete Document'),
        ('GRANT_ACCESS', 'Granted Access'),
        ('REVOKE_ACCESS', 'Revoked Access'),
        ('DENIED_ACCESS', 'Denied Access Attempt'),
    )
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} | {self.actor} | {self.action}"
