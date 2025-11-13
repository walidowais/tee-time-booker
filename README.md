# Tee Time Booking Automation

This automation script books tee times on the ForeuP software booking system. It can run locally or as a cloud-based web service triggered by cron jobs.

## Features

- Automatically logs in with provided credentials
- Chooses a date 5 days from the current date
- Finds the first available tee time before 10:30 AM with minimum 2 players
- Configures booking for maximum players and no carts
- Completes the booking automatically
- **NEW**: Web server for cloud deployment and cron job triggers

## Setup

1. Run the setup script to install dependencies:
   ```bash
   ./setup.sh
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Usage Options

### Option 1: Local Execution
Run the booking automation directly:
```bash
python tee_time_booker.py
```

### Option 2: Web Server + Cron Jobs (Recommended)
For automated daily bookings:

1. **Start the web server locally**:
   ```bash
   python web_server.py
   ```

2. **Test the web endpoints**:
   ```bash
   python test_server.py
   ```

3. **Deploy to cloud and set up cron job**:
   - See [CRON_SETUP.md](CRON_SETUP.md) for detailed instructions
   - Deploy to Replit, Heroku, or similar platform
   - Use cron-job.org to trigger daily bookings

### Web Server Endpoints

- `GET /` - Service status and information
- `GET /run` - Trigger tee time booking
- `GET /run?test=true` - Test mode (doesn't actually book)
- `GET /status` - Check last booking result
- `GET /health` - Health check

## Configuration

You can modify the following settings in `tee_time_booker.py`:

- **Credentials**: Update `self.username` and `self.password` in the `__init__` method
- **Headless mode**: Change `headless=False` to `headless=True` to run without opening a browser window
- **Time cutoff**: Modify `cutoff_minutes` to change the latest acceptable tee time
- **Minimum players**: Adjust the player count check in `find_and_book_tee_time`

## Troubleshooting

The script includes several debugging features:

- **Screenshots**: Automatically takes screenshots when errors occur
- **Logging**: Detailed console output shows what the script is doing
- **Multiple selectors**: Uses fallback selectors in case the website structure changes

Common debug files created:
- `debug_rate_selection.png` - Screenshot when rate selection fails
- `debug_date_selection.png` - Screenshot when date selection fails
- `debug_tee_times.png` - Screenshot of available tee times
- `debug_book_button.png` - Screenshot when booking button not found
- `debug_booking_error.png` - Screenshot when booking fails
- `debug_error.png` - General error screenshot

## Technical Details

- **Framework**: Uses Playwright for web automation
- **Browser**: Chromium (Chrome-based)
- **Language**: Python 3.7+
- **Async**: Uses async/await for better performance

## Important Notes

1. **Rate Limiting**: Be respectful of the website - don't run this too frequently
2. **Website Changes**: If the website structure changes, you may need to update the selectors
3. **Manual Verification**: Always verify that bookings were successful
4. **Terms of Service**: Make sure using automation complies with the website's terms of service

## Customization

The script is designed to be easily customizable. Key areas for modification:

### Changing Login Credentials
```python
def __init__(self):
    self.username = "your_email@example.com"
    self.password = "your_password"
```

### Changing Time Preferences
```python
cutoff_minutes = 11 * 60 + 0  # Change to 11:00 AM instead of 10:30 AM
```

### Changing Date Range
```python
def get_target_date(self):
    target_date = datetime.now() + timedelta(days=7)  # 7 days instead of 14
    return target_date
```

### Adding Error Notifications
You could extend the script to send notifications (email, SMS, etc.) when bookings succeed or fail.

## Dependencies

- `playwright` - Web automation framework
- `python-dateutil` - Date manipulation utilities

## License

This is a utility script for personal use. Please ensure compliance with the booking website's terms of service.
