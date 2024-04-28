import random

def generate_otp(length=6):
    """
    Generate a random OTP of the specified length.
    """
    return ''.join(random.choices('0123456789', k=6))
