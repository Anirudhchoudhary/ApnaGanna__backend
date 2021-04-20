import string
import random
num = 13
def randomString():
    return str( ''.join(random.choices(string.ascii_uppercase + string.digits, k = num)))