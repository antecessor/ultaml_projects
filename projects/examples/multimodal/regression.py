import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.metrics import mean_squared_error, r2_score

from projects.data.multimodal.TabularData import TabularData
from projects.models.multimodal.Regression.LinearRegression import LinearRegression
from projects.models.multimodal.Regression.LinearRegressionConfig import \
    LinearRegressionConfig

# Load the diabetes dataset
data = datasets.load_diabetes(return_X_y=False)
columns = data.feature_names
columns.extend(['diabete'])
df = pd.DataFrame(np.append(data.data, data['target'].reshape(-1, 1), axis=1),
                  columns=columns)

tabData = TabularData().load(df).set_input_target(columns[:-1], columns[-1])
# Split the data into training/testing sets
train_features, test_feature, train_target, test_target = tabData.get_train_test()

# Create linear regression object
linear_reg = LinearRegression(LinearRegressionConfig())

# Train the model using the training sets
linear_reg.fit(train_features, train_target)

# Make predictions using the testing set
diabetes_y_pred = linear_reg.predict(test_feature)

# The coefficients
print("Score: \n", linear_reg.score)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(test_target, diabetes_y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(test_target, diabetes_y_pred))

# Plot outputs
plt.scatter(test_feature[:,0], test_target, color="black")
plt.scatter(test_feature[:,0], diabetes_y_pred, color="blue", linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
