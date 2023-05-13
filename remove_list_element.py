l=[0, 0, 0, 1, 1, 1, 0, 0, 1]

m=[l[x] for x in range(3,len(l)) if x%3!=0]

print(m)