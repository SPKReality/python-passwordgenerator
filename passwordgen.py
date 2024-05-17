import tkinter as tk
from ttkbootstrap import Style
from tkinter import ttk
from tkinter import messagebox
import string
import random
from PIL import Image, ImageTk

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x500")

        self.style = Style(theme='flatly')
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TRadiobutton', font=('Helvetica', 12))

        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill='both', expand=True)

        self.header_label = ttk.Label(self.main_frame, text="Password Generator", font=('Helvetica', 16, 'bold'))
        self.header_label.pack(pady=10)

        self.length_label = ttk.Label(self.main_frame, text="Password Length:")
        self.length_label.pack(pady=5)

        self.length_var = tk.IntVar(value=12)
        self.length_entry = ttk.Entry(self.main_frame, textvariable=self.length_var, width=10)
        self.length_entry.pack(pady=5)

        self.characters_label = ttk.Label(self.main_frame, text="Custom Characters (optional):")
        self.characters_label.pack(pady=5)

        self.characters_var = tk.StringVar()
        self.characters_entry = ttk.Entry(self.main_frame, textvariable=self.characters_var, width=30)
        self.characters_entry.pack(pady=5)

        self.strength_label = ttk.Label(self.main_frame, text="Password Strength:")
        self.strength_label.pack(pady=5)

        self.strength_var = tk.StringVar(value="Strong")
        self.strong_radio = ttk.Radiobutton(self.main_frame, text="Strong", variable=self.strength_var, value="Strong")
        self.medium_radio = ttk.Radiobutton(self.main_frame, text="Medium", variable=self.strength_var, value="Medium")
        self.weak_radio = ttk.Radiobutton(self.main_frame, text="Weak", variable=self.strength_var, value="Weak")

        self.strong_radio.pack(pady=2)
        self.medium_radio.pack(pady=2)
        self.weak_radio.pack(pady=2)

        self.generate_button = ttk.Button(self.main_frame, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=15)

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.main_frame, textvariable=self.password_var, state='readonly', width=50)
        self.password_entry.pack(pady=10)

        self.status_label = ttk.Label(self.main_frame, text="", font=('Helvetica', 10, 'italic'))
        self.status_label.pack(pady=5)

        # Password history list
        self.password_history = []

    def generate_password(self):
        # Clear password entry field
        self.password_var.set("")

        length = self.length_var.get()
        if length < 4:
            messagebox.showwarning("Invalid Length", "Password length should be at least 4")
            return

        custom_characters = self.characters_var.get()
        if custom_characters:
            characters = custom_characters
        else:
            strength = self.strength_var.get()
            if strength == "Strong":
                characters = string.ascii_letters + string.digits + string.punctuation
            elif strength == "Medium":
                characters = string.ascii_letters + string.digits
            else:  # Weak
                characters = string.ascii_lowercase

        password = ''.join(random.choice(characters) for _ in range(length))

        # Check if the password is in history, regenerate if it is
        if password in self.password_history:
            self.generate_password()
            return

        self.password_history.append(password)
        self.password_var.set(password)
        self.copy_to_clipboard(password)
        self.ask_satisfaction(password)

    def copy_to_clipboard(self, password):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()  # now it stays on the clipboard after the window is closed
            self.status_label.config(text="Password copied to clipboard!", foreground='green')
        except Exception as e:
            messagebox.showerror("Error", "Failed to copy password to clipboard.")

    def ask_satisfaction(self, password):
        response = messagebox.askyesno("Password Satisfaction", f"Generated password: {password}\n\nAre you satisfied with the generated password?")
        if not response:
            self.generate_password()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
