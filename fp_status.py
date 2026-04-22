import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class FitnessApp(App):
    def build(self):
        self.workouts = []

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(text="Fitness Tracker", font_size=24)
        layout.add_widget(title)

        self.input = TextInput(hint_text="Enter workout (e.g. Push-ups)")
        layout.add_widget(self.input)

        add_btn = Button(text="Add Workout")
        add_btn.bind(on_press=self.add_workout)
        layout.add_widget(add_btn)

        self.output = Label(text="No workouts yet")
        layout.add_widget(self.output)

        return layout

    def add_workout(self, instance):
        workout = self.input.text
        if workout:
            self.workouts.append(workout)
            self.output.text = "\n".join(self.workouts)
            self.input.text = ""

if __name__ == "__main__":
    FitnessApp().run()
    