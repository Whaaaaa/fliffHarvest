# Automated Fliff Coin Claimer

This project automates the process of claiming Fliff coins on the sports betting site [Fliff](https://sports.getfliff.com/shop). The script, using Selenium and `undetected_chromedriver`, logs in, navigates to the coin claiming section, and schedules regular claims as specified.

## Features

- Automatically logs into the Fliff website and claims daily coins.
- Uses undetected Chrome driver to reduce detection risk.
- Schedules the next claim based on the availability countdown.
- Runs continuously and updates the schedule dynamically based on the availability of coins.

## Requirements

This project requires:
- Python 3.7+
- Google Chrome (latest version recommended)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/fliff-coin-claimer.git
   cd fliff-coin-claimer
   ```

2. **Set Up Dependencies**:
   Install all required packages by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**:
   Create a `config.ini` file in the project directory with your login credentials and Chrome user data directory:
   ```ini
   [Credentials]
   email = your_email@gmail.com
   password = your_password

   [Paths]
   chrome_user_data_dir = /path/to/chrome/user/data
   ```
   - Replace `your_email@gmail.com` and `your_password` with your actual Fliff account email and password.
   - Set `chrome_user_data_dir` to the path of your Chrome profile data directory if you’re using a specific Chrome profile.

## Usage

Run the script with:
```bash
python fliff_coin_claimer.py
```

The script will:
1. Open Chrome in a non-detectable mode.
2. Attempt to log into the Fliff website.
3. Check for coin availability and claim if possible.
4. Schedule the next claim based on the countdown.

## Schedule and Automation

- The script runs in a loop using the `schedule` library, checking every minute.
- If a claim is available, it will claim it and reschedule based on a 121-minute interval or the site’s availability countdown.

## Troubleshooting

- Ensure Chrome is updated to the latest version to avoid compatibility issues.
- Adjust the path in `chrome_user_data_dir` if you encounter errors related to Chrome profiles.

## License

This project is open-source and free to use.
