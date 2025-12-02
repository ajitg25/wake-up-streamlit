# ⏰ Keep My Streamlit Apps Awake

Automatically keep your Streamlit apps active and prevent them from going to sleep!

## 🎯 What This Does

This system automatically wakes up your Streamlit apps every hour to keep them active and responsive. No more waiting for sleeping apps to restart!

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────────┐
│  Streamlit UI   │ ───> │   MongoDB    │ ───> │ GitHub Actions  │
│  (Add websites) │      │  (Database)  │      │  (Cron Job)     │
└─────────────────┘      └──────────────┘      └─────────────────┘
                                                         │
                                                         ▼
                                                 ┌───────────────┐
                                                 │ Playwright    │
                                                 │ Wake-up Script│
                                                 └───────────────┘
```

## 🚀 How to Use

### 1. Setup MongoDB

1. Create a free MongoDB Atlas account at [mongodb.com](https://www.mongodb.com/)
2. Create a new cluster (free tier is fine)
3. Get your connection string (it looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

### 2. Configure Secrets

Add your MongoDB connection string to Streamlit secrets:

**For local development:**
Create `.streamlit/secrets.toml`:
```toml
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
```

**For Streamlit Cloud:**
1. Go to your app settings
2. Add `MONGODB_URI` in the Secrets section

**For GitHub Actions:**
1. Go to your repository Settings > Secrets and variables > Actions
2. Add a new secret named `MONGODB_URI` with your connection string

### 3. Add Your Streamlit Apps

Run the Streamlit UI:

```bash
streamlit run app.py
```

Then add your Streamlit app URLs through the web interface. They'll be saved directly to MongoDB!

### 4. GitHub Actions Does the Rest!

The GitHub Actions workflow runs automatically every hour and wakes up all your apps from the MongoDB database.

## 📁 Project Structure

```
wake-up-streamlit/
├── app.py                    # Streamlit UI for managing websites
├── automation_script.py      # Playwright script to wake up apps
├── db_utils.py               # MongoDB database utilities
├── .github/
│   └── workflows/
│       └── wake-up.yml       # GitHub Actions cron job
├── pyproject.toml            # Poetry dependencies
└── README.md                 # This file
```

## 🛠️ Local Testing

Test the automation script locally (make sure to set MONGODB_URI environment variable):

```bash
# Windows PowerShell
$env:MONGODB_URI="your-connection-string"
python automation_script.py

# Linux/Mac
export MONGODB_URI="your-connection-string"
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
- `pymongo` - For MongoDB database connection

Install with Poetry:

```bash
poetry install
```

Or with pip:

```bash
pip install streamlit playwright pymongo
playwright install chromium
```

## 🗄️ Database Schema

The MongoDB database uses a simple schema:

**Database:** `wake_up_streamlit`  
**Collection:** `websites`  
**Document Structure:**
```json
{
  "website_name": "https://your-app.streamlit.app/"
}
```

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📄 License

MIT License - feel free to use this for your own projects!