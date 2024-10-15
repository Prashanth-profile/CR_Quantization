import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 50, })
import math

#p_e=0.1
# Define the x values
p_e = np.linspace(0, 0.5, 100)  # 100 points between -10 and 10
#H=np.linspace(0, 1, 100)
H=1
print(p_e)
rho=[1, 2, 4]

# Define the function for y in terms of x
for rho_element in rho:
    y = H*(1-(2*p_e) ** rho_element)  # You can change this to any function of x
    #print("y", y)

    # Plotting the graph
    if rho_element==1:
        plt.plot(p_e, y, color='cyan', label=f'$y = (1-(2p_e))$')
    elif rho_element==2:
        plt.plot(p_e, y, color='red', label=f'$y = (1-(2p_e)^{rho_element})$')
    if rho_element==4:
        plt.plot(p_e, y, color='blue', label=f'$y = (1-(2p_e)^{rho_element})$')

z=[]
p_eplushalf=p_e+0.5
for element in p_eplushalf:
    #print(element)
    if element==1:
        z.append(0)
        #z.append(H*(-(element*math.log2(element))-((1-element)*math.log2(1-element))))
    #if element==1:
    else:
        z.append(H * (-(element * math.log2(element)) - ((1 - element) * math.log2(1 - element))))
        #z.append(0)
    #else:
        #print(-element*math.log2(element)-((1-element)*math.log2(1-element)))
        #z.append(element*(-(p_eplushalf*math.log2(p_eplushalf))-((1-p_eplushalf)*math.log2(1-p_eplushalf))))  # You can change this to any function of x
#print("y", y)

str=r"$y = -((p_e +0.5) log(p_e +0.5) \\+(1−(p_e +0.5)) log(1−(p_e +0.5)))$"
#print(str)

# Plotting the graph
plt.plot(p_e, z, color='black', label=str)
         #label=r"$y = −H(K)((p_e +0.5) log(p_e +0.5)"+f'\n'+r"+(1−(p_e +0.5)) log(1−(p_e +0.5)))$")

# Adding labels and title
plt.xlabel('p_e')
plt.ylabel('Normalised CR rate')
#plt.title('Plot of y = x^2')

# Show a legend
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
