import uuid
import string
import secrets

def generate_random_password(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_random_unique_id():
    return uuid.uuid4().hex