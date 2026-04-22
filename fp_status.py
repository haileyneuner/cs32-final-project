from flask import Flask, render_template, request
import random
import math

app = Flask(__name__)


def round_to_5(x):
    return int(round(x / 5) * 5)


def get_workout(group, energy, time, goal, bench_max, squat_max):

    upper = ["Bench Press", "Incline Bench Press", "Push-ups",
             "Shoulder Press", "Tricep Dips", "Dumbbell Rows"]

    lower = ["Bar Squats", "Goblet Squats", "Lunges",
             "RDL", "Glute Bridges", "Calf Raises"]

    core = ["Side Plank", "Mountain Climbers", "High Knees",
            "Bear Crawl", "Dead Bugs", "V-ups"]

    if group == "Upper Body":
        exercises = upper
    elif group == "Lower Body":
        exercises = lower
    else:
        exercises = core

    if time <= 15:
        count = 3
    elif time <= 45:
        count = 4
    else:
        count = 5

    chosen = random.sample(exercises, min(count, len(exercises)))
    plan = []

    for ex in chosen:

        # CORE = TIME BASED
        if group == "Core":
            duration = "45 sec" if goal == "Lose Weight" else "30 sec"
            plan.append(f"{ex}: 3 x {duration}")

        # UPPER = WEIGHT BASED (bench)
        elif group == "Upper Body":

            if goal == "Gain Muscle":
                reps = "8–10"
                pct = 0.75
            else:
                reps = "12–15"
                pct = 0.60

            weight = None

            if "Bench" in ex or "Push" in ex or "Press" in ex:
                weight = round_to_5(bench_max * pct)
            else:
                weight = round_to_5(bench_max * 0.4)

            plan.append(f"{ex}: 3 x {reps} @ {weight} lbs")

        # LOWER = WEIGHT BASED (squat)
        else:

            if goal == "Gain Muscle":
                reps = "8–10"
                pct = 0.75
            else:
                reps = "12–15"
                pct = 0.60

            if "Squat" in ex or "Lunge" in ex:
                weight = round_to_5(squat_max * pct)
            else:
                weight = round_to_5(squat_max * 0.5)

            plan.append(f"{ex}: 3 x {reps} @ {weight} lbs")

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

    return render_template("index.html", workout=workout, group=None)


if __name__ == "__main__":
    app.run(debug=True)
