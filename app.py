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
        
        print(f"[DEBUG] Starting git commit and push for: {message}")
        
        # Check if GitHub token is available
        github_token = st.secrets.get("GITHUB_TOKEN", None)
        if not github_token:
            error_msg = "⚠️ GitHub token not configured. Please add GITHUB_TOKEN to Streamlit secrets."
            print(f"[ERROR] {error_msg}")
            st.warning(error_msg)
            return False
        
        print(f"[DEBUG] GitHub token found (length: {len(github_token)})")
        
        # Configure git (needed for Streamlit Cloud)
        print("[DEBUG] Configuring git user...")
        result = subprocess.run(['git', 'config', 'user.name', 'Streamlit App'], 
                               capture_output=True, text=True)
        print(f"[DEBUG] Git config user.name: {result.returncode}, stdout: {result.stdout}, stderr: {result.stderr}")
        
        result = subprocess.run(['git', 'config', 'user.email', 'app@streamlit.io'], 
                               capture_output=True, text=True)
        print(f"[DEBUG] Git config user.email: {result.returncode}, stdout: {result.stdout}, stderr: {result.stderr}")
        
        # Get current remote URL and update with token
        print("[DEBUG] Getting remote URL...")
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] Failed to get remote URL: {result.stderr}")
            st.error(f"Failed to get remote URL: {result.stderr}")
            return False
            
        remote_url = result.stdout.strip()
        print(f"[DEBUG] Remote URL: {remote_url}")
        
        # Convert to authenticated URL
        if remote_url.startswith('https://github.com/'):
            auth_url = remote_url.replace('https://github.com/', 
                                         f'https://{github_token}@github.com/')
            print(f"[DEBUG] Setting authenticated remote URL...")
            result = subprocess.run(['git', 'remote', 'set-url', 'origin', auth_url], 
                                   capture_output=True, text=True)
            print(f"[DEBUG] Set remote URL: {result.returncode}, stderr: {result.stderr}")
        
        # Add files
        print(f"[DEBUG] Adding {WEBSITES_FILE}...")
        result = subprocess.run(['git', 'add', WEBSITES_FILE], 
                               capture_output=True, text=True)
        print(f"[DEBUG] Git add: {result.returncode}, stdout: {result.stdout}, stderr: {result.stderr}")
        if result.returncode != 0:
            st.error(f"Git add failed: {result.stderr}")
            return False
        
        # Commit
        print(f"[DEBUG] Committing with message: {message}")
        result = subprocess.run(['git', 'commit', '-m', message], 
                               capture_output=True, text=True)
        print(f"[DEBUG] Git commit: {result.returncode}, stdout: {result.stdout}, stderr: {result.stderr}")
        if result.returncode != 0:
            # Check if it's "nothing to commit"
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                print("[DEBUG] Nothing to commit (file unchanged)")
                st.info("No changes to commit")
                return True
            else:
                st.error(f"Git commit failed: {result.stderr}")
                return False
        
        # Push
        print("[DEBUG] Pushing to remote...")
        result = subprocess.run(['git', 'push'], 
                               capture_output=True, text=True, timeout=30)
        print(f"[DEBUG] Git push: {result.returncode}, stdout: {result.stdout}, stderr: {result.stderr}")
        if result.returncode != 0:
            st.error(f"Git push failed: {result.stderr}")
            return False
        
        print("[DEBUG] Git commit and push completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Git operation failed: {e}, stdout: {e.stdout if hasattr(e, 'stdout') else 'N/A'}, stderr: {e.stderr if hasattr(e, 'stderr') else 'N/A'}"
        print(f"[ERROR] {error_msg}")
        st.error(error_msg)
        return False
    except subprocess.TimeoutExpired:
        error_msg = "Git push timed out (30s). Check your network connection."
        print(f"[ERROR] {error_msg}")
        st.error(error_msg)
        return False
    except Exception as e:
        error_msg = f"Unexpected error: {type(e).__name__}: {e}"
        print(f"[ERROR] {error_msg}")
        st.error(error_msg)
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
                    

                    print("adding website")
                    # Auto-commit to GitHub
                    with st.spinner("Saving to GitHub..."):
                        if git_commit_and_push(f"Add website: {new_website}"):
                            print("website added")
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
