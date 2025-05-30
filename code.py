import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import random
import datetime
import math
import os
import json
import webbrowser

class CodingPlatform:
    def __init__(self, root):
        self.root = root
        self.root.title("PyCoder - Learn to Code")
        self.root.geometry("1000x700")
        
        # Set theme colors
        self.bg_color = "#f0f0f0"
        self.sidebar_color = "#2c3e50"
        self.button_color = "#3498db"
        self.text_bg = "#ffffff"
        
        self.create_widgets()
        self.load_problems()
        self.current_problem = None
        
    def create_widgets(self):
        # Create main frames
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=200)
        self.sidebar.pack(side="left", fill="y")
        
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        # Sidebar widgets
        tk.Label(self.sidebar, text="PyCoder", bg=self.sidebar_color, 
                fg="white", font=("Arial", 16, "bold")).pack(pady=20)
        
        buttons = [
            ("Problems", self.show_problems),
            ("Code Editor", self.show_editor),
            ("Run Code", self.run_code),
            ("Save Code", self.save_code),
            ("Load Code", self.load_code),
            ("Math Help", self.show_math_help),
            ("Resources", self.open_resources),
            ("Daily Challenge", self.daily_challenge)
        ]
        
        for text, command in buttons:
            btn = tk.Button(self.sidebar, text=text, bg=self.button_color, 
                           fg="white", command=command, width=15)
            btn.pack(pady=5, padx=10)
            
        # Time and date display
        self.time_label = tk.Label(self.sidebar, bg=self.sidebar_color, fg="white")
        self.time_label.pack(side="bottom", pady=10)
        self.update_time()
        
        # Main area - problem view
        self.problem_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.problem_title = tk.Label(self.problem_frame, bg=self.bg_color, 
                                     font=("Arial", 14, "bold"))
        self.problem_title.pack(pady=10)
        
        self.problem_text = scrolledtext.ScrolledText(
            self.problem_frame, wrap=tk.WORD, width=80, height=10, 
            bg=self.text_bg, font=("Arial", 12))
        self.problem_text.pack(pady=10, padx=20)
        
        self.difficulty_label = tk.Label(self.problem_frame, bg=self.bg_color)
        self.difficulty_label.pack()
        
        # Editor area
        self.editor_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.code_editor = scrolledtext.ScrolledText(
            self.editor_frame, wrap=tk.WORD, width=80, height=20, 
            bg=self.text_bg, font=("Courier", 12))
        self.code_editor.pack(pady=10, padx=20)
        
        # Output area
        self.output_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.output_label = tk.Label(self.output_frame, text="Output:", 
                                    bg=self.bg_color, font=("Arial", 12))
        self.output_label.pack()
        self.output_text = scrolledtext.ScrolledText(
            self.output_frame, wrap=tk.WORD, width=80, height=10, 
            bg="#2d2d2d", fg="#ffffff", font=("Courier", 12))
        self.output_text.pack(pady=10, padx=20)
        
        # Show problem view by default
        self.show_problems()
        
    def update_time(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S\n%A, %B %d")
        self.time_label.config(text=time_str)
        self.root.after(1000, self.update_time)
        
    def load_problems(self):
        # Load problems from a JSON file if it exists
        if os.path.exists("problems.json"):
            with open("problems.json", "r") as f:
                self.problems = json.load(f)
        else:
            # Default problems
            self.problems = [
                {
                    "title": "Sum of Two Numbers",
                    "description": "Write a function that takes two numbers as input and returns their sum.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "5, 7", "output": "12"},
                        {"input": "-3, 10", "output": "7"},
                        {"input": "0, 0", "output": "0"}
                    ]
                },
                {
                    "title": "Factorial Calculator",
                    "description": "Write a function that calculates the factorial of a given number (n!).",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "5", "output": "120"},
                        {"input": "0", "output": "1"},
                        {"input": "7", "output": "5040"}
                    ]
                },
                {
                    "title": "Prime Number Check",
                    "description": "Write a function that checks if a number is prime.",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "7", "output": "True"},
                        {"input": "4", "output": "False"},
                        {"input": "13", "output": "True"}
                    ]
                }
            ]
            self.save_problems()
            
    def save_problems(self):
        with open("problems.json", "w") as f:
            json.dump(self.problems, f, indent=4)
            
    def show_problems(self):
        self.hide_all_frames()
        self.problem_frame.pack(fill="both", expand=True)
        
        # Clear previous content
        self.problem_title.config(text="Coding Problems")
        self.problem_text.delete(1.0, tk.END)
        
        # Display list of problems
        self.problem_text.insert(tk.END, "Available Problems:\n\n")
        for i, problem in enumerate(self.problems, 1):
            self.problem_text.insert(tk.END, f"{i}. {problem['title']} ({problem['difficulty']})\n")
            
        # Add button to select a random problem
        tk.Button(self.problem_frame, text="Random Problem", bg=self.button_color,
                 fg="white", command=self.select_random_problem).pack(pady=10)
        
    def select_random_problem(self):
        self.current_problem = random.choice(self.problems)
        self.display_problem(self.current_problem)
        
    def display_problem(self, problem):
        self.hide_all_frames()
        self.problem_frame.pack(fill="both", expand=True)
        
        self.problem_title.config(text=problem["title"])
        self.problem_text.delete(1.0, tk.END)
        self.problem_text.insert(tk.END, problem["description"])
        
        self.difficulty_label.config(text=f"Difficulty: {problem['difficulty']}")
        
        # Add button to start coding this problem
        tk.Button(self.problem_frame, text="Start Coding", bg=self.button_color,
                 fg="white", command=self.show_editor).pack(pady=10)
        
    def show_editor(self):
        self.hide_all_frames()
        self.editor_frame.pack(fill="both", expand=True)
        self.output_frame.pack(fill="both", expand=True)
        
        # Insert default code if editor is empty
        if not self.code_editor.get(1.0, tk.END).strip():
            self.code_editor.delete(1.0, tk.END)
            self.code_editor.insert(tk.END, "# Write your code here\n")
            if self.current_problem:
                self.code_editor.insert(tk.END, f"\n# Problem: {self.current_problem['title']}\n")
                
    def run_code(self):
        self.show_editor()  # Make sure editor is visible
        
        code = self.code_editor.get(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        
        try:
            # Create a local namespace for execution
            local_vars = {}
            
            # Execute the code
            exec(code, globals(), local_vars)
            
            # If there's a function, try to test it
            if self.current_problem and "test_cases" in self.current_problem:
                self.output_text.insert(tk.END, "Running test cases...\n\n")
                
                # Find the first function defined in the code
                functions = [name for name, obj in local_vars.items() 
                           if callable(obj) and not name.startswith('_')]
                
                if functions:
                    test_func = local_vars[functions[0]]
                    passed = 0
                    
                    for case in self.current_problem["test_cases"]:
                        try:
                            # Evaluate the input (this is a simplified approach)
                            inputs = [eval(arg.strip()) for arg in case["input"].split(",")]
                            expected = case["output"]
                            
                            # Call the function with the inputs
                            result = str(test_func(*inputs))
                            
                            if result == expected:
                                self.output_text.insert(tk.END, 
                                    f"✓ Passed: {case['input']} -> {result}\n")
                                passed += 1
                            else:
                                self.output_text.insert(tk.END, 
                                    f"✗ Failed: {case['input']} -> Expected {expected}, got {result}\n")
                        except Exception as e:
                            self.output_text.insert(tk.END, 
                                f"! Error with test case {case['input']}: {str(e)}\n")
                    
                    self.output_text.insert(tk.END, 
                        f"\nTest results: {passed}/{len(self.current_problem['test_cases'])} passed\n")
                else:
                    self.output_text.insert(tk.END, "No function found to test.\n")
            else:
                self.output_text.insert(tk.END, "Code executed successfully (no tests run).\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
            
    def save_code(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        
        if file_path:
            with open(file_path, "w") as f:
                code = self.code_editor.get(1.0, tk.END)
                f.write(code)
                
    def load_code(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        
        if file_path:
            with open(file_path, "r") as f:
                code = f.read()
                self.code_editor.delete(1.0, tk.END)
                self.code_editor.insert(tk.END, code)
                
    def show_math_help(self):
        self.hide_all_frames()
        self.problem_frame.pack(fill="both", expand=True)
        
        self.problem_title.config(text="Math Help")
        self.problem_text.delete(1.0, tk.END)
        
        math_functions = [
            "math.sqrt(x) - Square root",
            "math.pow(x, y) - x raised to power y",
            "math.sin(x) - Sine of x radians",
            "math.cos(x) - Cosine of x radians",
            "math.tan(x) - Tangent of x radians",
            "math.pi - The mathematical constant π",
            "math.e - The mathematical constant e",
            "math.factorial(x) - Factorial of x",
            "math.gcd(a, b) - Greatest common divisor",
            "math.log(x, base) - Logarithm of x to the given base"
        ]
        
        self.problem_text.insert(tk.END, "Common Math Functions:\n\n")
        for func in math_functions:
            self.problem_text.insert(tk.END, f"• {func}\n")
            
    def open_resources(self):
        resources = {
            "Python Documentation": "https://docs.python.org/3/",
            "W3Schools Python": "https://www.w3schools.com/python/",
            "Real Python": "https://realpython.com/",
            "GeeksforGeeks Python": "https://www.geeksforgeeks.org/python-programming-language/"
        }
        
        self.hide_all_frames()
        self.problem_frame.pack(fill="both", expand=True)
        
        self.problem_title.config(text="Learning Resources")
        self.problem_text.delete(1.0, tk.END)
        
        self.problem_text.insert(tk.END, "Click a link to open in browser:\n\n")
        for name, url in resources.items():
            link = tk.Label(self.problem_text, text=name, fg="blue", cursor="hand2")
            link.bind("<Button-1>", lambda e, u=url: webbrowser.open_new(u))
            self.problem_text.window_create(tk.END, window=link)
            self.problem_text.insert(tk.END, "\n")
            
    def daily_challenge(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        random.seed(today)  # Same challenge for the whole day
        
        challenges = [
            {
                "title": "Daily Math Challenge",
                "description": f"Calculate the sum of all numbers from 1 to {random.randint(10, 100)}.",
                "difficulty": "Easy"
            },
            {
                "title": "Daily Algorithm Challenge",
                "description": f"Find all prime numbers up to {random.randint(20, 50)}.",
                "difficulty": "Medium"
            },
            {
                "title": "Daily String Challenge",
                "description": "Reverse a string without using built-in reverse functions.",
                "difficulty": "Easy"
            }
        ]
        
        challenge = random.choice(challenges)
        self.current_problem = {
            **challenge,
            "test_cases": []  # No predefined test cases for daily challenge
        }
        self.display_problem(self.current_problem)
        
    def hide_all_frames(self):
        self.problem_frame.pack_forget()
        self.editor_frame.pack_forget()
        self.output_frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = CodingPlatform(root)
    root.mainloop()