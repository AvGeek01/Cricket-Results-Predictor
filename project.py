#DATA FUNCTIONS

def load_dataset(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    
    data = []
    
    for i in range(1, len(lines)):
        row = lines[i].strip().split(",")
        
        row[0] = int(row[0])
        row[6] = int(row[6])
        row[7] = int(row[7])
        row[8] = int(row[8])
        row[9] = int(row[9])
        row[10] = int(row[10])
        row[12] = int(row[12])
        row[13] = int(row[13])
        row[14] = int(row[14])
        row[15] = int(row[15])
        
        data.append(row)
    
    return data


def encode_row(row):
    team_map = {
        "India":1,"Australia":2,"England":3,
        "Afghanistan":4,"South Africa":5,
        "New Zealand":6,"Oman":7
    }
    
    toss = 1 if row[5] == "bat" else 0
    match_type = 1 if row[11] == "T20" else 2
    
    return [
        team_map[row[1]], team_map[row[2]], team_map[row[4]],
        toss, row[6], row[7], row[8], row[9],
        row[10], match_type,
        row[12], row[13], row[14], row[15]
    ]


def prepare_classification(data):
    X, y = [], []
    
    for row in data:
        X.append(encode_row(row))
        y.append(1 if row[16] == row[1] else 0)
    
    return X, y


def prepare_regression(data):
    X, y = [], []
    
    for row in data:
        X.append(encode_row(row))
        y.append(row[6])
    
    return X, y


#ML FUNCTIONS

def sigmoid(x):
    if x > 100:
        return 1.0
    elif x < -100:
        return 0.0
    return 1/(1+2.71828**(-x))

def train_linear(X, y, lr=0.000001, epochs=50):
    w = [0]*len(X[0])    
    for _ in range(epochs):
        for i in range(len(X)):
            pred = sum(w[j]*X[i][j] for j in range(len(w)))
            error = pred - y[i]
            
            for j in range(len(w)):
                w[j] -= lr * error * X[i][j]
    
    return w

def train_logistic(X, y, lr=0.001, epochs=50):
    w = [0]*len(X[0])    
    for _ in range(epochs):
        for i in range(len(X)):
            z = sum(w[j]*X[i][j] for j in range(len(w)))
            pred = sigmoid(z)
            error = pred - y[i]
            
            for j in range(len(w)):
                w[j] -= lr * error * X[i][j]
    
    return w

def distance(a,b):
    return sum((a[i]-b[i])**2 for i in range(len(a)))**0.5

def knn_predict(train_X, train_y, test_x, k=3):
    dists = []    
    for i in range(len(train_X)):
        d = distance(train_X[i], test_x)
        dists.append((d, train_y[i]))
    
    dists.sort()
    
    votes = {}
    for i in range(k):
        label = dists[i][1]
        votes[label] = votes.get(label,0)+1
    
    return max(votes, key=votes.get)

def naive_bayes(train_X, train_y, test_x):
    class_data = {}    
    for i in range(len(train_y)):
        label = train_y[i]
        if label not in class_data:
            class_data[label] = []
        class_data[label].append(train_X[i])
    
    best_class = None
    best_prob = -1
    
    for label in class_data:
        prob = 1
        
        for i in range(len(test_x)):
            mean = sum(row[i] for row in class_data[label]) / len(class_data[label])
            prob *= 1/(1+abs(test_x[i]-mean))
        
        if prob > best_prob:
            best_prob = prob
            best_class = label
    
    return best_class

#EVALUATION

def accuracy(y_true, y_pred):
    correct = 0
    
    for i in range(len(y_true)):
        if y_true[i] == y_pred[i]:
            correct += 1
    
    return (correct / len(y_true)) * 100


def mean_absolute_error(y_true, y_pred):
    error = 0
    
    for i in range(len(y_true)):
        error += abs(y_true[i] - y_pred[i])
    
    return error / len(y_true)

train_data = load_dataset("train.csv")
test_data = load_dataset("test.csv")

train_X_cls, train_y_cls = prepare_classification(train_data)
test_X_cls, test_y_cls = prepare_classification(test_data)

train_X_reg, train_y_reg = prepare_regression(train_data)
test_X_reg, test_y_reg = prepare_regression(test_data)

# Linear Regression (score)
weights_lr = train_linear(train_X_reg, train_y_reg)

# Logistic Regression (winner)
weights_log = train_logistic(train_X_cls, train_y_cls)

def predict_linear(X, w):
    preds = []
    for x in X:
        pred = sum(w[j]*x[j] for j in range(len(w)))
        preds.append(pred)
    return preds

score_predictions = predict_linear(test_X_reg, weights_lr)

def predict_logistic(X, w):
    preds = []
    for x in X:
        z = sum(w[j]*x[j] for j in range(len(w)))
        prob = sigmoid(z)
        preds.append(1 if prob >= 0.5 else 0)
    return preds

winner_logistic = predict_logistic(test_X_cls, weights_log)
winner_knn = []
for x in test_X_cls:
    pred = knn_predict(train_X_cls, train_y_cls, x, k=3)
    winner_knn.append(pred)

def simple_tree_predict(x):
    # Better logic using ranking + form
    
    if x[10] < x[11]:   # better ranking
        if x[12] >= x[13]:
            return 1
    return 0

winner_tree = [simple_tree_predict(x) for x in test_X_cls]

winner_nb = []

for x in test_X_cls:
    pred = naive_bayes(train_X_cls, train_y_cls, x)
    winner_nb.append(pred)

def print_predictions():
    for i in range(len(test_X_cls)):
        print("Match", i+1)
        print("Actual Winner:", test_y_cls[i])
        print("Predicted Winners:")
        print(" Logistic:", winner_logistic[i])
        print(" KNN:", winner_knn[i])
        print(" Decision Tree:", winner_tree[i])
        print(" Naive Bayes:", winner_nb[i])
        print("Predicted Score (Team1):", int(score_predictions[i]))
        print("----------------------")

print_predictions()
print("Logistic Accuracy:", accuracy(test_y_cls, winner_logistic))
print("KNN Accuracy:", accuracy(test_y_cls, winner_knn))
print("Decision Tree Accuracy:", accuracy(test_y_cls, winner_tree))
print("Naive Bayes Accuracy:", accuracy(test_y_cls, winner_nb))
print("Score MAE:", mean_absolute_error(test_y_reg, score_predictions))