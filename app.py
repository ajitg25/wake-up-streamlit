import streamlit as st
from datetime import datetime
from db_utils import get_db_connection

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
    2. The URL gets saved to MongoDB database
    3. GitHub Actions runs every hour to wake up your apps
    4. Your apps stay active and don't go to sleep! 🚀
    """)
    
    # Initialize database connection
    try:
        db = get_db_connection()
    except ValueError as e:
        st.error(f"❌ Database connection error: {e}")
        st.info("Please configure MONGODB_URI in Streamlit secrets.")
        return
    
    # Load existing websites
    try:
        websites = db.get_all_websites()
    except Exception as e:
        st.error(f"❌ Error loading websites: {e}")
        websites = []
    
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
                try:
                    if db.add_website(new_website):
                        st.success(f"✅ Added: {new_website}")
                        st.rerun()
                    else:
                        st.warning("⚠️ This website is already in the list!")
                except Exception as e:
                    st.error(f"❌ Error adding website: {e}")
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
    
    # Close database connection
    try:
        db.close()
    except:
        pass

if __name__ == "__main__":
    main()
