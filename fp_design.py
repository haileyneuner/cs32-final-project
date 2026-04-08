# sample input:
# ask user: "What muscle group would you like to workout today? Select: Upper Body, Lower Body, Core"
# user input: "Core"
# ask user: "Which muscles would you like to train within [group]?"
# user input: "All"
# "how much energy do you have today to spend on a scale of 1-10"
# user input: "10"
# "how much time do you have?"
# user input: "10" # list of input options

# ouput example (resemble workout app interface):
# Workout of the Day
# Side Plank 3x0:30
# Mountain Climbers 3x0:30
# High Knees 3x0:30
# Bear Crawl 3x10 yards

import random  # lets us pick random items

def get_workout(group, energy, time):

    workouts = {
        "Upper Body": ["Push-ups", "Pull-ups", "Shoulder Taps", "Tricep Dips"],
        "Lower Body": ["Squats", "Lunges", "Glute Bridges", "Calf Raises"],
        "Core": ["Side Plank", "Mountain Climbers", "High Knees", "Bear Crawl"]
    }

    # Get list for chosen group
    exercises = workouts[group]

    # Decide how many exercises based on time
    if time < 15:
        num_exercises = 3
    elif time >= 30:
        num_exercises = 5
    else:
        num_exercises = 4

    # Pick random exercises
    exercises = random.sample(exercises, min(num_exercises, len(exercises)))

    # Decide difficulty based on energy
    if energy >= 8:
        sets = 3
        duration = "30 sec"
    elif energy >= 5:
        sets = 2
        duration = "20 sec"
    else:
        sets = 1
        duration = "15 sec"

    return exercises, sets, duration


def main():
    print("=== Workout Generator ===\n")

    group = input("Muscle group (Upper Body, Lower Body, Core): ")
    energy = int(input("Energy level (1-10): "))
    time = int(input("Time available (minutes): "))

    exercises, sets, duration = get_workout(group, energy, time)

    print("\nYour Workout:")
    for ex in exercises:
        print(f"{ex}: {sets} x {duration}")


main()

