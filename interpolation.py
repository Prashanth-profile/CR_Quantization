from sklearn.linear_model import LinearRegression

# Example lists (List A and List B)
list_a = [1, 3, 5, 7]
list_b = [2, 4, 6, 8]

# Reshape the lists for regression (required by scikit-learn)
X = [[x] for x in list_a]
y = list_b

# Fit a linear regression model
regressor = LinearRegression()
regressor.fit(X, y)
print(regressor)

# Predict new values for List B based on List A
predicted_values = regressor.predict(X)
print(predicted_values)

# Create two lists with the predicted values
result_list_a = list_a.copy()
result_list_b = predicted_values.copy()

print("Result List A:", result_list_a)
print("Result List B:", result_list_b)
