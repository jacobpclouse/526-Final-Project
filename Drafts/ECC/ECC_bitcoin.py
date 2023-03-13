# Elliptic Curve Cryptography using the BitCoin curve, SECG secp256k1
#  Dr. Orion Lawlor, lawlor@alaska.edu, 2015-02-20 (Public Domain)
# LINK: https://www.cs.uaf.edu/2015/spring/cs463/lecture/02_23_ECC_impl/ECC_bitcoin.py

from math import log
from copy import copy
from time import time # timing
# from fractions import gcd # Greatest Common Denominator -- This was depreciated in Python 3.10.
from math import gcd # Greatest Common Denominator -- where gcd was moved to 
from random import SystemRandom # cryptographic random byte generator
rand=SystemRandom() # create strong random number generator

# Convert a string with hex digits, colons, and whitespace to a long integer
def hex2int(hexString):
	return int("".join(hexString.replace(":","").split()),16)

# Half the extended Euclidean algorithm:
#    Computes   gcd(a,b) = a*x + b*y  
#    Returns only gcd, x (not y)
# From http://rosettacode.org/wiki/Modular_inverse#Python
def half_extended_gcd(aa, bb):
	lastrem, rem = abs(aa), abs(bb)
	x, lastx = 0, 1
	while rem:
		lastrem, (quotient, rem) = rem, divmod(lastrem, rem)
		x, lastx = lastx - quotient*x, x
	return lastrem, lastx 

# Modular inverse: compute the multiplicative inverse i of a mod m:
#     i*a = a*i = 1 mod m
def modular_inverse(a, m):
	g, x = half_extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m


# An elliptic curve has these fields:
#   p: the prime used to mod all coordinates
#   a: linear part of curve: y^2 = x^3 + ax + b
#   b: constant part of curve
#   G: a curve point (G.x,G.y) used as a "generator"
#   n: the order of the generator
class ECcurve:
	def __init__(self):
		return

	# Prime field multiplication: return a*b mod p
	def field_mul(self,a,b):
		return (a*b)%self.p

	# Prime field division: return num/den mod p
	def field_div(self,num,den):
		inverse_den=modular_inverse(den%self.p,self.p)
		return self.field_mul(num%self.p,inverse_den)

	# Prime field exponentiation: raise num to power mod p
	def field_exp(self,num,power):
		return pow(num%self.p,power,self.p)

	# Return the special identity point
	#   We pick x=p, y=0
	def identity(self):
		return ECpoint(self,self.p,0)

	# Return true if point Q lies on our curve
	def touches(self,Q):
		y2=self.field_exp(Q.y,2)
		x3ab=(self.field_mul((Q.x*Q.x)%self.p+self.a,Q.x)+self.b)%self.p
		return y2==x3ab

	# Return the slope of the tangent of this curve at point Q
	def tangent(self,Q):
		return self.field_div(Q.x*Q.x*3+self.a,Q.y*2)

	# Return the (x,y) point where this line intersects our curve
	#  Q1 and Q2 are two points on the line of slope m
	def line_intersect(self,Q1,Q2,m):
		v=(Q1.y + self.p - (m*Q1.x)%self.p)%self.p
		x=(m*m + self.p-Q1.x + self.p-Q2.x)%self.p
		y=(self.p-(m*x)%self.p + self.p-v)%self.p
		return ECpoint(self,x,y)

	# Return a doubled version of this elliptic curve point
	def double(self,Q):
		if (Q.x==self.p): # doubling the identity
			return Q
		return self.line_intersect(Q,Q,self.tangent(Q))

	# Return the "sum" of these elliptic curve points
	def add(self,Q1,Q2):
		# Identity special cases
		if (Q1.x==self.p): # Q1 is identity
			return Q2
		if (Q2.x==self.p): # Q2 is identity
			return Q1

		# Equality special cases
		if (Q1.x==Q2.x): 
			if (Q1.y==Q2.y): # adding point to itself
				return self.double(Q1)
			else: # vertical pair--result is the identity
				return self.identity()

		# Ordinary case
		m=self.field_div(Q1.y+self.p-Q2.y,Q1.x+self.p-Q2.x)
		return self.line_intersect(Q1,Q2,m)

	# "Multiply" this elliptic curve point Q by the integer m
	#    Often the point Q will be the generator G
	def mul(self,Q,m):
		R=self.identity() # return point
		while m!=0:  # binary multiply loop
			if m&1: # bit is set
				# print("  mul: adding Q to R =",R);
				R=self.add(R,Q)
			m=m>>1
			if (m!=0):
				# print("  mul: doubling Q =",Q);
				Q=self.double(Q)
		
		return R

# A point on an elliptic curve: (x,y)
class ECpoint:
	"""A point on an elliptic curve (x,y)"""
	def __init__(self,curve, x,y):
		self.curve=curve
		self.x=x
		self.y=y
		if not x==curve.p and not curve.touches(self):
			print(" ECpoint left curve: ",x,",",y)

	# "Add" this point to another point on the same curve
	def add(self,Q2):
		return self.curve.add(self,Q2)

	# "Multiply" this point by a scalar
	def mul(self,m):
		return self.curve.mul(self,m)

	# Print this ECpoint
	def __str__(self):
		if (self.x==self.curve.p):
			return "identity_point"
		else:
			return "("+str(self.x)+", "+str(self.y)+")"


# This is the BitCoin elliptic curve, SECG secp256k1
#   See http://www.secg.org/SEC2-Ver-1.0.pdf
secp256k1=ECcurve()
secp256k1.p=hex2int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F");
secp256k1.a=0 # it's a Koblitz curve, with no linear part
secp256k1.b=7 
secp256k1.n=hex2int("FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141");

# SEC's "04" means they're representing the generator point's X,Y parts explicitly.
#  The compressed "02" form means storing only x (you compute Y)
secp256k1.G=ECpoint(curve=secp256k1,
  x = hex2int("79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798"),
  y = hex2int("483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8")
);


#################
# Test program:
curve=secp256k1

Q=curve.G
print("Generator touches curve? ",curve.touches(Q));
print("Tangent of generator: ",curve.tangent(Q));

for i in range(2,10):
	Q=Q.add(curve.G) # repeatedly add generator
	print("Curve point ",i,Q);

	J=curve.mul(curve.G,i) # direct jump
	if (J.x!=Q.x or J.y!=Q.y):
		print("    -> MULTIPLY MISMATCH: ",J.x,",",J.y);


start=time()

# Diffie-Hellman key exchange
A_secret=rand.getrandbits(256)%curve.p
A_public=curve.mul(curve.G,A_secret);

B_secret=rand.getrandbits(256)%curve.p
B_public=curve.mul(curve.G,B_secret);

# A and B would exchange public points here

AB_shared=curve.mul(A_public,B_secret); # B computes this
BA_shared=curve.mul(B_public,A_secret); # A computes this

if (AB_shared.x == BA_shared.x):
	print("ECDH key exchange success! ",AB_shared);

print("ECDH elapsed=",time()-start," seconds")

