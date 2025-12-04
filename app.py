import streamlit as st
import base64
from datetime import datetime
from db_utils import get_db_connection

def main():
    st.set_page_config(
        page_title="Keep My Apps Awake",
        page_icon="⏰",
        layout="centered"
    )
    
    st.title("⏰ Keep My Streamlit Apps Awake")

    st.warning("⚠️ Deprecating this project as it violates Streamlit's Terms of Service.")

    # Display clickable image linking to the tweet
    tweet_url = "https://x.com/unfiltered_ajit/status/1995535758476935456?s=20"
    try:
        with open("image.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f'<a href="{tweet_url}" target="_blank">'
            f'<img src="data:image/png;base64,{data}" style="width:100%; border-radius: 10px;">'
            '</a>',
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.error("Image not found")
    st.markdown("---")
    
    st.markdown("""
    ### 🛑 The Problem
    As a developer, getting early traffic is hard enough. If a potential user lands on your Streamlit app only to see a **"Waking up..."** screen, they'll likely bounce and never come back.
    
    ### ✅ The Solution
    We've built an automation tool that makes sure your Streamlit apps stay **awake and ready** for every visitor, instantly.
    """)

    st.markdown("""
    ### How it works:
    1. Enter your Streamlit app name below (e.g., `my-app`)
    2. The URL gets automatically formatted and saved to MongoDB
    3. GitHub Actions runs every 12 hours to wake up your apps
    4. Your apps stay active and don't go to sleep! 🚀
    """)
    
    # Initialize database connection
    # try:
    #     db = get_db_connection()
    # except ValueError as e:
    #     st.error(f"❌ Database connection error: {e}")
    #     st.info("Please configure MONGODB_URI in Streamlit secrets.")
    #     return
    
    # # Load existing apps
    # try:
    #     websites = db.get_all_websites()
    # except Exception as e:
    #     st.error(f"❌ Error loading apps: {e}")
    #     websites = []
    
    # Add new app section
    st.subheader("➕ Add New App")
    
    # Create a structured input with prefix and suffix
    st.markdown("**Enter your Streamlit app name:**")
    
    # Use columns with better spacing and alignment
    col1, col2, col3 = st.columns([0.6, 2.5, 1.2], gap="small", vertical_alignment="center")
    
    with col1:
        st.markdown("<div style='text-align: right;'><b>https://</b></div>", unsafe_allow_html=True)
    
    with col2:
        app_name = st.text_input(
            "App Name",
            placeholder="your-app-name",
            help="Enter only the app name (e.g., 'my-app' for https://my-app.streamlit.app/)",
            label_visibility="collapsed"
        )
    
    with col3:
        st.markdown("<div><b>.streamlit.app/</b></div>", unsafe_allow_html=True)
    
    if st.button("Add App", type="primary"):
        if app_name:
            # Remove any spaces and convert to lowercase
            app_name_clean = app_name.strip().lower()
            
            # Validate app name format (alphanumeric and hyphens only)
            if not app_name_clean:
                st.error("❌ Please enter an app name")
            elif not all(c.isalnum() or c == '-' for c in app_name_clean):
                st.error("❌ App name can only contain letters, numbers, and hyphens")
            elif app_name_clean.startswith('-') or app_name_clean.endswith('-'):
                st.error("❌ App name cannot start or end with a hyphen")
            else:
                # Construct the full URL
                full_url = f"https://{app_name_clean}.streamlit.app/"
                
                try:
                    if db.add_website(full_url):
                        st.success(f"✅ Added: {full_url}")
                        st.rerun()
                    else:
                        st.warning("⚠️ This app is already in the list!")
                except Exception as e:
                    st.error(f"❌ Error adding app: DB CONNECTION IS REMOVED")
        else:
            st.error("❌ Please enter an app name")
    
    # Display existing apps
    st.markdown("---")
    st.subheader("📋 Managed Apps")
    st.markdown("These apps are currently being monitored and kept awake by our automation.")
    
    # if websites:
    #     for website in websites:
    #         col1, col2 = st.columns([3, 1], vertical_alignment="center")
    #         with col1:
    #             st.markdown(f"🔗 **[{website}]({website})**")
    #         with col2:
    #             st.success("Click to check status as now are not managed by automation")
    # else:
    #     st.info("No apps added yet. Add one above!")
    
    # Footer
    st.markdown("---")
    
    st.markdown(
        f"<div style='text-align: center; color: grey; font-size: small;'>© {datetime.now().year} Ajit Gupta. All rights reserved.</div>",
        unsafe_allow_html=True
    )

    # Close database connection
    try:
        db.close()
    except:
        pass

if __name__ == "__main__":
    main()
