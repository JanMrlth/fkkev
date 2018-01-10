import string
import random

# Just alphanumeric characters
chars = string.letters + string.digits

# Alphanumeric + special characters
#chars = string.letters + string.digits + string.punctuation

pwdSize = 20

print ''.join((random.choice(chars)) for x in range(pwdSize))
