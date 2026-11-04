from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, FileResponse, Http404
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Document, DocumentPermission

@login_required
def dashboard(request):
    query = request.GET.get('q')
    user = request.user
    
    if hasattr(user, 'userprofile') and user.userprofile.role == 'ADMIN':
        docs = Document.objects.all()
    else:
        docs = Document.objects.filter(
            Q(owner=user) | Q(permissions__user=user)
        ).distinct()
        
    if query:
        docs = docs.filter(Q(title__icontains=query) | Q(category__icontains=query))
        
    return render(request, 'vault/dashboard.html', {'documents': docs})

@login_required
def upload_doc(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        file = request.FILES.get('file')
        
        Document.objects.create(
            owner=request.user,
            title=title,
            category=category,
            file=file
        )
        return redirect('dashboard')
    return render(request, 'vault/upload.html')

@login_required
def secure_download(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    
    is_owner = doc.owner == request.user
    is_admin = hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'
    has_perm = DocumentPermission.objects.filter(document=doc, user=request.user).exists()
    
    if not (is_owner or is_admin or has_perm):
        return HttpResponseForbidden("You do not have permission to access this file.")
        
    return FileResponse(doc.file.open('rb'), as_attachment=True, filename=doc.file.name)

@login_required
def manage_permissions(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    
    is_owner = doc.owner == request.user
    is_admin = hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'
    
    if not (is_owner or is_admin):
        return HttpResponseForbidden("Only owners or admins can manage permissions.")
        
    if request.method == 'POST':
        target_username = request.POST.get('username', '').strip()
        target_user = User.objects.filter(username=target_username).first()
        if target_user:
            DocumentPermission.objects.get_or_create(document=doc, user=target_user)
        return redirect('manage_permissions', doc_id=doc.id)
        
    permissions = DocumentPermission.objects.filter(document=doc)
    return render(request, 'vault/permissions.html', {'document': doc, 'permissions': permissions})

@login_required
def revoke_permission(request, perm_id):
    perm = get_object_or_404(DocumentPermission, id=perm_id)
    doc_id = perm.document.id
    
    is_owner = perm.document.owner == request.user
    is_admin = hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'
    
    if is_owner or is_admin:
        perm.delete()
        
    return redirect('manage_permissions', doc_id=doc_id)
