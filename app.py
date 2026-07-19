from flask import Flask, render_template, request, jsonify
import project

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    mode = data.get('mode', 'pre-match')
    
    team1 = data.get('team1', 'Team 1')
    team2 = data.get('team2', 'Team 2')
    match_type = data.get('matchType', 'T20')
    toss_winner = data.get('tossWinner', team1)
    toss_decision = data.get('tossDecision', 'bat')
    
    t1_rank = data.get('team1Rank', 1)
    t2_rank = data.get('team2Rank', 2)
    t1_form = data.get('team1Form', 3)
    t2_form = data.get('team2Form', 3)
    
    # Format matches project.py expected row
    row = [
        0, team1, team2, "Venue", toss_winner, toss_decision,
        0, 0, 0, 0, 20,
        match_type,
        t1_rank, t2_rank,
        t1_form, t2_form,
        "unknown"
    ]
    
    x_base = project.encode_row(row)
    
    if mode == 'pre-match':
        # Normal prediction
        results = project.predict_single(x_base)
        log, knn, tree, nb, perc, rank_exp = results
        score = log*2 + perc*2 + knn + tree + nb + rank_exp*3
        final = 1 if score >= 5 else 0
        winner = team1 if final == 1 else team2
        
        return jsonify({
            "winner": winner,
            "score": "--",
            "prob_team1": (score/10.0)*100,
            "prob_team2": 100 - (score/10.0)*100
        })
        
    elif mode == 'live':
        innings = str(data.get('innings', '1'))
        batting_team = str(data.get('battingTeam', '1'))
        live_score = data.get('liveScore', '0-0-0')
        target_score = data.get('targetScore', 0) if innings == '2' else None
        
        try:
            parts = live_score.split('-')
            runs = int(parts[0])
            wickets = int(parts[1])
            overs = float(parts[2]) if len(parts) == 3 else 15.0
            
            x_live = list(x_base)
            run_rate = runs / max(0.1, overs)
            perf_ratio = (run_rate / max(1, wickets)) / 2.0
            
            if batting_team == '1':
                x_live[7] = min(1.0, x_live[7] * (0.3 + 0.7 * perf_ratio))
            else:
                x_live[8] = min(1.0, x_live[8] * (0.3 + 0.7 * perf_ratio))
                
            total_overs = 20 if match_type.upper() == "T20" else 50
            if wickets >= 10:
                projected_score = runs
            else:
                remaining_overs = max(0, total_overs - overs)
                remaining_wickets = 10 - wickets
                overs_per_wicket = 2.0 if total_overs == 20 else 5.0
                max_survivable_overs = remaining_wickets * overs_per_wicket
                effective_remaining_overs = min(remaining_overs, max_survivable_overs)
                resource_factor = 0.5 + 0.5 * (remaining_wickets / 10.0)
                projected_score = int(runs + (run_rate * effective_remaining_overs * resource_factor))
                
            if innings == '1':
                par_score = 160 if total_overs == 20 else 260
                score_diff = projected_score - par_score
            else:
                score_diff = projected_score - target_score
                
            progress_factor = min(1.0, overs / total_overs)
            
            if batting_team == '1':
                z_boost = (score_diff * 0.05) * progress_factor
            else:
                z_boost = -(score_diff * 0.05) * progress_factor
                
            # Probabilities using logistic regression
            z = sum(project.weights_log[j]*x_live[j] for j in range(len(x_live))) + z_boost
            prob_team1 = project.sigmoid(z) * 100
            prob_team2 = 100 - prob_team1
            
            # Predict single
            results = project.predict_single(x_live, z_boost)
            log, knn, tree, nb, perc, rank_exp = results
            score_ensemble = log*2 + perc*2 + knn + tree + nb + rank_exp*3
            
            if innings == '2':
                if projected_score >= target_score:
                    override_winner = 1 if batting_team == '1' else 0
                else:
                    override_winner = 0 if batting_team == '1' else 1
            else:
                override_winner = 1 if prob_team1 >= 50 else 0
            
            final = override_winner
                
            winner = team1 if final == 1 else team2
            
            score_text = f"Projected {projected_score}" + (f" (Target: {target_score})" if innings == '2' else "")
            
            return jsonify({
                "winner": winner,
                "score": score_text,
                "prob_team1": prob_team1,
                "prob_team2": prob_team2
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
