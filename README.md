# Auto Feedback Script

This repository contains a Python script for automating the feedback process on a web application. The script uses Selenium WebDriver to interact with the web page, submit feedback for students, and handle pagination to process multiple pages of students.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Script Details](#script-details)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contact](#contact)

## Overview

The Auto Feedback Script automates the process of providing feedback for students in a web application. It handles login, feedback submission, and pagination to ensure that feedback is given to all students across multiple pages.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.12 or later
- Google Chrome Browser
- ChromeDriver that matches your version of Chrome

You also need the following Python libraries:

- `selenium`

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/auto-feedback-script.git
   cd auto-feedback-script
   ```

2. **Install Python Libraries**

   Install the required libraries using pip:

   ```bash
   pip install selenium
   ```

3. **Download ChromeDriver**

   Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and ensure it matches your version of Chrome. Place the `chromedriver` executable in a directory that is included in your system's PATH.

## Usage

1. **Edit the Script**

   Open the script file `Auto_Feedback.py` and update the following variables with your specific details:

   ```python
   TUTOR_ID = "your_tutor_id"
   TUTOR_PASSWORD = "your_tutor_password"
   ```

2. **Run the Script**

   Execute the script from the command line:

   ```bash
   python Auto_Feedback.py
   ```

   The script will open a Chrome browser window, navigate to the login page, log in, and start processing feedback for students.

## Script Details

### Main Functions

- **`give_feedback(driver, comment)`**: Automates the feedback submission process, including selecting star ratings and comments.
- **`get_number_of_students(driver)`**: Retrieves the number of students displayed on the current page.
- **`main()`**: The main function that initializes the WebDriver, handles login, navigates to the feedback page, processes feedback for students, and handles pagination.

### Error Handling

The script includes error handling for various scenarios such as click interception, element visibility issues, and pagination problems. Screenshots are taken if errors occur during feedback submission.

## Troubleshooting

- **Element Click Interception**: If you encounter issues with element clicks being intercepted, ensure that no other elements (such as toasts or modals) are blocking the view. The script includes retry logic to handle such cases.
- **No More Pages**: If the script reports "No more pages or error navigating to the next page," verify that the pagination buttons are visible and not obstructed by other elements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or issues, please contact:

- **Author**: [A.Mesbah](https://github.com/AMesbah-Lamp)
- **Email**: ahmed.320230033@ejust.edu.eg
