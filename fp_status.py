from flask import Flask, render_template, request
import random

app = Flask(__name__)

def get_workout(group, energy, time):
    workouts = {
        "Upper Body": ["Push-ups", "Pull-ups", "Shoulder Press", "Tricep Dips",
                       "Bicep Curls", "Bench Press", "Incline Bench Press", "Dumbbell Rows"],
        "Lower Body": ["Bar Squats", "Goblet Squats", "Bulgarian Split Squats",
                       "RDL", "Lunges", "Glute Bridges", "Calf Raises"],
        "Core": ["Side Plank", "Mountain Climbers", "High Knees", "Bear Crawl",
                 "Dead Bugs", "Elbow Planks", "V-ups", "Crunches",
                 "Toe Taps", "Bicycle Kicks", "Hollow Holds"]
    }

    exercises = workouts[group]

    if time <= 10:
        num_exercises = 3
    elif time <= 20:
        num_exercises = 4
    else:
        num_exercises = 5

    selected = random.sample(exercises, min(num_exercises, len(exercises)))

    if energy >= 8:
        sets = 3
        duration = "0:45"
    elif energy >= 6:
        sets = 3
        duration = "0:30"
    elif energy >= 4:
        sets = 2
        duration = "0:30"
    else:
        sets = 2
        duration = "0:15"

    return selected, sets, duration


@app.route("/", methods=["GET", "POST"])
def index():
    workout = None

    if request.method == "POST":
        group = request.form["group"]
        energy = int(request.form["energy"])
        time = int(request.form["time"])

        exercises, sets, duration = get_workout(group, energy, time)
        workout = [(ex, sets, duration) for ex in exercises]

    return render_template("index.html", workout=workout)


if __name__ == "__main__":
    app.run(debug=True)
