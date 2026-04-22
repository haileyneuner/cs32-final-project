import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


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


class FitnessUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)

        # Title
        self.add_widget(Label(text="Workout Generator", font_size=28, size_hint=(1, 0.2)))

        # Muscle group input
        self.group_input = TextInput(
            hint_text="Enter: Upper Body, Lower Body, or Core",
            multiline=False
        )
        self.add_widget(self.group_input)

        # Energy input
        self.energy_input = TextInput(
            hint_text="Energy level (1-10)",
            multiline=False,
            input_filter='int'
        )
        self.add_widget(self.energy_input)

        # Time input
        self.time_input = TextInput(
            hint_text="Time (minutes)",
            multiline=False,
            input_filter='int'
        )
        self.add_widget(self.time_input)

        # Generate button
        btn = Button(text="Generate Workout", size_hint=(1, 0.3))
        btn.bind(on_press=self.generate_workout)
        self.add_widget(btn)

        # Output label
        self.output = Label(text="Your workout will appear here",
                            halign="left",
                            valign="top")
        self.output.bind(size=self.output.setter('text_size'))
        self.add_widget(self.output)

    def generate_workout(self, instance):
        group = self.group_input.text.title()

        # Validate inputs
        try:
            energy = int(self.energy_input.text)
            time = int(self.time_input.text)
        except:
            self.output.text = "Please enter valid numbers."
            return

        if group not in ["Upper Body", "Lower Body", "Core"]:
            self.output.text = "Invalid muscle group."
            return

        exercises, sets, duration = get_workout(group, energy, time)

        # Format output nicely
        result = "WORKOUT OF THE DAY\n\n"
        for ex in exercises:
            result += f"{ex}: {sets} x {duration}\n"

        self.output.text = result


class FitnessApp(App):
    def build(self):
        return FitnessUI()


if __name__ == "__main__":
    FitnessApp().run()
