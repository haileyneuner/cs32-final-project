from flask import Flask, render_template, request
import random

app = Flask(__name__)

def get_workout(group, energy, time, goal, bench_max, squat_max):
    upper_workouts = ["Bench Press", "Incline Bench Press", "Push-ups",
                      "Shoulder Press", "Tricep Dips", "Dumbbell Rows"]

    lower_workouts = ["Bar Squats", "Goblet Squats", "Lunges",
                      "RDL", "Glute Bridges", "Calf Raises"]

    core_workouts = ["Side Plank", "Mountain Climbers", "High Knees",
                     "Bear Crawl", "Dead Bugs", "V-ups"]

    # choose correct list
    if group == "Upper Body":
        exercises = upper_workouts
    elif group == "Lower Body":
        exercises = lower_workouts
    else:
        exercises = core_workouts

    # number of exercises
    if time <= 15:
        num_exercises = 3
    elif time <= 45:
        num_exercises = 4
    else:
        num_exercises = 5

    selected = random.sample(exercises, min(num_exercises, len(exercises)))
    workout_plan = []

    for ex in selected:

        # CORE (time-based)
        if group == "Core":
            duration = "0:45" if goal == "Lose Weight" else "0:30"
            sets = 3
            workout_plan.append(f"{ex}: {sets} x {duration}")

        # UPPER BODY (bench-based)
        elif group == "Upper Body":
            if goal == "Gain Muscle":
                reps = "8–10"
                intensity = 0.75
            else:
                reps = "12–15"
                intensity = 0.60

            # weight logic for upper
            if "Bench" in ex or "Push" in ex:
                weight = int(bench_max * intensity)
                workout_plan.append(f"{ex}: 3 x {reps} @ {weight} lbs")
            else:
                workout_plan.append(f"{ex}: 3 x {reps} (Bodyweight/Moderate)")

        # 🦵 LOWER BODY (squat-based)
        elif group == "Lower Body":
            if goal == "Gain Muscle":
                reps = "8–10"
                intensity = 0.75
            else:
                reps = "12–15"
                intensity = 0.60

            # weight logic for lower
            if "Squat" in ex or "Lunge" in ex:
                weight = int(squat_max * intensity)
                workout_plan.append(f"{ex}: 3 x {reps} @ {weight} lbs")
            else:
                workout_plan.append(f"{ex}: 3 x {reps} (Bodyweight/Moderate)")

    return workout_plan


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
