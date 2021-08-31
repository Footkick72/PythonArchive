n=raw_input("Pick a number. ")
counter=0

while not n.isdigit() or (n[0]=='0' and len(n)!=1):
    if not n.isdigit():
        n=raw_input("That's not a positive integer! ")
    else:
        n=raw_input("Numbers do not start with 0. ")

n=int(n)

while n!=1:
    if n%2==0:
        n/=2
    else:
        n*=3
        n+=1
    counter+=1

print "It took %i steps to get to 1 using the collatz conjecture" %counter
