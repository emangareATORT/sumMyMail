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
import sys
from openai import OpenAI


class EmailSummarizerApp:
    # Model configuration
    MODEL_NAME = "gpt-4o"
    
    def __init__(self, root):
        self.root = root
        self.root.title("sumMyMail - Email Thread Summarizer")
        self.root.geometry("900x700")
        
        # Load API key
        self.api_key = self.load_api_key()
        if not self.api_key:
            messagebox.showerror(
                "Configuration Error",
                "API key not found. Please create a config.ini file with your OpenAI API key.\n"
                "See config.ini.example for the format."
            )
            sys.exit(1)
        
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
            
            # Display results
            self.display_results(result)
            
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
            temperature=0.3,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
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
