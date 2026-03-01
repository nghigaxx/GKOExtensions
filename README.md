# GKOExtensions
Extensions for certain GKO activities
This project uses Python + Selenium to automate activities in GoKickOff.

📋 Requirements

Before running the script, make sure you have the following installed:

1️⃣ Python

Install Python 3.9+

Download from: https://www.python.org/downloads/

Verify installation:

python --version

2️⃣ Selenium

Install Selenium using pip:

pip install selenium

3️⃣ Chrome Browser

Make sure Google Chrome is installed on your system.

4️⃣ ChromeDriver (Important ⚠)

You must:

Download the latest ChromeDriver version

Make sure it matches your Chrome browser version

Place the chromedriver.exe (or chromedriver on Mac/Linux) in the same directory as the Python script

Download here: https://chromedriver.chromium.org/downloads

Verify Chrome version:

chrome://settings/help

🔐 Credentials Setup

You must create a file named:

credentials.txt

Place it in the same directory as the script.

Format: your_gokickoff_username your_gokickoff_password

Line 1 → GoKickOff username

Line 2 → GoKickOff password

No extra spaces

No quotes

📂 Project Structure Example project-folder/ │ ├── market.py ├── chromedriver.exe ├── credentials.txt └── README.md

▶ Running the Script

From the project directory:

python main.py

⚠ Notes

ChromeDriver must match your Chrome version.

Do not share your credentials.txt.

You may need to adjust timeouts depending on your internet speed.

If Chrome opens and closes immediately, check driver compatibility.

Scout.py need premium activated

🛠 Troubleshooting

Error: session not created → ChromeDriver version does not match Chrome.

Error: cannot find chromedriver → Make sure it is in the same directory as the script.

Logging system

Config file for filters

Auto ChromeDriver detection
