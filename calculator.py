import math

lamb=3e8/2.4e9
v=0.58

Bs=v/lamb
print("Doppler spread is", Bs)

print("Coherence time", 1/Bs)

H=(0.25*math.log2(1/0.25)+0.5*math.log2(1/0.5)+2*0.125*math.log2(1/0.125))
print("CR rate", H)