#!/usr/bin/env python3
"""
sumMyMail - Email Thread Summarizer using GPT-4o
Processes long email threads and extracts:
- Concise summary
- Action items for Eduardo Mangarelli
- List of participants
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import configparser
import os
import re
from openai import OpenAI


class ActionItemsWindow:
    """Window to display action items in a To-Do list format"""
    
    def __init__(self, parent, action_items):
        self.window = tk.Toplevel(parent)
        self.window.title("Action Items To-Do List")
        self.window.geometry("600x500")
        
        # Title
        title_label = tk.Label(
            self.window,
            text="📋 Action Items for Eduardo Mangarelli",
            font=("Arial", 14, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Instructions
        instructions = tk.Label(
            self.window,
            text="Check off items as you complete them",
            font=("Arial", 9),
            fg="gray"
        )
        instructions.pack()
        
        # Create scrolled frame for checkboxes
        canvas_frame = tk.Frame(self.window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Parse and display action items
        self.checkboxes = []
        self.action_items = action_items
        
        if action_items and len(action_items) > 0:
            for idx, item in enumerate(action_items, 1):
                var = tk.BooleanVar()
                checkbox = tk.Checkbutton(
                    scrollable_frame,
                    text=item,
                    variable=var,
                    font=("Arial", 11),
                    wraplength=550,
                    anchor="w",
                    justify="left",
                    command=lambda v=var, c=None: self.on_check(v, c)
                )
                checkbox.pack(fill=tk.X, padx=20, pady=5, anchor="w")
                self.checkboxes.append((checkbox, var))
                # Store the checkbox reference in the lambda
                checkbox.config(command=lambda v=var, c=checkbox: self.on_check(v, c))
        else:
            no_items_label = tk.Label(
                scrollable_frame,
                text="No specific action items identified",
                font=("Arial", 11),
                fg="gray"
            )
            no_items_label.pack(pady=20)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        close_button = tk.Button(
            self.window,
            text="Close",
            command=self.window.destroy,
            font=("Arial", 10),
            padx=20,
            pady=5
        )
        close_button.pack(pady=10)
    
    def on_check(self, var, checkbox):
        """Handle checkbox state changes"""
        if var.get():
            # Item is checked - show strikethrough effect
            checkbox.config(fg="gray")
        else:
            # Item is unchecked - remove strikethrough effect
            checkbox.config(fg="black")


class EmailSummarizerApp:
    # Model configuration
    MODEL_NAME = "gpt-4o"
    TEMPERATURE = 0.3
    MAX_TOKENS = 1000
    
    def __init__(self, root):
        self.root = root
        self.root.title("sumMyMail - Email Thread Summarizer")
        self.root.geometry("900x700")
        
        # Store action items for To-Do window
        self.current_action_items = []
        
        # Load API key
        self.api_key = self.load_api_key()
        if not self.api_key:
            messagebox.showerror(
                "Configuration Error",
                "API key not found. Please create a config.ini file with your OpenAI API key.\n"
                "See config.ini.example for the format."
            )
            self.root.destroy()
            return
        
        self.client = OpenAI(api_key=self.api_key)
        self.setup_ui()
    
    def load_api_key(self):
        """Load OpenAI API key from config.ini"""
        config = configparser.ConfigParser()
        config_file = 'config.ini'
        
        if os.path.exists(config_file):
            config.read(config_file)
            if 'OpenAI' in config and 'api_key' in config['OpenAI']:
                api_key = config['OpenAI']['api_key']
                if api_key and api_key != 'your_openai_api_key_here':
                    return api_key
        
        # Try environment variable as fallback
        return os.environ.get('OPENAI_API_KEY')
    
    def setup_ui(self):
        """Create the user interface"""
        # Title label
        title_label = tk.Label(
            self.root,
            text="Email Thread Summarizer",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Paste your email thread below and click 'Process'",
            font=("Arial", 10)
        )
        instructions.pack()
        
        # Input frame
        input_frame = tk.LabelFrame(self.root, text="Email Thread Input", padx=10, pady=10)
        input_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            width=80,
            height=10,
            font=("Arial", 10)
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Process button
        self.process_button = tk.Button(
            self.root,
            text="Process Email Thread",
            command=self.process_email,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        self.process_button.pack(pady=10)
        
        # Open To-Do button (initially hidden)
        self.todo_button = tk.Button(
            self.root,
            text="📋 Open Action Items To-Do List",
            command=self.open_todo_window,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8
        )
        # Don't pack it yet - will be shown after processing
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=5)
        
        # Output frame
        output_frame = tk.LabelFrame(self.root, text="Analysis Results", padx=10, pady=10)
        output_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
    
    def process_email(self):
        """Process the email thread using GPT-4o"""
        email_text = self.input_text.get("1.0", tk.END).strip()
        
        if not email_text:
            messagebox.showwarning("Input Required", "Please paste an email thread to process.")
            return
        
        # Disable button and show progress
        self.process_button.config(state=tk.DISABLED)
        self.progress.start(10)
        self.root.update()
        
        try:
            # Call GPT-4o API
            result = self.analyze_email_thread(email_text)
            
            # Extract action items
            self.current_action_items = self.extract_action_items(result)
            
            # Display results
            self.display_results(result)
            
            # Show To-Do button if there are action items
            if self.current_action_items:
                self.todo_button.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            # Re-enable button and stop progress
            self.process_button.config(state=tk.NORMAL)
            self.progress.stop()
    
    def analyze_email_thread(self, email_text):
        """Analyze email thread using GPT-4o"""
        system_prompt = """You are an expert email analyst. Analyze the provided email thread and extract:
1. A concise summary of the email thread (2-3 sentences)
2. Specific action items for Eduardo Mangarelli (if any are mentioned or implied)
3. A list of all participants mentioned in the thread

Format your response exactly as follows:
SUMMARY:
[Your concise summary here]

ACTION ITEMS FOR EDUARDO MANGARELLI:
- [Action item 1]
- [Action item 2]
(or "No specific action items identified" if none)

PARTICIPANTS:
- [Participant 1]
- [Participant 2]
"""
        
        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Email thread:\n\n{email_text}"}
            ],
            temperature=self.TEMPERATURE,
            max_tokens=self.MAX_TOKENS
        )
        
        return response.choices[0].message.content
    
    def extract_action_items(self, results):
        """Extract action items from the GPT-4o response"""
        action_items = []
        
        # Find the ACTION ITEMS section
        lines = results.split('\n')
        in_action_section = False
        
        for line in lines:
            line = line.strip()
            
            # Check if we're entering the action items section
            if 'ACTION ITEMS FOR EDUARDO MANGARELLI' in line.upper():
                in_action_section = True
                continue
            
            # Check if we're leaving the action items section
            if in_action_section and line.startswith('PARTICIPANTS'):
                break
            
            # Extract action items (lines starting with -)
            if in_action_section and line.startswith('-'):
                item = line[1:].strip()  # Remove the dash and whitespace
                # Skip the "No specific action items" message
                if item and 'no specific action items' not in item.lower():
                    action_items.append(item)
        
        return action_items
    
    def open_todo_window(self):
        """Open the To-Do list window with action items"""
        ActionItemsWindow(self.root, self.current_action_items)
    
    def display_results(self, results):
        """Display the analysis results"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", results)
        self.output_text.config(state=tk.DISABLED)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = EmailSummarizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
