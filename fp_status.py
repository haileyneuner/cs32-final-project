from flask import Flask, render_template, request
import random

app = Flask(__name__)


def get_workout(group, energy, time, goal, bench_max, squat_max):

    upper = ["Bench Press", "Incline Bench Press", "Push-ups",
             "Shoulder Press", "Tricep Dips", "Dumbbell Rows"]

    lower = ["Bar Squats", "Goblet Squats", "Lunges",
             "RDL", "Glute Bridges", "Calf Raises"]

    core = ["Side Plank", "Mountain Climbers", "High Knees",
            "Bear Crawl", "Dead Bugs", "V-ups"]

    # select group
    if group == "Upper Body":
        exercises = upper
    elif group == "Lower Body":
        exercises = lower
    else:
        exercises = core

    # workout size based on time
    if time <= 15:
        count = 3
    elif time <= 45:
        count = 4
    else:
        count = 5

    chosen = random.sample(exercises, min(count, len(exercises)))
    plan = []

    for ex in chosen:

        # CORE → time based
        if group == "Core":
            duration = "0:45" if goal == "Lose Weight" else "0:30"
            plan.append(f"{ex}: 3 x {duration}")

        # UPPER → bench-based
        elif group == "Upper Body":
            if goal == "Gain Muscle":
                reps = "8–10"
                pct = 0.75
            else:
                reps = "12–15"
                pct = 0.60

            if "Bench" in ex or "Push" in ex:
                weight = int(bench_max * pct)
                plan.append(f"{ex}: 3 x {reps} @ {weight} lbs")
            else:
                plan.append(f"{ex}: 3 x {reps}")

        # LOWER → squat-based
        else:
            if goal == "Gain Muscle":
                reps = "8–10"
                pct = 0.75
            else:
                reps = "12–15"
                pct = 0.60

            if "Squat" in ex or "Lunge" in ex:
                weight = int(squat_max * pct)
                plan.append(f"{ex}: 3 x {reps} @ {weight} lbs")
            else:
                plan.append(f"{ex}: 3 x {reps}")

    return plan


@app.route("/", methods=["GET", "POST"])
def index():
    workout = None

    if request.method == "POST":
        group = request.form["group"]
        energy = int(request.form["energy"])
        time = int(request.form["time"])
        goal = request.form["goal"]
        bench = int(request.form["bench"])
        squat = int(request.form["squat"])

        workout = get_workout(group, energy, time, goal, bench, squat)

    return render_template("index.html", workout=workout)


if __name__ == "__main__":
    app.run(debug=True)
