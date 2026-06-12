#comments for understanding and presentation

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

    # Rank encoding: lower rank number = stronger team.
    # Use 1/rank so rank 1 → 1.0, rank 20 → 0.05 (clean, no negatives)
    rank1 = max(1, row[12])
    rank2 = max(1, row[13])
    rank1_enc = 1.0 / rank1         # team1 strength: high = good
    rank2_enc = 1.0 / rank2         # team2 strength: high = good
    # Rank differential: high value = team1 is stronger (lower rank number)
    rank_diff = (rank1_enc - rank2_enc + 1.0) / 2.0  # normalised to [0,1]

    return [
        team_map.get(row[1], 5) / 10,
        team_map.get(row[2], 5) / 10,
        team_map.get(row[4], 5) / 10,
        toss,
        match_type / 2,
        rank1_enc,          # x[5]: team1 rank strength (higher = stronger)
        rank2_enc,          # x[6]: team2 rank strength (higher = stronger)
        row[14] / 5,        # x[7]: team1 form
        row[15] / 5,        # x[8]: team2 form
        rank_diff           # x[9]: direct rank advantage for team1
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

# Logistic Regression (with bias term)
def train_logistic(X, y, lr=0.05, epochs=1000):
    w = [0.0] * len(X[0])
    bias = 0.0
    for _ in range(epochs):
        for i in range(len(X)):
            z = sum(w[j] * X[i][j] for j in range(len(w))) + bias
            pred = sigmoid(z)
            error = pred - y[i]
            for j in range(len(w)):
                w[j] -= lr * error * X[i][j]
            bias -= lr * error
    return w, bias

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

# Decision Tree (rank + form aware)
def simple_tree_predict(x):
    # x[5]=team1 rank strength, x[6]=team2 rank strength
    # x[7]=team1 form,          x[8]=team2 form
    # x[9]=rank differential (>0.5 means team1 stronger)
    rank_advantage = x[9] > 0.5          # team1 has better (lower) rank
    form_advantage = x[7] >= x[8]        # team1 has equal or better form
    strong_rank_edge = x[9] > 0.7        # team1 is much stronger by rank

    if strong_rank_edge:
        return 1  # dominant rank advantage overrides form
    if rank_advantage and form_advantage:
        return 1
    return 0

# Rank Expert: pure rank-based vote (weight=3 in ensemble)
# x[9] = rank_diff: >0.5 means team1 has better rank, <0.5 means team2 better
def rank_expert_predict(x):
    return 1 if x[9] > 0.5 else 0

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
def train_perceptron(X, y, lr=0.01, epochs=500):
    w = [0.0] * len(X[0])
    bias = 0.0
    for _ in range(epochs):
        for i in range(len(X)):
            z = sum(w[j] * X[i][j] for j in range(len(w))) + bias
            pred = 1 if z >= 0 else 0
            error = y[i] - pred
            for j in range(len(w)):
                w[j] += lr * error * X[i][j]
            bias += lr * error
    return w, bias

#TRAIN

train_data = load_dataset("train.csv")
train_X, train_y = prepare_classification(train_data)

weights_log, bias_log = train_logistic(train_X, train_y)
weights_perc, bias_perc = train_perceptron(train_X, train_y)


#TESTING

def predict_dataset(X):
    predictions = []

    for x in X:

        z = sum(weights_log[j] * x[j] for j in range(len(x))) + bias_log
        log = 1 if sigmoid(z) >= 0.5 else 0

        knn = knn_predict(train_X, train_y, x)
        tree = simple_tree_predict(x)
        nb = naive_bayes(train_X, train_y, x)
        rank_exp = rank_expert_predict(x)

        z = sum(weights_perc[j] * x[j] for j in range(len(x))) + bias_perc
        perc = 1 if z >= 0 else 0

        # Max score = 2+2+1+1+1+3 = 10; threshold = 5
        score = log*2 + perc*2 + knn + tree + nb + rank_exp*3
        final = 1 if score >= 5 else 0

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

def predict_single(x, z_boost=0):
    z = sum(weights_log[j] * x[j] for j in range(len(x))) + bias_log + z_boost
    log = 1 if sigmoid(z) >= 0.5 else 0
    knn = knn_predict(train_X, train_y, x)
    tree = simple_tree_predict(x)
    nb = naive_bayes(train_X, train_y, x)
    rank_exp = rank_expert_predict(x)
    z_perc = sum(weights_perc[j] * x[j] for j in range(len(x))) + bias_perc + z_boost
    perc = 1 if z_perc >= 0 else 0
    return log, knn, tree, nb, perc, rank_exp

def display(row, results, override_winner=None):
    team1 = row[1]
    team2 = row[2]
    def decode(p):
        return team1 if p == 1 else team2

    log, knn, tree, nb, perc, rank_exp = results

    print("\n--- PREDICTION ---")
    print("Logistic:", decode(log))
    print("KNN:", decode(knn))
    print("Decision Tree:", decode(tree))
    print("Naive Bayes:", decode(nb))
    print("Perceptron:", decode(perc))
    print("Rank Expert:", decode(rank_exp))
    # Max score = 10, threshold = 5
    score = log*2 + perc*2 + knn + tree + nb + rank_exp*3
    
    if override_winner is not None:
        final = override_winner
    else:
        final = 1 if score >= 5 else 0
        
    print("\nFINAL WINNER:", decode(final))
    print("------------------")

#MENU SYSTEM

if __name__ == "__main__":
    while True:
        print("\n1. Test Model on Test Dataset")
        print("2. Predict Manually (Pre-Match)")
        print("3. Predict Live (In-Match)")
        print("4. Exit")
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

        elif choice == "3":
            print("\n--- LIVE MATCH SETUP ---")
            row = get_input()
            x_base = encode_row(row)
            team1 = row[1]
            team2 = row[2]
            
            while True:
                innings_choice = input("\nSelect Innings (1 or 2, 'q' to stop):\n1. 1st Innings (Setting Score)\n2. 2nd Innings (Chasing Score)\nChoice: ")
                if innings_choice.lower() == 'q':
                    break
                if innings_choice not in ['1', '2']:
                    print("Invalid choice.")
                    continue

                batting_choice = input(f"\nWhich team is batting? (1 for {team1}, 2 for {team2}, 'q' to stop): ")
                if batting_choice.lower() == 'q':
                    break
                if batting_choice not in ['1', '2']:
                    print("Invalid choice.")
                    continue
                    
                target_score = None
                if innings_choice == '2':
                    target_input = input("Enter Target Score set in 1st Innings (or 'q' to stop): ")
                    if target_input.lower() == 'q':
                        break
                    try:
                        target_score = int(target_input)
                    except ValueError:
                        print("Invalid target score.")
                        continue
                        
                score_input = input(f"Enter live score for Team {batting_choice} (runs-wickets-overs) or 'q' to stop: ")
                if score_input.lower() == 'q':
                    break
                try:
                    parts = score_input.split('-')
                    runs = int(parts[0])
                    wickets = int(parts[1])
                    overs = float(parts[2]) if len(parts) == 3 else 15.0 # Fallback to 15.0 if overs omitted
                    
                    x_live = list(x_base) # Create a copy 
                    
                    # Simple logic to convert live score into an ML feature boost
                    # We calculate run rate using overs and factor that in
                    run_rate = runs / max(0.1, overs)
                    perf_ratio = (run_rate / max(1, wickets)) / 2.0
                    
                    if batting_choice == '1':
                        x_live[7] = min(1.0, x_live[7] * (0.3 + 0.7 * perf_ratio))
                    else:
                        x_live[8] = min(1.0, x_live[8] * (0.3 + 0.7 * perf_ratio))
                    
                    total_overs = 20 if str(row[11]).upper() == "T20" else 50
                    if wickets >= 10:
                        projected_score = runs
                    else:
                        remaining_overs = max(0, total_overs - overs)
                        remaining_wickets = 10 - wickets
                        
                        # Estimate maximum overs they can survive based on remaining wickets
                        overs_per_wicket = 2.0 if total_overs == 20 else 5.0
                        max_survivable_overs = remaining_wickets * overs_per_wicket
                        effective_remaining_overs = min(remaining_overs, max_survivable_overs)
                        
                        # Scoring capability decays as wickets fall
                        resource_factor = 0.5 + 0.5 * (remaining_wickets / 10.0)
                        
                        projected_score = int(runs + (run_rate * effective_remaining_overs * resource_factor))
                    
                    if innings_choice == '1':
                        par_score = 160 if total_overs == 20 else 260
                        score_diff = projected_score - par_score
                    else:
                        score_diff = projected_score - target_score
                        
                    progress_factor = min(1.0, overs / total_overs)
                    
                    if batting_choice == '1':
                        z_boost = (score_diff * 0.05) * progress_factor
                    else:
                        z_boost = -(score_diff * 0.05) * progress_factor
                    
                    z = sum(weights_log[j]*x_live[j] for j in range(len(x_live))) + z_boost
                    prob = sigmoid(z) * 100
                    
                    print(f"\n--- LIVE ML PREDICTION SCORE ---")
                    if innings_choice == '1':
                        print(f"Projected Score ({total_overs} Overs): {projected_score}")
                    else:
                        print(f"Projected Score ({total_overs} Overs): {projected_score} (Target: {target_score})")
                        if projected_score >= target_score:
                            print(f"Status: Batting team is on track to chase the target.")
                        else:
                            print(f"Status: Batting team is falling short of the target.")

                    print(f"{team1} Win Probability: {prob:.1f}%")
                    print(f"{team2} Win Probability: {100 - prob:.1f}%")
                    
                    results = predict_single(x_live, z_boost)
                    override_winner = None
                    if innings_choice == '2':
                        if projected_score >= target_score:
                            override_winner = 1 if batting_choice == '1' else 0
                        else:
                            override_winner = 0 if batting_choice == '1' else 1
                            
                    display(row, results, override_winner)
                except (ValueError, IndexError):
                    print("Invalid input. Use format: runs-wickets-overs (e.g. 150-3-15.2)")

        elif choice == "4":
            break
        else:
            print("Invalid choice, please try again.")
