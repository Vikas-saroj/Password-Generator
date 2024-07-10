import customtkinter as ctk
import random
import string
import pyperclip
from PIL import Image, ImageTk

# Function to generate a password based on selected character sets
def generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols):
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return "No character set selected"

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Event handler for the generate button
def on_generate():
    try:
        length = int(entry_length.get())
        if length <= 0:
            result_label.configure(text="Please enter an integer greater than 0.")
            return

        password = generate_password(
            length,
            uppercase_var.get(),
            lowercase_var.get(),
            digits_var.get(),
            symbols_var.get()
        )
        result_label.configure(text=f"Generated Password:\n {password}")
        copy_button.configure(state=ctk.NORMAL)

        rotate_image(0)
    except ValueError:
        result_label.configure(text="Invalid input. Please enter a valid number.")

# Function to copy the generated password to the clipboard
def copy_to_clipboard():
    password = result_label.cget("text")
    if password.startswith("Generated Password:"):
        password = password.replace("Generated Password:\n ", "")
        try:
            pyperclip.copy(password)
            result_label.configure(text=f"Copied to clipboard:\n {password}")
        except pyperclip.PyperclipException:
            result_label.configure(text="Failed to copy to clipboard.")
    else:
        try:
            pyperclip.copy(password)
            result_label.configure(text=password)
        except pyperclip.PyperclipException:
            result_label.configure(text="Failed to copy to clipboard.")

# Function to rotate the image on the generate button
def rotate_image(angle):
    global img, rotated_img, photo
    if angle >= -360:
        rotated_img = img.rotate(angle)
        photo = ctk.CTkImage(rotated_img)
        generate_button.configure(image=photo)
        app.after(5, rotate_image, angle - 24)  # Adjust the speed of the rotation by changing the delay and angle increment

# Create the main application window
app = ctk.CTk()
app.title("Password Generator")
app.geometry("380x400")

# Load and set the new icon
app.iconbitmap('images/password.ico')

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Create and place widgets
label_length = ctk.CTkLabel(app, text="Enter the length for the password:", text_color="#90CAF9", font=('default', 20))
label_length.pack(pady=5)

# Load the image for the button
img = Image.open("images/button.png")  # Replace with your image path
rotated_img = img
photo = ctk.CTkImage(img)

# Load the image for the copy button
img_copy = Image.open('images/copy.png')
image_copy = ctk.CTkImage(img_copy)

# Variables to store the state of checkboxes
uppercase_var = ctk.BooleanVar(value=True)
lowercase_var = ctk.BooleanVar(value=True)
digits_var = ctk.BooleanVar(value=True)
symbols_var = ctk.BooleanVar(value=True)

# Use a frame to hold the checkboxes and labels
checkbox_frame = ctk.CTkFrame(app)
checkbox_frame.pack(pady=5)

# Entry for password length
entry_length = ctk.CTkEntry(checkbox_frame, height=45, width=250, font=('default', 20, 'bold'))
# Generate button with image
generate_button = ctk.CTkButton(checkbox_frame, width=40, height=40, text="", image=photo, command=on_generate, fg_color="#018a26", hover_color="#014212")

# Checkboxes for character set options
uppercase_check = ctk.CTkCheckBox(checkbox_frame, text="Include Uppercase Letters", font=('default', 14), variable=uppercase_var, fg_color='#333333', checkmark_color="#48E91B")
lowercase_check = ctk.CTkCheckBox(checkbox_frame, text="Include Lowercase Letters", font=('default', 14), variable=lowercase_var, fg_color='#333333', checkmark_color="#48E91B")
digits_check = ctk.CTkCheckBox(checkbox_frame, text="Include Digits", font=('default', 14), variable=digits_var, fg_color='#333333', checkmark_color="#48E91B")
symbols_check = ctk.CTkCheckBox(checkbox_frame, text="Include Symbols", font=('default', 14), variable=symbols_var, fg_color='#333333', checkmark_color="#48E91B")

# Arrange checkboxes and entry in the frame using grid
entry_length.grid(row=0, column=0, sticky='w', padx=5, pady=(10, 10))
generate_button.grid(row=0, column=1, sticky='w', padx=(2, 5), pady=(10, 10))
uppercase_check.grid(row=1, column=0, sticky="w", padx=(5, 20), pady=(5, 5))
lowercase_check.grid(row=2, column=0, sticky="w", padx=(5, 20), pady=(5, 5))
digits_check.grid(row=3, column=0, sticky="w", padx=(5, 20), pady=(5, 5))
symbols_check.grid(row=4, column=0, sticky="w", padx=(5, 20), pady=(5, 5))

# Create and pack the result frame
result_frame = ctk.CTkFrame(app)
result_frame.pack(pady=20)

# Label to display generated password and copy button
result_label = ctk.CTkLabel(result_frame, text="", height=100, width=250, wraplength=250)
copy_button = ctk.CTkButton(result_frame, text="", image=image_copy, height=40, width=40, command=copy_to_clipboard, fg_color="#018a26", hover_color="#014212", state=ctk.DISABLED)

result_label.grid(row=0, column=0, sticky='w', padx=5, pady=(10, 10))
copy_button.grid(row=0, column=1, sticky='ne', padx=5, pady=(10, 10))

# Start the main loop
app.mainloop()
