import tkinter as tk
import time
import threading
import random
import difflib

# Set up the main Tkinter window
window = tk.Tk()
window.title("Typing Speed Test")
window.geometry("600x500")
window.configure(bg="pink")

# Instructions for the typing test
instructions = """Instructions:
1. Press 'Start' to begin.
2. Type the sentence as quick as you can.
3. Press 'Enter' to submit and see your WPM and Accuracy."""

# Display the instructions in a label
info_label = tk.Label(window, text=instructions, font=("Comic Sans MS", 12), bg="lightblue", fg="white", justify="left",
                      padx=10, pady=10)
info_label.pack(pady=10)

# List of sentences for the typing test
text_list = [
    "the quick brown fox jumps over the lazy dog.",
    "the five boxing wizards jump quickly.",
    "pack my box with five dozen liquor jugs.",
    "how quickly daft jumping zebras vex.",
    "Im just a girl",
]

# Label for the text the user needs to type
label = tk.Label(window, text="Type the following text:", font=("Comic Sans MS", 12), bg="pink", fg="white", padx=10,
                 pady=10)
label.pack() # adds label to the window, defaults places at top.

# Select a random sentence to be typed
text_to_type = random.choice(text_list)

# Display the selected sentence
label2 = tk.Label(window, text=text_to_type, font=("Comic Sans MS", 12), bg="pink", fg="white", padx=10, pady=10)
label2.pack()

# Entry widget for user input, initially disabled
text_box = tk.Entry(window, font=("Comic Sans MS", 12), width=50, borderwidth=2, relief="groove")
text_box.insert(0, "Press Start")
text_box.config(state="disabled", fg="gray")
text_box.pack(pady=10)


def text_box_focus_in(entry):
    # Enable the text box and clear the placeholder text when it gains focus
    text_box.configure(state=tk.NORMAL, fg="black")
    text_box.delete(0, tk.END)


text_box.bind("<FocusIn>", text_box_focus_in)

# StringVar to display the timer
timer_text = tk.StringVar()
label4 = tk.Label(window, textvariable=timer_text, font=("Comic Sans MS", 12), bg="pink", fg="white", padx=10, pady=10)
label4.pack()

# Global variables for timing and state management
running = False
start_time = None


def update_timer():
    #Continuously updates the timer while the typing test is active
    while running:
        elapsed_time = time.time() - start_time
        timer_text.set(f"Time taken: {elapsed_time:.3f} seconds")
        time.sleep(0.05)  # Update every 50ms


def calculate_accuracy(user_input, target_text):
    #Calculates the accuracy between the user's input and the target text.
    similarity = difflib.SequenceMatcher(None, user_input, target_text).ratio()
    return similarity * 100  # Return accuracy as a percentage


def key_press(event):
    #Handles typing progress and checks for the Enter key.
    global running
    if event.keysym == 'Return':  # If Enter is pressed
        running = False  # Stop the timer
        user_input = text_box.get()  # Get the user's typed input
        elapsed_time = time.time() - start_time  # Calculate elapsed time

        # Calculate WPM
        words = len(user_input.split())  # Count the words typed
        wpm = words / (elapsed_time / 60)  # Calculate WPM

        # Calculate accuracy
        accuracy = calculate_accuracy(user_input, text_to_type)

        # Display results
        timer_text.set(f"WPM: {wpm:.2f}, Accuracy: {accuracy:.2f}%, Time Taken: {elapsed_time:.2f} seconds")


# Bind key presses to the key_press function
text_box.bind("<Return>", key_press)


def start_test():
    #Starts the typing test and initializes the timer.
    global start_time, running
    start_time = time.time()  # Record the current time as the start time
    text_box.config(state=tk.NORMAL)
    #text_box.delete(0, tk.END)  # Clear any previous input
    timer_text.set("")  # Clear any previous results
    running = True  # Start the timer

    # Start the timer in the background
    threading.Thread(target=update_timer).start()
    retry_button.config(state=tk.NORMAL)


def retry_test():
    #Resets the typing test for another attempt.
    global start_time, running
    text_box.delete(0, tk.END)  # Clear any previous results
    timer_text.set("")  # Clear the results
    start_time = time.time()  # Restart the timer
    running = True  # Allow typing again
    threading.Thread(target=update_timer).start()


# Start button to begin the test
button1 = tk.Button(window, text="Start", command=start_test, bg="pink", fg="white", font=("Comic Sans MS", 12),
                    padx=10, pady=5, relief="ridge")
button1.pack(pady=5)

# Retry button to reset the test, initially disabled
retry_button = tk.Button(window, text="Retry", command=retry_test, bg="pink", fg="white", font=("Comic Sans MS", 12),
                         padx=10, pady=5, relief="ridge", state=tk.DISABLED)
retry_button.pack(pady=5)


def on_closing():
    #Stops the timer and closes the application safely."""
    global running
    running = False  # Stop the timer
    window.destroy()  # Close the Tkinter window


# Bind the close event to the on_closing function
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
window.mainloop()
