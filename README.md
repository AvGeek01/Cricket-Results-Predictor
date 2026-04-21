# Cricket-Results-Predictor
This project focuses on developing a Machine Learning system capable of predicting cricket match outcomes and scores based on historical match data and key influencing factors. The system takes into account various parameters such as team performance, rankings, toss decisions, match format, and recent form to generate accurate predictions.

The primary objective of this project is twofold:

To predict the total score of a team in a match (regression task)
To predict the winning team (classification task)

A structured dataset of cricket matches is used, containing features like team names, venue, toss winner, match type, player performance indicators, and historical trends. These features are preprocessed and converted into numerical form to make them suitable for machine learning models.

The system implements multiple machine learning algorithms developed from scratch, including:

Linear Regression (for score prediction)
Logistic Regression (for winner prediction)
K-Nearest Neighbors (KNN)
Decision Tree
Naive Bayes
Perceptron

Each algorithm independently analyzes the input data and produces predictions. A final decision is made based on the consensus or best-performing model. The system also computes win probabilities, providing a more detailed analytical insight rather than just a binary prediction.

The dataset is divided into training and testing sets using a 5-part split approach, ensuring robust evaluation and minimizing overfitting. Model performance is assessed using accuracy metrics for classification and error-based metrics for regression.
