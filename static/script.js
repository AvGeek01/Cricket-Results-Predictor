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
