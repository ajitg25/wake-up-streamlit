import streamlit as st
import os
from datetime import datetime

# File to store website URLs
WEBSITES_FILE = "websites.txt"

def load_websites():
    """Load websites from the text file"""
    if os.path.exists(WEBSITES_FILE):
        with open(WEBSITES_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

def save_websites(websites):
    """Save websites to the text file"""
    with open(WEBSITES_FILE, 'w') as f:
        for website in websites:
            f.write(f"{website}\n")

def git_commit_and_push(message):
    """Commit and push changes to GitHub"""
    try:
        import subprocess
        
        # Check if GitHub token is available
        github_token = st.secrets.get("GITHUB_TOKEN", None)
        if not github_token:
            st.warning("⚠️ GitHub token not configured. Please add GITHUB_TOKEN to Streamlit secrets.")
            return False
        
        # Configure git (needed for Streamlit Cloud)
        subprocess.run(['git', 'config', 'user.name', 'Streamlit App'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'app@streamlit.io'], check=True)
        
        # Get current remote URL and update with token
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, check=True)
        remote_url = result.stdout.strip()
        
        # Convert to authenticated URL
        if remote_url.startswith('https://github.com/'):
            auth_url = remote_url.replace('https://github.com/', 
                                         f'https://{github_token}@github.com/')
            subprocess.run(['git', 'remote', 'set-url', 'origin', auth_url], check=True)
        
        # Add, commit, and push
        subprocess.run(['git', 'add', WEBSITES_FILE], check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push'], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"Git operation failed: {e}")
        return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False


def main():
    st.set_page_config(
        page_title="Keep My Apps Awake",
        page_icon="⏰",
        layout="centered"
    )
    
    st.title("⏰ Keep My Streamlit Apps Awake")
    st.markdown("---")
    
    st.markdown("""
    ### How it works:
    1. Add your Streamlit app URL below
    2. The URL gets saved to the repository
    3. GitHub Actions runs every hour to wake up your apps
    4. Your apps stay active and don't go to sleep! 🚀
    """)
    
    # Load existing websites
    websites = load_websites()
    
    # Add new website section
    st.subheader("➕ Add New Website")
    new_website = st.text_input(
        "Enter your Streamlit app URL:",
        placeholder="https://your-app.streamlit.app/",
        help="Enter the full URL of your Streamlit app"
    )
    
    if st.button("Add Website", type="primary"):
        if new_website:
            if new_website.startswith("http"):
                if new_website not in websites:
                    websites.append(new_website)
                    save_websites(websites)
                    
                    # Auto-commit to GitHub
                    with st.spinner("Saving to GitHub..."):
                        if git_commit_and_push(f"Add website: {new_website}"):
                            st.success(f"✅ Added and committed: {new_website}")
                        else:
                            st.warning("⚠️ Website added locally but git push failed. You may need to commit manually.")
                    
                    st.rerun()
                else:
                    st.warning("⚠️ This website is already in the list!")
            else:
                st.error("❌ Please enter a valid URL starting with http:// or https://")
        else:
            st.error("❌ Please enter a website URL")
    
    # Display existing websites
    st.markdown("---")
    st.subheader("📋 Websites which are added")
    
    if websites:
        for idx, website in enumerate(websites):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(f"{idx + 1}. {website}")
    else:
        st.info("No websites added yet. Add one above!")
    
    # Footer
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
