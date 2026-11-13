
def rev_first(var2):
	var1 = [-16, 13, -18, -20, 15, -3, 6, -1, -15, 11, -11, -17, -15, -16, 3, -3, 4, -11, 19, 20, -10, 11, 9, 2, -12, -14, -3, 0, 0, 13, 12, -12, -18, 18, 6, -6, 4, 5, 3, -6, -15, -3, -5, -3, 10, 0]
	var0 = ''

	for i in range(0, len(var2)):
		var0 += chr(ord(var2[i]) - var1[i])

	return var0 

def rev_second(a):
	n = len(a)
	return a[n-2:] + a[16:n-2] +a[:16]

def rev_third(a):
	var = ''

	for i in range(len(a)):
		if i % 3 == 0:
			var += chr(ord(a[i]) - i//3)
		elif i % 3 == 2:
			var += chr(ord(a[i]) - (i-2)//3)
		else:
			var += chr(ord(a[i]))

	return var

def rev_fourth(a):
	n = len(a)
	return a[n-19:] + a[:n-19]

dec = '''?PsaC~F^oKk/qcBzeWKw(<lg-'9b9EB1UGq9iro+vHFYq_'''

print(rev_fourth(rev_third(rev_second(rev_first(dec)))))
