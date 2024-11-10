import tkinter as tk
from tkinter import messagebox
import time
quiz_data = [
    {
        "question": "What are the two core components of OKRs?",
        "choices": ["A) Objectives and Key Results", "B) Objectives and Key Metrics", "C) Outputs and Key Results", "D) Operational Key Results"],
        "correct": ["A"]
    },
    {
        "question": "Which of the following are characteristics of effective Key Results? (Select multiple)",
        "choices": ["A) Specific", "B) Measurable", "C) Ambiguous", "D) Time-bound"],
        "correct": ["A", "B", "D"]
    },
    {
        "question": "What is the ideal percentage completion rate for 'aspirational' OKRs?",
        "choices": ["A) 100%", "B) 50%", "C) 70%", "D) 90%"],
        "correct": ["C"]
    },
    {
        "question": "Who introduced the OKR framework to Google?",
        "choices": ["A) Eric Schmidt", "B) Larry Page", "C) John Doerr", "D) Sundar Pichai"],
        "correct": ["C"]
    },
    {
        "question": "What are the benefits of making OKRs public within an organization? (Select multiple)",
        "choices": ["A) Increases transparency", "B) Enhances accountability", "C) Helps employees set personal financial goals", "D) Aligns teams with company objectives"],
        "correct": ["A", "B", "D"]
    },
    {
        "question": "What is the primary purpose of OKRs in a company?",
        "choices": ["A) To improve sales performance", "B) To align individual and organizational goals", "C) To reduce the need for project managers", "D) To increase marketing output"],
        "correct": ["B"]
    },
    {
        "question": "In the book, which company is highlighted for adopting OKRs early and scaling its success?",
        "choices": ["A) Microsoft", "B) Google", "C) Intel", "D) Amazon"],
        "correct": ["C"]
    },
    {
        "question": "Which of the following can be considered 'committed' OKRs? (Select multiple)",
        "choices": ["A) Aspirational goals", "B) Goals that must be achieved 100%", "C) Long-term plans", "D) Quarterly deliverables tied to team performance"],
        "correct": ["B", "D"]
    },
    {
        "question": "How did OKRs help Google during its rapid growth?",
        "choices": ["A) By increasing marketing resources", "B) By focusing on the right projects and aligning the team", "C) By creating more sales channels", "D) By reducing product development costs"],
        "correct": ["B"]
    },
    {
        "question": "What does CFR stand for in relation to OKRs?",
        "choices": ["A) Continuous Feedback Results", "B) Collaboration, Feedback, Recognition", "C) Comprehensive Forecast Review", "D) Collaborative Framework for Results"],
        "correct": ["B"]
    },
    {
        "question": "How often are OKRs typically reviewed in high-performing organizations?",
        "choices": ["A) Annually", "B) Monthly", "C) Quarterly", "D) Weekly"],
        "correct": ["C"]
    },
    {
        "question": "What are the key elements of a well-defined Objective in the OKR framework? (Select multiple)",
        "choices": ["A) Time-bound", "B) Measurable", "C) Ambitious", "D) Vague"],
        "correct": ["A", "B", "C"]
    },
    {
        "question": "What is one of the main risks of setting OKRs that are too easy to achieve?",
        "choices": ["A) Decreases employee satisfaction", "B) Discourages innovation and risk-taking", "C) Leads to poor financial performance", "D) Increases burnout rates"],
        "correct": ["B"]
    },
    {
        "question": "What term is used for OKRs that are difficult to achieve but push teams to perform at their best?",
        "choices": ["A) Stretch OKRs", "B) Committed OKRs", "C) Moonshot OKRs", "D) Incremental OKRs"],
        "correct": ["C"]
    },
    {
        "question": "Why is it important for Key Results to be measurable?",
        "choices": ["A) To ensure subjective progress tracking", "B) To provide a numerical basis for evaluation", "C) To align financial goals", "D) To keep the OKR process flexible"],
        "correct": ["B"]
    },
    {
        "question": "Which of the following are considered benefits of OKRs for an organization? (Select multiple)",
        "choices": ["A) Better alignment of teams", "B) Improved employee focus", "C) Guaranteed revenue growth", "D) Transparent progress tracking"],
        "correct": ["A", "B", "D"]
    },
    {
        "question": "How does John Doerr recommend handling OKRs that are not completed by the deadline?",
        "choices": ["A) Carry them over to the next quarter", "B) Drop them entirely", "C) Reassess and adjust them", "D) Increase the number of Key Results"],
        "correct": ["C"]
    },
    {
        "question": "What factors should be considered when setting an OKR? (Select multiple)",
        "choices": ["A) Business impact", "B) Employee capabilities", "C) Feasibility", "D) Customer feedback"],
        "correct": ["A", "B", "C"]
    },
    {
        "question": "Which organization used OKRs to improve its advocacy strategy, as mentioned in the book?",
        "choices": ["A) The Bill & Melinda Gates Foundation", "B) ONE (Bono’s nonprofit)", "C) World Health Organization", "D) UNICEF"],
        "correct": ["B"]
    },
    {
        "question": "Which of the following is not a recommended practice for successful OKR implementation?",
        "choices": ["A) Holding regular check-ins", "B) Setting vague objectives", "C) Keeping OKRs transparent", "D) Ensuring Key Results are measurable"],
        "correct": ["B"]
    },
    {
        "question": "Which are the two types of OKRs discussed in Measure What Matters? (Select multiple)",
        "choices": ["A) Moonshot OKRs", "B) Incremental OKRs", "C) Committed OKRs", "D) General OKRs"],
        "correct": ["A", "C"]
    },
    {
        "question": "What did John Doerr suggest as the maximum number of OKRs a team should focus on in any given quarter?",
        "choices": ["A) 1-2", "B) 3-5", "C) 6-10", "D) 10-15"],
        "correct": ["B"]
    },
    {
        "question": "What is one of the major pitfalls of linking OKRs directly to compensation?",
        "choices": ["A) It reduces innovation", "B) It increases burnout rates", "C) It encourages goal manipulation", "D) It decreases team collaboration"],
        "correct": ["C"]
    },
    {
        "question": "What’s the main difference between aspirational OKRs and committed OKRs?",
        "choices": ["A) Aspirational OKRs are for personal growth", "B) Aspirational OKRs are often harder to fully achieve", "C) Committed OKRs have no deadlines", "D) Committed OKRs are always aligned with financial metrics"],
        "correct": ["B"]
    },
    {
        "question": "Which behaviors do OKRs encourage in a team setting? (Select multiple)",
        "choices": ["A) Accountability", "B) Cross-functional collaboration", "C) Competition", "D) Focus on individual performance"],
        "correct": ["A", "B"]
    },
    {
        "question": "How can OKRs be adapted when circumstances change during a quarter?",
        "choices": ["A) They can be abandoned", "B) Key Results can be adjusted", "C) Objectives must be rewritten entirely", "D) OKRs cannot be changed mid-quarter"],
        "correct": ["B"]
    },
    {
        "question": "Why is it essential to limit the number of OKRs a team focuses on?",
        "choices": ["A) To ensure clarity and focus", "B) To reduce employee workload", "C) To avoid complex management", "D) To decrease project timelines"],
        "correct": ["A"]
    },
    {
        "question": "Which of the following are examples of well-defined Key Results? (Select multiple)",
        "choices": ["A) Increase sales by 15%", "B) Launch new product features by end of Q2", "C) Improve team morale", "D) Complete 100 customer interviews by end of quarter"],
        "correct": ["A", "B", "D"]
    },
    {
        "question": "What is one key practice for keeping OKRs on track?",
        "choices": ["A) Waiting until the end of the quarter for reviews", "B) Setting OKRs without a timeline", "C) Conducting frequent check-ins", "D) Setting broad Key Results"],
        "correct": ["C"]
    }
]



class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OKR Quiz")
        self.root.geometry("600x500")

        self.current_question_index = 0
        self.score = 0
        self.start_time = 0

        self.question_label = tk.Label(root, text="", wraplength=500, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.choices_label = tk.Label(root, text="", wraplength=500, font=("Arial", 12))
        self.choices_label.pack(pady=10)

        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(root, textvariable=self.answer_var, font=("Arial", 14))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer, font=("Arial", 14))
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 12))
        self.score_label.pack(pady=10)

        self.start_time = time.time()
        self.show_question()

    # Function to sanitize the user's input (removes spaces, commas, and capitalizes)
    def sanitize_input(self, user_input):
        return "".join(user_input.upper().split()).replace(",", "")

    # Function to show the next question
    def show_question(self):
        if self.current_question_index < len(quiz_data):
            question_data = quiz_data[self.current_question_index]
            self.question_label.config(text=question_data["question"])
            choices_text = "\n".join(question_data["choices"])
            self.choices_label.config(text=choices_text)
            self.answer_var.set("")
            self.result_label.config(text="")
            self.start_time = time.time()
        else:
            self.end_quiz()

    # Function to check if the user's answer is correct
    def check_answer(self, user_answer, correct_answer):
        return set(user_answer) == set(correct_answer)

    # Function to calculate score based on time taken
    def calculate_score(self, elapsed_time):
        base_score = 10000
        grace_period = 4  # 4 seconds of grace
        max_time = 20  # 20 seconds maximum time allowed
        deduction_rate = 10000 / (max_time - grace_period)  # Points per second deduction after grace period

        if elapsed_time <= grace_period:
            return base_score  # Full points if answered within grace period
        elif elapsed_time > max_time:
            return 0  # No points if time exceeds max time
        else:
            deduction = (elapsed_time - grace_period) * deduction_rate
            return max(0, base_score - deduction)  # Deduct points for time taken

    # Function to handle answer submission
    import tkinter as tk
    from tkinter import messagebox
    import time

    # Define the questions, choices, and correct answers
    quiz_data = [
        {
            "question": "What are the two core components of OKRs?",
            "choices": ["A) Objectives and Key Results", "B) Objectives and Key Metrics", "C) Outputs and Key Results",
                        "D) Operational Key Results"],
            "correct": ["A"]
        },
        {
            "question": "Which of the following are characteristics of effective Key Results? (Select multiple)",
            "choices": ["A) Specific", "B) Measurable", "C) Ambiguous", "D) Time-bound"],
            "correct": ["A", "B", "D"]
        },
        # Add more questions here as before
    ]

    class QuizApp:
        def __init__(self, root):
            self.root = root
            self.root.title("OKR Quiz")
            self.root.geometry("600x500")

            self.current_question_index = 0
            self.score = 0
            self.start_time = 0

            self.question_label = tk.Label(root, text="", wraplength=500, font=("Arial", 14))
            self.question_label.pack(pady=20)

            self.choices_label = tk.Label(root, text="", wraplength=500, font=("Arial", 12))
            self.choices_label.pack(pady=10)

            self.answer_var = tk.StringVar()
            self.answer_entry = tk.Entry(root, textvariable=self.answer_var, font=("Arial", 14))
            self.answer_entry.pack(pady=10)

            self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer, font=("Arial", 14))
            self.submit_button.pack(pady=10)

            self.result_label = tk.Label(root, text="", font=("Arial", 12))
            self.result_label.pack(pady=10)

            self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 12))
            self.score_label.pack(pady=10)

            self.start_time = time.time()
            self.show_question()

        # Function to sanitize the user's input (removes spaces, commas, and capitalizes)
        def sanitize_input(self, user_input):
            return "".join(user_input.upper().split()).replace(",", "")

        # Function to show the next question
        def show_question(self):
            if self.current_question_index < len(quiz_data):
                question_data = quiz_data[self.current_question_index]
                self.question_label.config(text=question_data["question"])
                choices_text = "\n".join(question_data["choices"])
                self.choices_label.config(text=choices_text)
                self.answer_var.set("")
                self.result_label.config(text="")
                self.start_time = time.time()
            else:
                self.end_quiz()

        # Function to check if the user's answer is correct
        def check_answer(self, user_answer, correct_answer):
            return set(user_answer) == set(correct_answer)

        # Function to calculate score based on time taken
        def calculate_score(self, elapsed_time):
            base_score = 10000
            grace_period = 4  # 4 seconds of grace
            max_time = 20  # 20 seconds maximum time allowed
            deduction_rate = 10000 / (max_time - grace_period)  # Points per second deduction after grace period

            if elapsed_time <= grace_period:
                return base_score  # Full points if answered within grace period
            elif elapsed_time > max_time:
                return 0  # No points if time exceeds max time
            else:
                deduction = (elapsed_time - grace_period) * deduction_rate
                return max(0, base_score - deduction)  # Deduct points for time taken

        # Function to handle answer submission
        def submit_answer(self):
            elapsed_time = time.time() - self.start_time
            sanitized_answer = self.sanitize_input(self.answer_var.get())
            user_answer_list = list(sanitized_answer)

            correct_answer = quiz_data[self.current_question_index]["correct"]
            if self.check_answer(user_answer_list, correct_answer):
                self.result_label.config(text="Correct!", fg="green")
                score = self.calculate_score(elapsed_time)
            else:
                self.result_label.config(text=f"Wrong. Correct answer(s): {', '.join(correct_answer)}", fg="red")
                score = 0

            self.score += score
            self.score_label.config(text=f"Score: {int(self.score)}")

            self.current_question_index += 1
            self.root.after(2000, self.show_question)  # Show next question after 2 seconds

        # Function to end the quiz
        def end_quiz(self):
            messagebox.showinfo("Quiz Complete",
                                f"Quiz complete! Your final score is {int(self.score)} out of {10000 * len(quiz_data)}.")
            self.root.quit()

    # Main loop for running the GUI application
    if __name__ == "__main__":
        root = tk.Tk()
        app = QuizApp(root)
        root.mainloop()