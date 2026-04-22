from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Workout Generator</title>

<style>
body {
 font-family: -apple-system, BlinkMacSystemFont, sans-serif;
 background: #f5f7fa;
 margin: 0;
}

.container {
 max-width: 420px;
 margin: auto;
 padding: 20px;
}

.card {
 background: white;
 padding: 20px;
 border-radius: 16px;
 box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

h1, h2, h3 { text-align: center; }

label { font-size: 12px; color: #555; }

select, input {
 width: 100%;
 margin: 6px 0 12px 0;
 padding: 10px;
 border-radius: 8px;
 border: 1px solid #ddd;
}

.main-btn {
 width: 100%;
 padding: 12px;
 border: none;
 border-radius: 10px;
 background: #4CAF50;
 color: white;
 font-size: 16px;
 margin-top: 10px;
}

.exercise {
 background: #eef2f7;
 padding: 12px;
 border-radius: 10px;
 margin-bottom: 10px;
 display: flex;
 justify-content: space-between;
 align-items: center;
}

.icon-btn {
 border: none;
 background: none;
 font-size: 18px;
 cursor: pointer;
}

/* TIMER (EXACT FIRST CODE STYLE) */
.timer-box {
 text-align: center;
 font-size: 32px;
 padding: 20px;
 border-radius: 12px;
 margin: 20px 0;
 color: white;
 background: green;
 transition: background 0.3s;
}

.button-row {
 display: flex;
 gap: 10px;
 margin-top: 10px;
}

.button-row button {
 flex: 1;
 padding: 8px;
 border: 2px solid black;
 border-radius: 8px;
 background: white;
 color: black;
 font-size: 14px;
}

.button-row button:active {
 background: #eee;
}
</style>
</head>

<body>

<div class="container">
<div class="card">

<h2>Workout Generator</h2>

<form method="POST">

<label>Goal</label>
<select name="goal">
  <option>Gain Muscle</option>
  <option>Lose Weight</option>
</select>

<label>Muscle Group</label>
<select name="group">
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
<div>Energy: <span id="e">5</span></div>

<label>Time</label>
<input type="range" name="time" min="5" max="90" value="30"
 oninput="t.innerText=this.value">
<div>Time: <span id="t">30</span></div>

<button class="main-btn" type="submit">Generate</button>
</form>

{% if workout %}

<h3>Workout of the Day</h3>

{% for item in workout %}
<div class="exercise">

  <div>
    <b>{{ item.name }}</b><br>
    <small>{{ item.sets }} x {{ item.reps }} | {{ item.weight }} | Rest {{ item.rest }}s</small>
  </div>

  <!-- EXACT CHECK/X TOGGLE STYLE -->
  <button class="icon-btn" onclick="toggle(this)">✔</button>

</div>
{% endfor %}

<!-- TIMER (EXACT FIRST CODE) -->
<div class="timer-box" id="timerBox">00:30</div>

<div class="button-row">
  <button onclick="startTimer()">Start</button>
  <button onclick="pauseTimer()">Pause</button>
  <button onclick="resetTimer()">Reset</button>
</div>

{% endif %}

</div>
</div>

<script>

/* ---------------- CHECK/X TOGGLE (FIRST STYLE) ---------------- */
function toggle(btn) {
 if (btn.innerText === "✔") {
   btn.innerText = "✖";
   btn.style.color = "red";
 } else {
   btn.innerText = "✔";
   btn.style.color = "green";
 }
}

/* ---------------- TIMER (EXACT FIRST CODE) ---------------- */
let time = 30;
let interval = null;

function updateDisplay() {
 let sec = time % 60;
 let display = "00:" + (sec < 10 ? "0" + sec : sec);

 const box = document.getElementById("timerBox");

 if (box) {
   box.innerText = display;

   if (time > 5) {
     box.style.background = "green";
   } else if (time > 0) {
     box.style.background = "goldenrod";
   } else {
     box.style.background = "red";
   }
 }
}

function startTimer() {
 if (interval) return;

 interval = setInterval(() => {
   if (time > 0) {
     time--;
     updateDisplay();
   }
 }, 1000);
}

function pauseTimer() {
 clearInterval(interval);
 interval = null;
}

function resetTimer() {
 time = 30;
 updateDisplay();
 pauseTimer();
}

updateDisplay();

</script>

</body>
</html>
"""

# ---------------- LOGIC ----------------

def calc_weight(max_lift, energy, goal):
    if goal == "Gain Muscle":
        pct = 0.80 if energy >= 8 else 0.70 if energy >= 5 else 0.60
    else:
        pct = 0.65 if energy >= 8 else 0.55 if energy >= 5 else 0.45

    return round(max_lift * pct / 5) * 5


def get_workout(group, energy, time, bench, squat, goal):

    base = {
        "Upper Body": ["Bench Press", "Incline Bench Press", "Shoulder Press",
                       "Tricep Dips", "Bicep Curls", "Dumbbell Rows"],
        "Lower Body": ["Bar Squats", "Goblet Squats", "RDL", "Lunges"],
        "Core": ["Planks", "Crunches", "Mountain Climbers", "Dead Bugs"]
    }

    exercises = random.sample(base[group], 4)

    output = []

    for ex in exercises:

        weight = "Bodyweight"

        if ex in ["Bench Press", "Incline Bench Press"]:
            weight = f"{calc_weight(bench, energy, goal)} lbs"

        elif ex == "Bar Squats":
            weight = f"{calc_weight(squat, energy, goal)} lbs"

        elif ex in ["Shoulder Press", "Tricep Dips", "Bicep Curls", "Dumbbell Rows"]:
            weight = f"{calc_weight(bench * 0.6, energy, goal)} lbs (DB)"

        elif ex in ["Goblet Squats", "RDL", "Lunges"]:
            weight = f"{calc_weight(squat * 0.5, energy, goal)} lbs (DB)"

        if energy >= 8:
            sets, reps, rest = 4, 10, 60
        elif energy >= 5:
            sets, reps, rest = 3, 12, 45
        else:
            sets, reps, rest = 2, 15, 30

        output.append({
            "name": ex,
            "weight": weight,
            "sets": sets,
            "reps": reps,
            "rest": rest
        })

    return output


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
