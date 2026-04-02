#LOAD DATA

def load_dataset(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    data = []
    for i in range(1, len(lines)):
        row = lines[i].strip().split(",")

        row[0] = int(row[0])
        row[12] = int(row[12])
        row[13] = int(row[13])
        row[14] = int(row[14])
        row[15] = int(row[15])

        data.append(row)
    
    return data

#ENCODING

def encode_row(row):
    team_map = {
        "India":1,"Australia":2,"England":3,
        "Afghanistan":4,"South Africa":5,
        "New Zealand":6,"Oman":7
    }
    toss = 1 if row[5] == "bat" else 0
    match_type = 1 if row[11] == "T20" else 2
    return [
        team_map[row[1]] / 10,
        team_map[row[2]] / 10,
        team_map[row[4]] / 10,
        toss,
        match_type / 2,
        (10 - row[12]) / 10,
        (10 - row[13]) / 10,
        row[14] / 5,
        row[15] / 5
    ]

#DATA PREP

def prepare_classification(data):
    X, y = [], []   
    for row in data:
        X.append(encode_row(row))
        y.append(1 if row[16] == row[1] else 0)
    
    return X, y

#ML MODELS

def sigmoid(x):
    if x > 100:
        return 1
    if x < -100:
        return 0
    return 1/(1+2.71828**(-x))

# Logistic Regression
def train_logistic(X, y, lr=0.001, epochs=200):
    w = [0]*len(X[0])
    for _ in range(epochs):
        for i in range(len(X)):
            z = sum(w[j]*X[i][j] for j in range(len(w)))
            pred = sigmoid(z)
            error = pred - y[i]

            for j in range(len(w)):
                w[j] -= lr * error * X[i][j]    
    return w

# KNN
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

# Decision Tree (rule-based)
def simple_tree_predict(x):
    if x[5] > x[6] and x[7] >= x[8]:
        return 1
    return 0

# Naive Bayes
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

# Perceptron
def train_perceptron(X, y, lr=0.01, epochs=200):
    w = [0]*len(X[0])
    bias = 0
    for _ in range(epochs):
        for i in range(len(X)):
            z = sum(w[j]*X[i][j] for j in range(len(w))) + bias
            pred = 1 if z >= 0 else 0
            error = y[i] - pred
            for j in range(len(w)):
                w[j] += lr * error * X[i][j]
            bias += lr * error
    return w, bias

#TRAIN

train_data = load_dataset("train.csv")
train_X, train_y = prepare_classification(train_data)

weights_log = train_logistic(train_X, train_y)
weights_perc, bias_perc = train_perceptron(train_X, train_y)


#TESTING

def predict_dataset(X):
    predictions = []

    for x in X:

        if x[5] > x[6] and x[7] > x[8]:
            predictions.append(1)
            continue

        z = sum(weights_log[j]*x[j] for j in range(len(x)))
        log = 1 if sigmoid(z) >= 0.5 else 0

        knn = knn_predict(train_X, train_y, x)
        tree = simple_tree_predict(x)
        nb = naive_bayes(train_X, train_y, x)

        z = sum(weights_perc[j]*x[j] for j in range(len(x))) + bias_perc
        perc = 1 if z >= 0 else 0

        score = log*2 + perc*2 + knn + tree + nb
        final = 1 if score >= 4 else 0

        predictions.append(final)

    return predictions

def accuracy(y_true, y_pred):
    correct = 0
    for i in range(len(y_true)):
        if y_true[i] == y_pred[i]:
            correct += 1
    return (correct / len(y_true)) * 100

def show_samples(data, preds, n=5):
    print("\n--- SAMPLE TEST RESULTS ---")    
    for i in range(min(n, len(preds))):
        team1 = data[i][1]
        team2 = data[i][2]
        actual = data[i][16]
        pred = team1 if preds[i] == 1 else team2

        print(f"{team1} vs {team2}")
        print("Predicted:", pred, "| Actual:", actual)
        print()

#INTERACTIVE

def get_input():
    print("\nEnter Match Details:")
    team1 = input("Team 1: ")
    team2 = input("Team 2: ")
    toss_winner = input("Toss Winner: ")
    toss_decision = input("Toss Decision (bat/field): ")
    match_type = input("Match Type (T20/ODI): ")
    team1_rank = int(input("Team1 Ranking: "))
    team2_rank = int(input("Team2 Ranking: "))
    team1_form = int(input("Team1 Form (0-5): "))
    team2_form = int(input("Team2 Form (0-5): "))
    row = [
        0, team1, team2, "Venue", toss_winner, toss_decision,
        0,0,0,0,20,
        match_type,
        team1_rank, team2_rank,
        team1_form, team2_form,
        "unknown"
    ]

    return row

def predict_single(x):
    if x[5] > x[6] and x[7] > x[8]:
        return 1,1,1,1,1
    z = sum(weights_log[j]*x[j] for j in range(len(x)))
    log = 1 if sigmoid(z) >= 0.5 else 0
    knn = knn_predict(train_X, train_y, x)
    tree = simple_tree_predict(x)
    nb = naive_bayes(train_X, train_y, x)
    z = sum(weights_perc[j]*x[j] for j in range(len(x))) + bias_perc
    perc = 1 if z >= 0 else 0
    return log, knn, tree, nb, perc

def display(row, results):
    team1 = row[1]
    team2 = row[2]
    def decode(p):
        return team1 if p == 1 else team2

    log, knn, tree, nb, perc = results

    print("\n--- PREDICTION ---")
    print("Logistic:", decode(log))
    print("KNN:", decode(knn))
    print("Decision Tree:", decode(tree))
    print("Naive Bayes:", decode(nb))
    print("Perceptron:", decode(perc))
    score = log*2 + perc*2 + knn + tree + nb
    final = 1 if score >= 4 else 0
    print("\nFINAL WINNER:", decode(final))
    print("------------------")


#MENU SYSTEM

while True:
    print("\n1. Test Model on Test Dataset")
    print("2. Predict Manually (Pre-Match)")
    print("3. Exit")
    choice = input("Enter choice: ")
    if choice == "1":
        test_data = load_dataset("test.csv")
        test_X, test_y = prepare_classification(test_data)
        preds = predict_dataset(test_X)
        print("\nAccuracy:", accuracy(test_y, preds), "%")
        show_samples(test_data, preds)

    elif choice == "2":
        row = get_input()
        x = encode_row(row)
        results = predict_single(x)
        display(row, results)

    else:
        break
