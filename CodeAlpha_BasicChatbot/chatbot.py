import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox, filedialog
from datetime import datetime


class SmartChatbot:
    def _init_(self, root):
        self.root = root
        self.root.title("GUI-Based Rule-Based Chatbot")
        self.root.geometry("750x600")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        self.chat_history = []

        self.create_header()
        self.create_chat_area()
        self.create_input_area()
        self.create_footer()

        self.display_message(
            "Bot",
            "Hello! I am your Smart Rule-Based Chatbot.\n"
            "Type 'help' to see available commands."
        )

    def create_header(self):
        header = tk.Frame(self.root, bg="#1e293b", height=60)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="SMART CHATBOT",
            font=("Helvetica", 20, "bold"),
            bg="#1e293b",
            fg="white"
        )
        title.pack(pady=15)

    def create_chat_area(self):
        chat_frame = tk.Frame(self.root, bg="#0f172a")
        chat_frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

        self.chat_area = ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Arial", 12),
            bg="#f8fafc",
            fg="#0f172a",
            state="disabled",
            padx=10,
            pady=10
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)

    def create_input_area(self):
        input_frame = tk.Frame(self.root, bg="#0f172a")
        input_frame.pack(fill=tk.X, padx=15, pady=10)

        self.entry_box = tk.Entry(
            input_frame,
            font=("Arial", 13),
            bg="white",
            fg="black",
            relief=tk.FLAT
        )
        self.entry_box.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            ipady=10,
            padx=(0, 10)
        )

        self.entry_box.bind("<Return>", self.send_message)

        send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 12, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            activeforeground="white",
            width=10,
            command=self.send_message
        )
        send_button.pack(side=tk.LEFT)

        clear_button = tk.Button(
            input_frame,
            text="Clear",
            font=("Arial", 12, "bold"),
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            width=10,
            command=self.clear_chat
        )
        clear_button.pack(side=tk.LEFT, padx=(10, 0))

        save_button = tk.Button(
            input_frame,
            text="Save",
            font=("Arial", 12, "bold"),
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            width=10,
            command=self.save_chat
        )
        save_button.pack(side=tk.LEFT, padx=(10, 0))

    def create_footer(self):
        footer = tk.Label(
            self.root,
            text="Internship Project - Python Tkinter Chatbot",
            font=("Arial", 10),
            bg="#1e293b",
            fg="white",
            pady=8
        )
        footer.pack(fill=tk.X, side=tk.BOTTOM)

    def display_message(self, sender, message):
        current_time = datetime.now().strftime("%I:%M %p")
        formatted_message = f"{sender} [{current_time}]: {message}\n\n"

        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, formatted_message)
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

        self.chat_history.append(formatted_message)

    def get_response(self, user_text):
        text = user_text.lower().strip()

        if text in ["hello", "hi", "hey", "good morning", "good evening"]:
            return "Hello! Welcome. How can I assist you today?"

        elif "how are you" in text:
            return "I am doing great and ready to help you."

        elif "your name" in text or "who are you" in text:
            return "I am a GUI-based rule-based chatbot developed using Python Tkinter."

        elif "time" in text:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}."

        elif "date" in text:
            return f"Today's date is {datetime.now().strftime('%d-%m-%Y')}."

        elif "help" in text:
            return (
                "Available commands:\n"
                "- hello / hi / hey\n"
                "- how are you\n"
                "- who are you\n"
                "- time\n"
                "- date\n"
                "- internship\n"
                "- python\n"
                "- project\n"
                "- bye"
            )

        elif "internship" in text:
            return "This chatbot is designed as an internship mini project using Python GUI."

        elif "python" in text:
            return "Python is a high-level, easy-to-learn programming language used in AI, web, automation, and GUI applications."

        elif "project" in text:
            return "This project demonstrates GUI design, event handling, rule-based logic, and file handling using Python."

        elif text in ["bye", "exit", "quit"]:
            return "Goodbye! Thank you for using the chatbot."

        else:
            return "Sorry, I did not understand that. Please try a different question."

    def send_message(self, event=None):
        user_message = self.entry_box.get().strip()

        if user_message == "":
            messagebox.showwarning("Empty Input", "Please enter a message.")
            return

        self.display_message("You", user_message)
        bot_reply = self.get_response(user_message)
        self.display_message("Bot", bot_reply)

        self.entry_box.delete(0, tk.END)

        if user_message.lower() in ["bye", "exit", "quit"]:
            self.root.after(1500, self.root.destroy)

    def clear_chat(self):
        confirm = messagebox.askyesno(
            "Clear Chat",
            "Do you want to clear the chat?"
        )

        if confirm:
            self.chat_area.config(state="normal")
            self.chat_area.delete("1.0", tk.END)
            self.chat_area.config(state="disabled")
            self.chat_history.clear()

            self.display_message(
                "Bot",
                "Chat cleared successfully. How can I help you now?"
            )

    def save_chat(self):
        if not self.chat_history:
            messagebox.showinfo(
                "Save Chat",
                "No chat history available to save."
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Chat History"
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(self.chat_history)

            messagebox.showinfo(
                "Save Chat",
                "Chat history saved successfully."
            )


if _name_ == "_main_":
    root = tk.Tk()
    app = SmartChatbot(root)
    root.mainloop()
