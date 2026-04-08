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

# Simple Workout Generator

def get_workout(group, muscles, energy, time):
    workouts = {
        "Upper Body": [
            "Push-ups", "Pull-ups", "Shoulder Taps", "Tricep Dips"
        ],
        "Lower Body": [
            "Squats", "Lunges", "Glute Bridges", "Calf Raises"
        ],
        "Core": [
            "Side Plank", "Mountain Climbers", "High Knees", "Bear Crawl"
        ]
    }

    selected_exercises = workouts.get(group, [])

    # Adjust intensity based on energy
    if energy >= 8:
        sets = 3
        duration = "0:30"
    elif energy >= 5:
        sets = 2
        duration = "0:20"
    else:
        sets = 1
        duration = "0:15"

    # Adjust volume based on time
    if time < 15:
        selected_exercises = selected_exercises[:3]
    elif time >= 30:
        selected_exercises = selected_exercises + selected_exercises[:2]

    return selected_exercises, sets, duration


def ask_question(prompt, valid_options=None, cast_func=str):
    while True:
        answer = input(prompt).strip()

        if valid_options:
            if answer.lower() in [opt.lower() for opt in valid_options]:
                return answer
            else:
                print(f"Please choose from: {', '.join(valid_options)}")
        else:
            try:
                return cast_func(answer)
            except:
                print("Invalid input, try again.")


def main():
    print("=== Workout Generator ===\n")

    group = ask_question(
        "1. What muscle group? (Upper Body, Lower Body, Core): ",
        ["Upper Body", "Lower Body", "Core"]
    )

    muscles = ask_question(
        f"2. Which specific muscles in {group}? "
    )

    energy = ask_question(
        "3. Energy level (1-10): ",
        cast_func=int
    )

    time = ask_question(
        "4. Available time (minutes): ",
        cast_func=int
    )

    exercises, sets, duration = get_workout(group, muscles, energy, time)

    print("\n=== Workout of the Day ===")
    for ex in exercises:
        if ex == "Bear Crawl":
            print(f"{ex}: {sets} x 10 yards")
        else:
            print(f"{ex}: {sets} x {duration}")


if __name__ == "__main__":
    main()
    
