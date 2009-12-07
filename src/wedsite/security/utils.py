from django.conf import settings

def encrypt(ip_addr):
    try:
        import hashlib
    except ImportError:
        import sha
        return sha.new(ip_addr + settings.SECRET_KEY).hexdigest()
    else:
        return hashlib.sha1(ip_addr + settings.SECRET_KEY).hexdigest()
    raise ValueError("Cryptographic algorithm not available.")
