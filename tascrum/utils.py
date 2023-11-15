import random
import string

def generate_invitation_link():
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(10))
    return f"https://example.com/invitation/{random_string}"