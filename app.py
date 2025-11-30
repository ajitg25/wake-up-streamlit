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
                    st.success(f"✅ Added: {new_website}")
                    st.rerun()
                else:
                    st.warning("⚠️ This website is already in the list!")
            else:
                st.error("❌ Please enter a valid URL starting with http:// or https://")
        else:
            st.error("❌ Please enter a website URL")
    
    # Display existing websites
    st.markdown("---")
    st.subheader("📋 Active Websites")
    
    if websites:
        for idx, website in enumerate(websites):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(f"{idx + 1}. {website}")
            with col2:
                if st.button("🗑️", key=f"delete_{idx}", help="Remove this website"):
                    websites.pop(idx)
                    save_websites(websites)
                    st.rerun()
    else:
        st.info("No websites added yet. Add one above!")
    
    # Footer
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
