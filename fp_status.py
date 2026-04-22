from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Workout App</title>

<style>
body {
 font-family: -apple-system, BlinkMacSystemFont, sans-serif;
 background: #f5f7fa;
 margin: 0;
}

.container {
 max-width: 400px;
 margin: auto;
 padding: 20px;
}

.card {
 background: white;
 padding: 20px;
 border-radius: 16px;
 box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

h2, h3 { text-align: center; }

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
}

.timer-box {
 text-align: center;
 font-size: 32px;
 padding: 20px;
 border-radius: 12px;
 margin: 20px 0;
 color: white;
 background: green;
}
</style>
</head>

<body>
<div class="container">
<div class="card">

<h2>Workout Generator</h2>

<form method="post">
  <label>Muscle Group</label>
  <select name="group">
    <option>Upper Body</option>
    <option>Lower Body</option>
    <option>Core</option>
  </select><br><br>

  <label>Energy: <span id="energyValue">5</span></label>
  <input type="range" name="energy" min="1" max="10" value="5"
         oninput="energyValue.innerText = this.value"><br><br>

  <label>Time (minutes)</label>
  <input type="number" name="time" required><br><br>

  <label>Max Bench (lbs)</label>
  <input type="number" name="bench" required><br><br>

  <label>Max Squat (lbs)</label>
  <input type="number" name="squat" required><br><br>

  <button class="main-btn" type="submit">Generate</button>
</form>

{% if workout %}

<div class="timer-box">00:30</div>

<h3>Workout of the Day</h3>

{% for ex, weight in workout %}
  <div class="exercise">
    {{ ex }}<br>
    <small>{{ weight }} | {{ sets }} x {{ duration }}</small>
  </div>
{% endfor %}

{% endif %}

</div>
</div>
</body>
</html>
"""

def calc_load(max_lift, energy, percent_low, percent_mid, percent_high):
    if energy >= 8:
        pct = percent_high
    elif energy >= 5:
        pct = percent_mid
    else:
        pct = percent_low
    return round(max_lift * pct / 100, -5)  # rounds to nearest 5 lbs


def get_workout(group, energy, time, bench, squat):

    workouts = {
        "Upper Body": ["Push-ups", "Pull-ups", "Shoulder Press", "Tricep Dips",
                       "Bicep Curls", "Bench Press", "Incline Bench Press", "Dumbbell Rows"],
        "Lower Body": ["Bar Squats", "Goblet Squats", "Bulgarian Split Squats",
                       "RDL", "Lunges", "Glute Bridges", "Calf Raises"],
        "Core": ["Side Plank", "Mountain Climbers", "High Knees",
                 "Bear Crawl", "Dead Bugs", "Planks", "Crunches"]
    }

    exercises = random.sample(workouts[group], 4 if time < 30 else 5)

    output = []

    for ex in exercises:

        weight = "Bodyweight"

        # Upper body strength lifts
        if ex in ["Bench Press", "Incline Bench Press", "Shoulder Press"]:
            w = calc_load(bench, energy, 60, 70, 85)
            weight = f"{w} lbs"

        elif ex in ["Bar Squats"]:
            w = calc_load(squat, energy, 65, 75, 85)
            weight = f"{w} lbs"

        elif ex in ["Goblet Squats", "RDL", "Lunges"]:
            w = calc_load(squat, energy, 40, 50, 60)
            weight = f"Dumbbells ~{w} lbs total"

        elif ex in ["Bicep Curls", "Tricep Dips", "Dumbbell Rows"]:
            w = calc_load(bench, energy, 30, 40, 50)
            weight = f"Dumbbells ~{w} lbs total"

        output.append((ex, weight))

    if energy >= 8:
        sets, duration = 3, "45 sec"
    elif energy >= 5:
        sets, duration = 3, "30 sec"
    else:
        sets, duration = 2, "20 sec"

    return output, sets, duration


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        group = request.form["group"]
        energy = int(request.form["energy"])
        time = int(request.form["time"])
        bench = int(request.form["bench"])
        squat = int(request.form["squat"])

        workout, sets, duration = get_workout(group, energy, time, bench, squat)

        return render_template_string(
            HTML,
            workout=workout,
            sets=sets,
            duration=duration
        )

    return render_template_string(HTML, workout=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
