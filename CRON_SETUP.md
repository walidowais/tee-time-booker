# Cron Job Setup Guide for Tee Time Booking Automation

This guide explains how to set up automated tee time booking using a free cron job service.

## Option A: Replit + cron-job.org (Recommended - Free)

### Step 1: Deploy to Replit

1. **Create a new Repl**:
   - Go to [replit.com](https://replit.com)
   - Click "Create Repl"
   - Choose "Import from GitHub" and paste your repository URL
   - Or create a new Python Repl and upload these files

2. **Configure the Repl**:
   - The `replit.toml` file is already configured
   - Replit will automatically install dependencies
   - The web server will start on port 5000

3. **Test your deployment**:
   - Run the Repl
   - Your app will be available at `https://<your-repl-name>.<username>.repl.co`
   - Test endpoints:
     - `GET /` - Home page with service info
     - `GET /health` - Health check
     - `GET /run?test=true` - Test mode (doesn't actually book)
     - `GET /run` - Trigger actual booking

### Step 2: Set up cron-job.org

1. **Create account**:
   - Go to [cron-job.org](https://cron-job.org)
   - Sign up for free account (up to 3 cron jobs)

2. **Create cron job**:
   - Click "Cronjobs" → "Create cronjob"
   - **Title**: "Tee Time Booking - 6:59 AM Daily"
   - **URL**: `https://<your-repl-name>.<username>.repl.co/run`
   - **Schedule**:
     - Minutes: `59`
     - Hours: `6` (or your preferred time)
     - Days: `*` (every day)
     - Months: `*`
     - Weekdays: `*`
   - **Timezone**: Select your local timezone
   - **Enabled**: ✅

3. **Configure notifications** (optional):
   - Enable email notifications for failures
   - Set up success notifications if desired

### Step 3: Monitor and Test

1. **Test the cron job**:
   - Use the "Execute now" button in cron-job.org
   - Check the execution logs
   - Monitor your Repl's logs

2. **Check booking status**:
   - Visit `https://<your-repl-name>.<username>.repl.co/status`
   - This shows the last booking attempt and result

## Option B: Alternative Cloud Platforms

### Heroku (Free tier discontinued, but still an option)
### Railway.app (Free tier available)
### Render.com (Free tier available)

All these platforms can use the same `Dockerfile` for deployment.

## Important Configuration

### Environment Variables (if needed)
You can set these in your cloud platform:

```bash
BOOKING_USERNAME=mukhtar91@gmail.com
BOOKING_PASSWORD=your_password
BOOKING_URL=https://foreupsoftware.com/index.php/booking/20954#/login
DAYS_ADVANCE=5
TIME_CUTOFF=10:30
MIN_PLAYERS=2
```

### Updating Credentials
If you need to change login credentials, you have several options:

1. **Edit the code directly** (current approach)
2. **Use environment variables** (more secure)
3. **Create a config endpoint** to update credentials via web interface

## Troubleshooting

### Common Issues:

1. **Repl goes to sleep**:
   - Free Repls sleep after inactivity
   - The cron job will wake it up automatically
   - Consider upgrading to Replit Core for always-on hosting

2. **Browser automation fails**:
   - Check the logs in your Repl
   - Playwright might need additional setup in cloud environments
   - Screenshots are saved for debugging (when possible)

3. **Cron job fails**:
   - Check cron-job.org execution logs
   - Verify your Repl URL is accessible
   - Test the `/health` endpoint

### Debug Endpoints:

- `GET /` - Service status and info
- `GET /health` - Health check
- `GET /status` - Last booking result
- `GET /run?test=true` - Test mode (safe testing)

## Security Considerations

1. **Credentials**: Consider using environment variables instead of hardcoded credentials
2. **Rate limiting**: The service includes basic rate limiting to prevent multiple simultaneous bookings
3. **HTTPS**: Always use HTTPS URLs for cron jobs
4. **Logs**: Monitor logs for any suspicious activity

## Cost Breakdown

- **Replit**: Free tier sufficient for this use case
- **cron-job.org**: Free (up to 3 cron jobs)
- **Total**: $0/month

## Advanced Features You Can Add

1. **Slack/Discord notifications** when bookings succeed/fail
2. **Multiple booking profiles** for different users
3. **Web interface** to configure booking preferences
4. **Backup booking times** if first choice isn't available
5. **Holiday scheduling** to skip bookings on certain dates

## Sample Cron Job URLs

```bash
# Basic booking
https://your-repl.username.repl.co/run

# Test mode (doesn't actually book)
https://your-repl.username.repl.co/run?test=true

# Health check
https://your-repl.username.repl.co/health
```

## Monitoring Your Setup

1. **Daily checks**: Visit the `/status` endpoint to see results
2. **Email notifications**: Configure cron-job.org to email you on failures
3. **Logs**: Check your Repl's logs for detailed execution information

This setup gives you a completely automated, cloud-based tee time booking system that runs every morning at 6:59 AM and attempts to book your preferred tee time!
