from sklearn.linear_model import LinearRegression

# Sample independent variable data
X = [[1], [2], [3], [4], [5]]

# Sample dependent variable data
y = [2, 4, 6, 8, 10]

def lin_reg(X, y):

    # Create a linear regression model
    model = LinearRegression()

    # Fit the model to the data
    model.fit(X, y)

    # Get the regression coefficients
    intercept = model.intercept_
    coefficients = model.coef_

    # Print the coefficients
    print("Intercept:", intercept)
    print("Coefficient(s):", coefficients)

    return intercept, coefficients

# Predicting independent variable values
def reverse_linear_regression(intercept, coefficients, dependent_variables):
    independent_variables = [(y - intercept) / coef for y, coef in zip(dependent_variables, coefficients)]
    return independent_variables


print(lin_reg(X, y))

# Given intercept and coefficients
intercept = 1.5
coefficients = [2.0, -0.5]

# Sample dependent variable data
y = [3.0, 2.0, 1.0, 0.0, -1.0]

# Predict the independent variable values
x_predicted = reverse_linear_regression(intercept, coefficients, y)
# Print the predicted independent variable values
print("Predicted Independent Variables:", x_predicted)
