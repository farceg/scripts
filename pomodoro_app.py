import tkinter as tk
import winsound


class TimerApp:
    def __init__(self, work_duration, rest_duration):
        self.work_duration = work_duration
        self.rest_duration = rest_duration
        self.remaining = work_duration
        self.running = False
        self.in_work_phase = True  # To track if we are in work or rest phase
        self.create_window()

    def create_window(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.6)
        self.root.geometry(f"160x80+{self.root.winfo_screenwidth()-180}+20")
        self.root.configure(bg="black")

        self.close_button = tk.Button(
            self.root,
            text="X",
            font=("Arial", 11),
            command=self.close_window,
            bg="black",
            fg="white",
            bd=0,
        )
        self.close_button.place(x=140, y=2)

        self.label = tk.Label(
            self.root, text="00:00", font=("Arial", 12), bg="black", fg="white"
        )
        self.label.place(relx=0.5, rely=0.3, anchor="center")

        self.stop_button = tk.Button(
            self.root,
            text="Stop",
            font=("Arial", 10),
            command=self.stop_timer,
            bg="red",
            fg="white",
        )
        self.stop_button.place(relx=0.3, rely=0.7, anchor="center")

        self.restart_button = tk.Button(
            self.root,
            text="Restart",
            font=("Arial", 10),
            command=self.restart_timer,
            bg="green",
            fg="white",
        )
        self.restart_button.place(relx=0.7, rely=0.7, anchor="center")

        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<B1-Motion>", self.on_drag)

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.x_offset = 0
        self.y_offset = 0

    def on_click(self, event):
        """Save the mouse position when the user clicks on the window."""
        self.x_offset = event.x
        self.y_offset = event.y

    def on_drag(self, event):
        """Move the window while dragging."""
        x = self.root.winfo_x() - self.x_offset + event.x
        y = self.root.winfo_y() - self.y_offset + event.y
        self.root.geometry(f"+{x}+{y}")

    def update_timer(self):
        """Update the timer display and check for end of timer."""
        if self.running and self.remaining > 0:
            mins, secs = divmod(self.remaining, 60)
            self.label.config(text=f"{mins:02}:{secs:02}")
            self.remaining -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining == 0:
            self.label.config(text="00:00")
            self.running = False
            self.play_sound()
            self.switch_phase()

    def stop_timer(self):
        """Stop the timer and change the Restart button to 'Continue'."""
        self.running = False
        self.restart_button.config(
            text="Continue", bg="blue", command=self.continue_timer
        )

    def continue_timer(self):
        """Resume the timer when clicking 'Continue'."""
        self.running = True
        self.update_timer()
        self.restart_button.config(
            text="Restart", bg="green", command=self.restart_timer
        )

    def restart_timer(self):
        """Reset the timer to the original duration."""
        self.running = False
        self.remaining = (
            self.work_duration if self.in_work_phase else self.rest_duration
        )
        self.label.config(text="00:00")
        self.restart_button.config(
            text="Continue", bg="blue", command=self.continue_timer
        )

    def play_sound(self):
        """Play a beep sound when the timer ends."""
        winsound.Beep(4000, 1200)

    def switch_phase(self):
        """Switch between work and rest phases after each block ends."""
        if self.in_work_phase:
            self.remaining = self.rest_duration
            self.in_work_phase = False
            self.label.config(text="Rest")
        else:
            self.remaining = self.work_duration
            self.in_work_phase = True
            self.label.config(text="Work")
        self.restart_button.config(
            text="Continue", bg="blue", command=self.continue_timer
        )

    def start_timer(self):
        self.remaining = self.work_duration
        self.running = True
        self.update_timer()
        self.root.mainloop()

    def close_window(self):
        """Gracefully close the application."""
        self.running = False
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    # Ask the user for work and rest durations
    work_time = int(input("Enter work time in minutes: ")) * 60
    rest_time = int(input("Enter rest time in minutes: ")) * 60

    app = TimerApp(work_time, rest_time)
    app.start_timer()
