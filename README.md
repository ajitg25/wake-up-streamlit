# ⏰ Keep My Streamlit Apps Awake

Automatically keep your Streamlit apps active and prevent them from going to sleep!

## 🎯 What This Does

This system automatically wakes up your Streamlit apps every hour to keep them active and responsive. No more waiting for sleeping apps to restart!

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────────┐
│  Streamlit UI   │ ───> │ websites.txt │ ───> │ GitHub Actions  │
│  (Add websites) │      │  (Storage)   │      │  (Cron Job)     │
└─────────────────┘      └──────────────┘      └─────────────────┘
                                                         │
                                                         ▼
                                                 ┌───────────────┐
                                                 │ Playwright    │
                                                 │ Wake-up Script│
                                                 └───────────────┘
```

## 🚀 How to Use

### 1. Add Your Streamlit Apps

Run the Streamlit UI locally:

```bash
streamlit run app.py
```

Then add your Streamlit app URLs through the web interface.

### 2. Commit Changes

After adding websites, commit the updated `websites.txt` file:

```bash
git add websites.txt
git commit -m "Add new website to wake-up list"
git push
```

### 3. GitHub Actions Does the Rest!

The GitHub Actions workflow runs automatically every hour and wakes up all your apps.

## 📁 Project Structure

```
wake-up-streamlit/
├── app.py                    # Streamlit UI for managing websites
├── automation_script.py      # Playwright script to wake up apps
├── websites.txt              # List of websites to keep awake
├── .github/
│   └── workflows/
│       └── wake-up.yml       # GitHub Actions cron job
├── pyproject.toml            # Poetry dependencies
└── README.md                 # This file
```

## 🛠️ Local Testing

Test the automation script locally:

```bash
python automation_script.py
```

## ⚙️ Configuration

### Change Wake-up Frequency

Edit `.github/workflows/wake-up.yml` and modify the cron schedule:

```yaml
schedule:
  - cron: '0 * * * *'  # Every hour
  # - cron: '*/30 * * * *'  # Every 30 minutes
  # - cron: '0 */2 * * *'  # Every 2 hours
```

### Manual Trigger

You can also manually trigger the wake-up script from GitHub Actions:
1. Go to the "Actions" tab in your repository
2. Select "Wake Up Streamlit Apps"
3. Click "Run workflow"

## 📦 Dependencies

- `streamlit` - For the web UI
- `playwright` - For browser automation

Install with Poetry:

```bash
poetry install
```

Or with pip:

```bash
pip install streamlit playwright
playwright install chromium
```

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📄 License

MIT License - feel free to use this for your own projects!