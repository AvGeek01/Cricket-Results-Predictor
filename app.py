INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cricket Match Predictor</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
:root {
    --primary: #2b7bc4;
    --primary-hover: #1e5a91;
    --bg-dark: #121820;
    --card-bg: rgba(25, 32, 43, 0.95);
    --border-color: rgba(255, 255, 255, 0.15);
    --text-main: #ffffff;
    --text-muted: #b0b8c5;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
}

body {
    background-color: var(--bg-dark);
    background-image: url('/static/bgcricket.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: var(--text-main);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 40px 20px;
    position: relative;
}

.overlay {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(18, 24, 32, 0.7);
    z-index: 0;
}

.container {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 35px;
    width: 100%;
    max-width: 600px;
    position: relative;
    z-index: 1;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.header {
    text-align: center;
    margin-bottom: 25px;
}

.header h1 {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 5px;
    color: #ffffff;
}

.header p {
    color: var(--primary);
    font-size: 14px;
    font-weight: 500;
}

.mode-toggle {
    display: flex;
    background: rgba(0,0,0,0.3);
    border-radius: 6px;
    padding: 4px;
    margin-bottom: 25px;
    border: 1px solid var(--border-color);
}

.toggle-btn {
    flex: 1;
    background: transparent;
    color: var(--text-muted);
    border: none;
    padding: 10px;
    margin: 0;
    border-radius: 4px;
    font-weight: 600;
    transition: background 0.2s ease;
    cursor: pointer;
}

.toggle-btn.active {
    background: var(--primary);
    color: white;
}

.toggle-btn:hover:not(.active) {
    background: rgba(255,255,255,0.05);
    color: white;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-bottom: 15px;
}

.form-group {
    margin-bottom: 0;
}

.full-width {
    grid-column: 1 / -1;
}

.section-title {
    margin-top: 10px;
    border-top: 1px solid var(--border-color);
    padding-top: 20px;
}

.section-title h3 {
    font-size: 15px;
    color: var(--primary);
    font-weight: 600;
}

.form-group label {
    display: block;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-muted);
    margin-bottom: 6px;
}

input, select {
    width: 100%;
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid var(--border-color);
    color: white;
    padding: 10px 12px;
    border-radius: 6px;
    font-size: 14px;
    outline: none;
}

input::placeholder {
    color: rgba(255, 255, 255, 0.3);
}

input:focus, select:focus {
    border-color: var(--primary);
}

select {
    appearance: none;
    -webkit-appearance: none;
    cursor: pointer;
}

.select-wrapper {
    position: relative;
}

.select-wrapper::after {
    content: "▼";
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 10px;
    color: var(--text-muted);
    pointer-events: none;
}

#predictBtn {
    width: 100%;
    background: var(--primary);
    color: #ffffff;
    border: none;
    padding: 14px;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

#predictBtn:hover {
    background: var(--primary-hover);
}

#predictBtn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.spinner {
    display: none;
    width: 18px;
    height: 18px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: #ffffff;
    animation: spin 1s linear infinite;
    margin-left: 10px;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.result-box {
    margin-top: 25px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    text-align: center;
}

.hidden {
    display: none !important;
}

.visible {
    display: block;
}

.winner-label {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 5px;
}

#winnerName {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 10px;
    color: var(--primary);
}

.score-box p {
    font-size: 14px;
    color: var(--text-muted);
}

.score-box strong {
    color: white;
    font-size: 16px;
}

.prob-text {
    margin-top: 15px;
    font-size: 14px;
    color: var(--text-muted);
}

.prob-text strong {
    color: var(--primary);
    font-size: 15px;
}
</style>
</head>
<body>
    <div class="overlay"></div>
    <div class="container">
        <div class="header">
            <h1>Cricket Score & Win Predictor</h1>
            <p>AI-powered Match Analysis</p>
        </div>

        <div class="mode-toggle">
            <button id="btn-pre-match" class="toggle-btn active" onclick="setMode('pre-match')">Pre-Match</button>
            <button id="btn-live" class="toggle-btn" onclick="setMode('live')">Live Prediction</button>
        </div>

        <div class="form-grid">
            <div class="form-group full-width">
                <label for="matchType">Match Type</label>
                <div class="select-wrapper">
                    <select id="matchType">
                        <option value="T20">T20 (20 overs)</option>
                        <option value="ODI">One Day (50 Overs)</option>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label for="team1">Team 1</label>
                <input type="text" id="team1" placeholder="e.g. India" autocomplete="off" oninput="updateTeamOptions()">
            </div>

            <div class="form-group">
                <label for="team2">Team 2</label>
                <input type="text" id="team2" placeholder="e.g. Australia" autocomplete="off" oninput="updateTeamOptions()">
            </div>

            <div class="form-group">
                <label for="team1Rank">Team 1 Ranking</label>
                <input type="number" id="team1Rank" placeholder="e.g. 1" min="1">
            </div>

            <div class="form-group">
                <label for="team2Rank">Team 2 Ranking</label>
                <input type="number" id="team2Rank" placeholder="e.g. 2" min="1">
            </div>

            <div class="form-group">
                <label for="team1Form">Team 1 Form (0-5)</label>
                <input type="number" id="team1Form" placeholder="e.g. 4" min="0" max="5">
            </div>

            <div class="form-group">
                <label for="team2Form">Team 2 Form (0-5)</label>
                <input type="number" id="team2Form" placeholder="e.g. 3" min="0" max="5">
            </div>

            <div class="form-group">
                <label for="tossWinner">Toss Winner</label>
                <div class="select-wrapper">
                    <select id="tossWinner">
                        <option value="" disabled selected>Select Team</option>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label for="tossDecision">Toss Decision</label>
                <div class="select-wrapper">
                    <select id="tossDecision">
                        <option value="bat">Bat</option>
                        <option value="field">Field</option>
                    </select>
                </div>
            </div>
        </div>

        <div id="live-section" class="form-grid hidden">
            <div class="form-group full-width section-title">
                <h3>Live Match Data</h3>
            </div>

            <div class="form-group">
                <label for="innings">Innings</label>
                <div class="select-wrapper">
                    <select id="innings" onchange="toggleTargetScore()">
                        <option value="1">1st Innings</option>
                        <option value="2">2nd Innings</option>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label for="battingTeam">Batting Team</label>
                <div class="select-wrapper">
                    <select id="battingTeam">
                        <option value="" disabled selected>Select Team</option>
                    </select>
                </div>
            </div>

            <div class="form-group" id="targetScoreGroup" style="display: none;">
                <label for="targetScore">Target Score</label>
                <input type="number" id="targetScore" placeholder="e.g. 185">
            </div>

            <div class="form-group full-width">
                <label for="liveScore">Live Score (Runs-Wickets-Overs)</label>
                <input type="text" id="liveScore" placeholder="e.g. 150-3-15.2">
            </div>
        </div>

        <button onclick="predict()" id="predictBtn">
            <span>Predict Outcome</span>
            <div class="spinner" id="spinner"></div>
        </button>

        <div id="result" class="result-box hidden">
            <div class="result-content">
                <p class="winner-label" id="resultLabel">Predicted Winner</p>
                <h2 id="winnerName">--</h2>
                <div class="score-box" id="scoreBox">
                    <p>Estimated Score: <strong id="predictedScore">--</strong></p>
                </div>
                <div class="prob-text hidden" id="probText">
                    <p><span id="probT1Name">Team 1</span>: <strong id="probT1Val">50%</strong> &nbsp;|&nbsp; <span id="probT2Name">Team 2</span>: <strong id="probT2Val">50%</strong></p>
                </div>
            </div>
        </div>
    </div>

    <script>
let currentMode = 'pre-match';

function setMode(mode) {
    currentMode = mode;
    document.getElementById('btn-pre-match').classList.remove('active');
    document.getElementById('btn-live').classList.remove('active');
    document.getElementById('btn-' + mode).classList.add('active');

    const liveSection = document.getElementById('live-section');
    if(mode === 'live') {
        liveSection.classList.remove('hidden');
    } else {
        liveSection.classList.add('hidden');
    }
}

function updateTeamOptions() {
    const team1 = document.getElementById('team1').value.trim();
    const team2 = document.getElementById('team2').value.trim();
    
    const tossWinner = document.getElementById('tossWinner');
    const battingTeam = document.getElementById('battingTeam');

    const t1Val = team1 || "Team 1";
    const t2Val = team2 || "Team 2";

    tossWinner.innerHTML = `
        <option value="" disabled selected>Select Team</option>
        <option value="${team1}">${t1Val}</option>
        <option value="${team2}">${t2Val}</option>
    `;
    
    battingTeam.innerHTML = `
        <option value="" disabled selected>Select Team</option>
        <option value="1">${t1Val}</option>
        <option value="2">${t2Val}</option>
    `;
}

function toggleTargetScore() {
    const innings = document.getElementById('innings').value;
    const targetGroup = document.getElementById('targetScoreGroup');
    if(innings === '2') {
        targetGroup.style.display = 'block';
    } else {
        targetGroup.style.display = 'none';
    }
}

async function predict() {
    const payload = { mode: currentMode };

    // Base inputs
    payload.team1 = document.getElementById("team1").value.trim();
    payload.team2 = document.getElementById("team2").value.trim();
    payload.matchType = document.getElementById("matchType").value;
    payload.tossWinner = document.getElementById("tossWinner").value;
    payload.tossDecision = document.getElementById("tossDecision").value;
    payload.team1Rank = parseInt(document.getElementById("team1Rank").value) || 1;
    payload.team2Rank = parseInt(document.getElementById("team2Rank").value) || 1;
    payload.team1Form = parseInt(document.getElementById("team1Form").value) || 0;
    payload.team2Form = parseInt(document.getElementById("team2Form").value) || 0;

    if(!payload.team1 || !payload.team2 || !payload.tossWinner) {
        alert("Please enter Team 1, Team 2, and Toss Winner.");
        return;
    }

    if(currentMode === 'live') {
        payload.innings = document.getElementById("innings").value;
        payload.battingTeam = document.getElementById("battingTeam").value;
        payload.liveScore = document.getElementById("liveScore").value.trim();

        if(!payload.battingTeam || !payload.liveScore) {
            alert("Please enter the Batting Team and Live Score.");
            return;
        }

        if(payload.innings === '2') {
            payload.targetScore = parseInt(document.getElementById("targetScore").value);
            if(!payload.targetScore) {
                alert("Please enter Target Score for 2nd Innings.");
                return;
            }
        }
    }

    const btn = document.getElementById("predictBtn");
    const spinner = document.getElementById("spinner");
    const btnText = btn.querySelector("span");
    const resultBox = document.getElementById("result");

    btn.disabled = true;
    btnText.textContent = "Analyzing...";
    spinner.style.display = "block";
    resultBox.classList.remove("visible");
    resultBox.classList.add("hidden");

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();

        setTimeout(() => {
            document.getElementById("winnerName").textContent = data.winner;
            
            if(data.score) {
                document.getElementById("predictedScore").textContent = data.score;
                document.getElementById("scoreBox").classList.remove("hidden");
            } else {
                document.getElementById("scoreBox").classList.add("hidden");
            }

            if(data.prob_team1 !== undefined && data.prob_team2 !== undefined) {
                document.getElementById("probText").classList.remove("hidden");
                document.getElementById("probT1Name").textContent = payload.team1;
                document.getElementById("probT1Val").textContent = `${data.prob_team1.toFixed(1)}%`;
                document.getElementById("probT2Name").textContent = payload.team2;
                document.getElementById("probT2Val").textContent = `${data.prob_team2.toFixed(1)}%`;
            } else {
                document.getElementById("probText").classList.add("hidden");
            }

            resultBox.classList.remove("hidden");
            resultBox.classList.add("visible");

            btn.disabled = false;
            btnText.textContent = "Predict Outcome";
            spinner.style.display = "none";
        }, 600);

    } catch (error) {
        console.error("Error predicting:", error);
        alert("There was an error making the prediction.");
        btn.disabled = false;
        btnText.textContent = "Predict Outcome";
        spinner.style.display = "none";
    }
}
</script>
</body>
</html>"""
