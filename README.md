# sumMyMail

Python Windows application that processes long email threads using GPT-4o. The user pastes the thread text, and the app outputs:
- (a) A concise summary
- (b) Action items for Eduardo Mangarelli
- (c) A list of participants

Designed for quick insight extraction and follow-up management.

## Features

- **User-Friendly GUI**: Simple Windows interface built with tkinter
- **GPT-4o Integration**: Leverages OpenAI's GPT-4o model for intelligent text analysis
- **Quick Processing**: Paste email threads and get instant analysis
- **Three-Part Output**:
  - Concise summary of the email thread
  - Specific action items for Eduardo Mangarelli
  - Complete list of all participants

## Requirements

- Python 3.8 or higher
- OpenAI API key
- Windows OS (tested on Windows 10/11)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/emangareATORT/sumMyMail.git
cd sumMyMail
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your OpenAI API key:
   - Copy `config.ini.example` to `config.ini`
   - Edit `config.ini` and replace `your_openai_api_key_here` with your actual OpenAI API key

```bash
copy config.ini.example config.ini
# Edit config.ini with your API key
```

Alternatively, you can set the API key as an environment variable:
```bash
set OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Run the application:
```bash
python sumMyMail.py
```

2. The GUI window will open with two main sections:
   - **Email Thread Input**: Paste your email thread here
   - **Analysis Results**: The processed output will appear here

3. Paste your email thread in the input area

4. Click the "Process Email Thread" button

5. Wait for the analysis to complete (progress bar will indicate processing)

6. Review the results in the output area:
   - Summary of the thread
   - Action items for Eduardo Mangarelli
   - List of participants

## Configuration

### API Key Setup

The application looks for your OpenAI API key in the following order:
1. `config.ini` file in the application directory
2. `OPENAI_API_KEY` environment variable

### config.ini Format

```ini
[OpenAI]
api_key = your_openai_api_key_here
```

**Important**: Never commit your `config.ini` file with a real API key to version control. The `.gitignore` file is configured to exclude this file.

## Example

### Input:
```
From: John Doe <john@example.com>
To: Eduardo Mangarelli <eduardo@example.com>, Jane Smith <jane@example.com>
Subject: Q4 Project Update

Hi Team,

I wanted to give you an update on the Q4 project. We're making good progress...

Eduardo, could you please review the budget proposal by Friday?

Best,
John

---

From: Jane Smith <jane@example.com>
...
```

### Output:
```
SUMMARY:
The email thread discusses Q4 project progress with a focus on budget review...

ACTION ITEMS FOR EDUARDO MANGARELLI:
- Review the budget proposal by Friday

PARTICIPANTS:
- John Doe
- Eduardo Mangarelli
- Jane Smith
```

## Troubleshooting

### "API key not found" error
- Ensure you've created a `config.ini` file with your API key
- Verify the API key is correct and active
- Check that the file is in the same directory as `sumMyMail.py`

### "Connection Error"
- Check your internet connection
- Verify your OpenAI API key has sufficient credits
- Ensure you're not behind a proxy that blocks OpenAI API

### GUI doesn't appear
- Ensure you're running on Windows with tkinter support
- Try reinstalling Python with tkinter enabled

## License

This project is provided as-is for personal use.

## Contributing

Feel free to open issues or submit pull requests for improvements.