# TrustVault Threat Model & Security Considerations

## Identified Security Threats

### 1. Insecure Direct Object References (IDOR)
* **Risk:** Users attempting to access or modify document IDs directly in the URL without permissions.
* **Mitigation:** Views explicitly verify document ownership or active granted permissions before granting access.

### 2. Unauthorized Direct File Access
* **Risk:** Unauthenticated users downloading sensitive media files via direct storage URLs.
* **Mitigation:** Files are served securely using custom view wrappers (secure_download) rather than raw static links.

### 3. Role Escalation & Audit Tampering
* **Risk:** Users attempting elevated access or modifying authorization logs.
* **Mitigation:** Access logs and role permissions are strictly enforced on the server side with Django ORM models.
