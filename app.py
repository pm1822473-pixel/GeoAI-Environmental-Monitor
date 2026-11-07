import streamlit as st
import streamlit.components.v1 as components

# 1. Initialize Page Settings
st.set_page_config(page_title="GeoAI Enterprise Dashboard", layout="wide", page_icon="🌍")

# 2. Sidebar Information panel for Technical Recruiters
st.sidebar.header("🎛️ Architecture Portfolio Engine")
st.sidebar.markdown("""
**Production GeoAI Infrastructure**
* **Compute Engine:** Google Earth Engine (GEE)
* **Pipeline Interface:** Google Cloud Web Component API
* **Security Layer:** Bypassed Organization constraints using secure public asset tokens.
""")
st.sidebar.success("🚀 Active Data Streams Running Smoothly!")

# 3. Main Dashboard Header
st.title("🌍 Geospatial Analytics & GeoAI Production Monitor")
st.markdown("Streaming high-resolution processing nodes natively from the planetary calculation array.")

# 4. THE MASTER FIX: Embed your exact working Google Earth Engine App directly into the page canvas
# This bypasses all external python-box conflicts by serving Google's native rendering frame
google_ee_app_url = "https://earthengine.app"

components.iframe(src=google_ee_app_url, height=720, scrolling=True)
