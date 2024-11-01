from py_ecc.bn128 import is_on_curve, FQ, G1
from py_ecc.fields import field_properties
field_mod = field_properties["bn128"]["field_modulus"]
from hashlib import sha256
from libnum import has_sqrtmod_prime_power, sqrtmod_prime_power


seed = "PedersonHash"

# generate random number%modulus
def random_field_element(seed):
    field_element=int(sha256(seed.encode('ascii')).hexdigest(),16) % field_mod
    return field_element

# mix with generator
def mix_generator(field_element):
    x = int(sha256(str(G1[0].__add__(field_element)).encode('ascii')).hexdigest(), 16) % field_mod 
    return x




b = 3 # for bn128, y^2 = x^3 + 3
n=10    # no of points to generate

entropy = 0

vector_basis = []
while n!=0:

    x=mix_generator(random_field_element(seed))

    # check if y has square root, if not update x
    while not has_sqrtmod_prime_power((x**3 + b) % field_mod, field_mod, 1):
        x = (x + 1) % field_mod

    y = list(sqrtmod_prime_power((x**3 + b) % field_mod, field_mod, 1))[0]
    point = (FQ(x), FQ(y))

    # check if point is not curve, if not update x
    while not is_on_curve(point,b):
        x=(x+1)%field_mod
        y = list(sqrtmod_prime_power((x**3 + b) % field_mod, field_mod, 1))[0]
        point = (FQ(x), FQ(y))

    vector_basis.append(point)
    n-=1

for item in vector_basis:
    print("Point",item)