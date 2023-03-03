# importing the required module
import matplotlib.pyplot as plt

# x axis values
x = ['WTQ', '2bit-UQ', '4bit-UQ', '8bit-UQ']
# corresponding y axis values
y = [41*100/128, 94*100/256, 212*100/512, 450*100/1024]
#y = [128, 256, 512, 1024]
# plotting the points
plt.plot(x, y)

# naming the x axis
plt.xlabel('Quantization Category')
# naming the y axis
plt.ylabel('Key Difference Rate as % of Generated Bits')

# giving a title to my graph
#plt.title('My first graph!')

# function to show the plot
plt.show()