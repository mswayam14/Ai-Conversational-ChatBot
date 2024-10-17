import tkinter as tk
from tkinter import messagebox
import google.generativeai as ai

API_KEY = 'AIzaSyBuqrWqXF7n2EItLkKfdw3ICsq1sqEdbaw'
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()
history = []
feedback_list = []

class ChatbotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.root.configure(background="#f0f0f0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.header_frame = tk.Frame(self.root, bg="#333", height=50)
        self.header_frame.place(relx=0, rely=0, relwidth=1, anchor='nw')

        self.header_label = tk.Label(self.header_frame, text="Chatbot", font=("Arial", 20), fg="white", bg="#333")
        self.header_label.place(relx=0.5, rely=0.5, anchor='center')

        self.chat_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.chat_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9, anchor='nw')

        self.message_label = tk.Label(self.chat_frame, text="You:", font=("Arial", 14), fg="#333", bg="#f0f0f0")
        self.message_label.place(relx=0.1, rely=0.05, anchor='nw')

        self.message_entry = tk.Text(self.chat_frame, height=5, width=60, font=("Arial", 14), fg="#333", bg="#f0f0f0")
        self.message_entry.place(relx=0.1, rely=0.1, relwidth=0.8, anchor='nw')

        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message, font=("Arial", 14), fg="white", bg="#007bff", borderwidth=0, relief="flat", padx=6, pady=3)
        self.send_button.place(relx=0.9, rely=0.1, anchor='ne')

        self.response_label = tk.Label(self.chat_frame, text="Chatbot:", font=("Arial", 14), fg="#333", bg="#f0f0f0")
        self.response_label.place(relx=0.1, rely=0.3, anchor='nw')

        self.response_text = tk.Text(self.chat_frame, height=5, width=60, font=("Arial", 14), fg="#333", bg="#f0f0f0")
        self.response_text.place(relx=0.1, rely=0.35, relwidth=0.8, anchor='nw')

        self.feedback_label = tk.Label(self.chat_frame, text="Was this response helpful? (yes/no):", font=("Arial", 14), fg="#333", bg="#f0f0f0")
        self.feedback_label.place(relx=0.1, rely=0.6, anchor='nw')

        self.feedback_entry = tk.Entry(self.chat_frame, width=60, font=("Arial", 14), fg="#333", bg="#f0f0f0")
        self.feedback_entry.place(relx=0.1, rely=0.65, relwidth=0.8, anchor='nw')

        self.feedback_button = tk.Button(self.chat_frame, text="Submit", command=self.submit_feedback, font=("Arial", 12), fg="white", bg="#007bff", borderwidth=0, relief="flat", padx=2, pady=1)
        self.feedback_button.place(relx=0.9, rely=0.65, anchor='ne')

        self.summary_button = tk.Button(self.chat_frame, text="Show Feedback Summary", command=self.show_feedback_summary, font=("Arial", 14), fg="white", bg="#007bff", borderwidth=0, relief="flat", padx=10, pady=5)
        self.summary_button.place(relx=0.5, rely=0.8, anchor='center')

    def send_message(self):
        message = self.message_entry.get("1.0", "end-1c")
        if message.lower() == 'bye':
            self.show_feedback_summary()
            messagebox.showinfo("Goodbye", "Goodbye!")
            self.root.quit()
        global history
        history.append(message)
        try:
            response = chat.send_message('\n'.join(history))
            self.response_text.delete("1.0", "end")
            self.response_text.insert("1.0", response.text)
            self.feedback_entry.delete ("0", "end")
            self.message_entry.delete("1.0", "end")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def submit_feedback(self):
        global feedback_list
        feedback = self.feedback_entry.get()
        if feedback .lower() == 'yes':
            feedback_list.append(True)
        elif feedback.lower() == 'no':
            feedback_list.append(False)
        else:
            messagebox.showerror("Invalid Feedback", "Please enter 'yes' or 'no'.")
            return
        self.feedback_entry.delete("0", "end")
        self.message_entry.delete("1.0", "end")

    def show_feedback_summary(self):
        global feedback_list
        if len(feedback_list) == 0:
            messagebox.showinfo("No Feedback", "No feedback has been submitted.")
            return
        yes_count = feedback_list.count(True)
        no_count = feedback_list.count(False)
        summary = f"Feedback Summary:\nYes: {yes_count}\nNo: {no_count}"
        messagebox.showinfo("Feedback Summary", summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()