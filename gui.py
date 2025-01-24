import tkinter as tk
from tkinter import ttk
from interview import InterviewHandler
from textgen import TextGen
from fpdf import FPDF


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IELTS Speaking Test Simulator App")
        self.geometry("960x720")
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.container, width=960, height=720)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.interview_handler = InterviewHandler()
        self.eval_model = TextGen(mode='eval')
        self.mode = ""
        self.section = ""
        self.show_start_screen()

    def show_start_screen(self):
        self.clear_widgets()
        start_button = tk.Button(self.scrollable_frame, text="Start", font=("Arial", 16), command=self.show_main_menu)
        start_button.pack(expand=True)

    def show_main_menu(self):
        self.clear_widgets()
        options = ["Practice Mode", "Test Mode"]
        for option in options:
            button = tk.Button(self.scrollable_frame, text=option, font=("Arial", 14), width=20,
                               command=lambda opt=option: self.select_option(opt))
            button.pack()

    def select_option(self, option):
        self.mode = option
        if option == "Practice Mode":
            self.show_practice_menu()
        elif option == "Test Mode":
            self.run_test()

    def run_test(self):
        self.section = 'Test'
        self.interview_handler.set_section('Test')
        self.ask_questions()

    def show_practice_menu(self):
        self.clear_widgets()
        practice_options = ["Introduction", "Long Turn", "Two-Way Discussion"]
        for option in practice_options:
            button = tk.Button(self.scrollable_frame, text=option, font=("Arial", 14), width=25,
                               command=lambda opt=option: self.practice_option_selected(opt))
            button.pack(pady=5)
        back_button = tk.Button(self.scrollable_frame, text="Back", font=("Arial", 12), command=self.show_main_menu)
        back_button.pack(pady=10)

    def practice_option_selected(self, option):
        self.section = option
        self.interview_handler.set_section(option)
        self.ask_questions()

    def ask_questions(self):
        self.clear_widgets()

        question_label = tk.Label(self.scrollable_frame, text=self.interview_handler.question, font=("Arial", 14),
                                  wraplength=800)
        question_label.pack(pady=10)

        def start():
            self.interview_handler.start_recording()
            start_button.config(state='disabled')
            stop_button.config(state='normal')

        def check_response_ready(label):
            if self.interview_handler.next_ready:
                next()
            else:
                dots = question_label.cget("text").count('.') % 3
                new_text = f'Waiting for response{"." * (dots + 1)}'
                question_label.config(text=new_text)
                question_label.after(1000, check_response_ready, label)

        def stop():
            self.interview_handler.stop_recording()
            start_button.config(state='disabled')
            stop_button.config(state='disabled')
            check_response_ready(question_label)

        def next():
            self.interview_handler.next_question()
            question_label.config(text=self.interview_handler.question)
            if self.interview_handler.limit_reached:
                self.show_summary()
            else:
                start_button.config(state='normal')
                stop_button.config(state='disabled')

        start_button = tk.Button(self.scrollable_frame, text="Start", font=("Arial", 12), command=start)
        start_button.pack(pady=5)

        stop_button = tk.Button(self.scrollable_frame, text="Stop", font=("Arial", 12), command=stop)
        stop_button.pack(pady=5)

        answer_label = tk.Label(self.scrollable_frame, text=self.interview_handler.recognized_text, font=("Arial", 14),
                                wraplength=800)
        answer_label.pack(pady=10)

        def refresh():
            ans = self.interview_handler.answers
            idx = self.interview_handler.question_index
            if len(ans) > idx:
                if ans[idx] != "":
                    answer_label.config(text=ans[idx])
                else:
                    answer_label.config(text='Listening...')
            answer_label.after(1000, refresh)

        self.interview_handler.start_interview()
        refresh()

    def show_summary(self):
        self.clear_widgets()

        conv = self.interview_handler.format_questions_answers()

        if self.section != 'Test':
            feedback = self.eval_model.feedback(conv)
        else:
            feedback = self.eval_model.feedback(conv, f_type='full')

        end_label = tk.Label(self.scrollable_frame, text = feedback, font = ("Arial", 12), wraplength = 800)
        end_label.pack(pady=20)

        if self.section == 'Test':
            download_button = tk.Button(self.scrollable_frame, text="Download PDF", font=("Arial", 12),
                                        command= lambda: self.download_pdf(feedback))
            download_button.pack(pady=5)

        finish_button = tk.Button(self.scrollable_frame, text="Finish", font=("Arial", 12), command=self.show_main_menu)
        finish_button.pack(pady=5)

    def download_pdf(self, text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Courier', 'B', 16)
        pdf.cell(40, 10, text)
        pdf.output('test_feedback.pdf', 'F')

    def clear_widgets(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
