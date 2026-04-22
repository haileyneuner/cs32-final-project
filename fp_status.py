from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Workout Generator</title>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">

    <style>
        body {
            font-family: Inter;
            background: #000;
            color: #fff;
            display: flex;
            justify-content: center;
            padding: 40px;
        }

        .container {
            width: 420px;
            background: #111;
            padding: 25px;
            border-radius: 14px;
            border: 1px solid #222;
        }

        h1 { text-align: center; }

        label {
            font-size: 12px;
            color: #aaa;
        }

        select, input {
            width: 100%;
            margin: 6px 0 12px 0;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #333;
            background: #000;
            color: white;
        }

        input[type="range"] { width: 100%; }

        .value {
            font-size: 12px;
            color: #00ff88;
            text-align: right;
            margin-bottom: 10px;
        }

        button {
            width: 100%;
            padding: 12px;
            background: #00ff88;
            border: none;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 10px;
        }

        button:hover { opacity: 0.85; }

        .card {
            margin-top: 20px;
            border: 1px solid #222;
            padding: 15px;
            border-radius: 10px;
        }

        li { margin-bottom: 6px; }

        .timer {
            margin-top: 20px;
            border-top: 1px solid #222;
            padding-top: 15px;
            text-align: center;
        }

        .time {
            font-size: 32px;
            color: #00ff88;
            margin: 10px 0;
        }

        .timer-controls {
            display: flex;
            gap: 10px;
        }

        .timer button { flex: 1; }
    </style>
</head>

<body>

<div class="container">

    <h1>Workout</h1>

    <form method="POST">

        <label>Goal</label>
        <select name="goal">
            <option>Lose Weight</option>
            <option>Gain Muscle</option>
        </select>

        <label>Muscle Group</label>
        <select name="group" id="groupSelect" onchange="checkGroup()">
            <option>Upper Body</option>
            <option>Lower Body</option>
            <option>Core</option>
        </select>

        <label>Bench Max</label>
        <input type="number" name="bench" required>

        <label>Squat Max</label>
        <input type="number" name="squat" required>

        <label>Energy</label>
        <input type="range" name="energy" min="1" max="10" value="5"
               oninput="e.innerText=this.value">
        <div class="value">Energy: <span id="e">5</span></div>

        <label>Time (minutes)</label>
        <input type="range" name="time" min="5" max="90" value="30"
               oninput="t.innerText=this.value">
        <div class="value">Time: <span id="t">30</span></div>

        <button type="submit">Generate</button>
    </form>

    {% if workout %}
    <div class="card">
        <h3>Workout</h3>
        <ul>
            {% for item in workout %}
            <li>
                {{ item.name }}
                <span style="color:#00ff88;"> — {{ item.weight }}</span>
            </li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}

    <!-- TIMER -->
    <div class="timer" id="timerBox">
        <h3>Core Timer</h3>
        <div class="time" id="timeDisplay">00:00</div>

        <div class="timer-controls">
            <button type="button" onclick="startTimer()">Start</button>
            <button type="button" onclick="pauseTimer()">Pause</button>
            <button type="button" onclick="resetTimer()">Reset</button>
        </div>
    </div>

</div>

<script>
let timer = null;
let seconds = 0;
let running = false;

function updateDisplay() {
    let m = Math.floor(seconds / 60);
    let s = seconds % 60;
    document.getElementById("timeDisplay").innerText =
        String(m).padStart(2,'0') + ":" + String(s).padStart(2,'0');
}

function startTimer() {
    if (running) return;
    running = true;
    timer = setInterval(() => {
        seconds++;
        updateDisplay();
    }, 1000);
}

function pauseTimer() {
    running = false;
    clearInterval(timer);
}

function resetTimer() {
    pauseTimer();
    seconds = 0;
    updateDisplay();
}

function checkGroup() {
    const group = document.getElementById("groupSelect").value;
    const box = document.getElementById("timerBox");
    box.style.display = (group === "Core") ? "block" : "block";
}

document.addEventListener("DOMContentLoaded", checkGroup);
</script>

</body>
</html>
"""

# ---------- SMART WEIGHT LOGIC ----------

def calc_weight(max_lift, energy, goal):
    if goal == "Gain Muscle":
        pct = 0.80 if energy >= 8 else 0.70 if energy >= 5 else 0.60
    else:
        pct = 0.65 if energy >= 8 else 0.55 if energy >= 5 else 0.45

    weight = round(max_lift * pct / 5) * 5
    return weight


def get_workout(group, energy, time, bench, squat, goal):

    workouts = {
        "Upper Body": ["Push-ups", "Pull-ups", "Shoulder Press", "Tricep Dips",
                       "Bicep Curls", "Bench Press", "Incline Bench Press", "Dumbbell Rows"],
        "Lower Body": ["Bar Squats", "Goblet Squats", "Bulgarian Split Squats",
                       "RDL", "Lunges", "Glute Bridges", "Calf Raises"],
        "Core": ["Planks", "Crunches", "Mountain Climbers", "Dead Bugs", "Bear Crawl"]
    }

    selected = random.sample(workouts[group], 4)

    output = []

    for ex in selected:

        weight = "Bodyweight"

        # Bench-based lifts
        if ex in ["Bench Press", "Incline Bench Press"]:
            weight = f"{calc_weight(bench, energy, goal)} lbs"

        elif ex in ["Shoulder Press", "Tricep Dips", "Bicep Curls", "Dumbbell Rows"]:
            weight = f"{calc_weight(bench * 0.6, energy, goal)} lbs (DB)"

        # Squat-based lifts
        elif ex == "Bar Squats":
            weight = f"{calc_weight(squat, energy, goal)} lbs"

        elif ex in ["Goblet Squats", "RDL", "Lunges"]:
            weight = f"{calc_weight(squat * 0.5, energy, goal)} lbs (DB)"

        output.append({"name": ex, "weight": weight})

    return output


# ---------- FLASK ----------

@app.route("/", methods=["GET", "POST"])
def home():
    workout = None

    if request.method == "POST":
        group = request.form["group"]
        energy = int(request.form["energy"])
        time = int(request.form["time"])
        bench = int(request.form["bench"])
        squat = int(request.form["squat"])
        goal = request.form["goal"]

        workout = get_workout(group, energy, time, bench, squat, goal)

    return render_template_string(HTML, workout=workout)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
