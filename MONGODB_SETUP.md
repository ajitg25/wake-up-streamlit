# MongoDB Setup Guide

This guide will help you set up MongoDB for the Wake Up Streamlit Apps project.

## Step 1: Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a free account
3. Verify your email address

## Step 2: Create a Cluster

1. After logging in, click "Build a Database"
2. Choose the **FREE** tier (M0 Sandbox)
3. Select a cloud provider and region (choose one closest to you)
4. Click "Create Cluster"
5. Wait for the cluster to be created (takes 1-3 minutes)

## Step 3: Create Database User

1. In the Security section, click "Database Access"
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Enter a username and password (save these!)
5. Set user privileges to "Read and write to any database"
6. Click "Add User"

## Step 4: Configure Network Access

1. In the Security section, click "Network Access"
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (or add `0.0.0.0/0`)
   - This is needed for GitHub Actions and Streamlit Cloud
4. Click "Confirm"

## Step 5: Get Connection String

1. Go back to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Select "Python" as the driver
5. Copy the connection string (it looks like this):
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<username>` and `<password>` with your actual credentials

## Step 6: Configure Secrets

### For Local Development

Create `.streamlit/secrets.toml` in your project root:

```toml
MONGODB_URI = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

### For Streamlit Cloud

1. Go to your app on [share.streamlit.io](https://share.streamlit.io)
2. Click on your app settings (⚙️)
3. Go to "Secrets"
4. Add:
   ```toml
   MONGODB_URI = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
   ```

### For GitHub Actions

1. Go to your GitHub repository
2. Click "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Name: `MONGODB_URI`
5. Value: Your MongoDB connection string
6. Click "Add secret"

## Step 7: Test the Connection

Run the Streamlit app locally:

```bash
streamlit run app.py
```

If everything is configured correctly, you should be able to add websites through the UI!

## Troubleshooting

### "Database connection error"
- Check that your connection string is correct
- Verify your username and password
- Make sure you've allowed network access from anywhere

### "Authentication failed"
- Double-check your username and password in the connection string
- Ensure the database user has proper permissions

### "Network timeout"
- Check your internet connection
- Verify that IP address `0.0.0.0/0` is allowed in Network Access

## Database Structure

The app will automatically create:
- **Database name:** `wake_up_streamlit`
- **Collection name:** `websites`
- **Document structure:**
  ```json
  {
    "_id": ObjectId("..."),
    "website_name": "https://your-app.streamlit.app/"
  }
  ```

You can view your data in MongoDB Atlas:
1. Go to "Database" in the left sidebar
2. Click "Browse Collections" on your cluster
3. Navigate to `wake_up_streamlit` > `websites`
