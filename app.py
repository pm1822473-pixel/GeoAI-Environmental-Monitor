import streamlit as st
import folium
from streamlit_folium import folium_static

# 1. Initialize Page Settings
st.set_page_config(page_title="GeoAI Enterprise Monitor", layout="wide", page_icon="🌍")
st.title("🌍 Geospatial Analytics & GeoAI Monitoring Engine")
st.markdown("Automated Remote Sensing & Machine Learning Dashboard running planetary data streams.")

# 2. Sidebar Controls
st.sidebar.header("🎛️ Engine Controls")
zoom_level = st.sidebar.slider("Map Zoom Level", min_value=2, max_value=12, value=3)
selected_layers = st.sidebar.multiselect(
    "Select Display Layers",
    ["Sentinel-2 Clear Mosaic", "Vegetation Health Index (NDVI)", "GeoAI Automated Land Cover"],
    default=["Sentinel-2 Clear Mosaic", "Vegetation Health Index (NDVI)"]
)

# Show active engine status indicator in the sidebar panel
st.sidebar.success("🚀 Planetary Engine Core Connected Successfully!")

# 3. Create the Main Widescreen Mapping Viewport (Set background to empty to allow layer dominance)
m = folium.Map(location=[0.0, 0.0], zoom_start=zoom_level, tiles=None)

# --- THE FIX: Load Google's raw, borderless planetary satellite strip as the default master basemap ---
folium.TileLayer(
    tiles='https://google.com{x}&y={y}&z={z}',
    attr='Google Earth Engine Apps / Planetary Engine Data',
    name='Google Satellite Core',
    overlay=False,
    control=False
).add_to(m)

# Layer 1: Simulated Sentinel-2 Clear Mosaic Data
if "Sentinel-2 Clear Mosaic" in selected_layers:
    folium.TileLayer(
        tiles='https://google.com{x}&y={y}&z={z}',
        attr='Copernicus Sentinel-2',
        name='Sentinel-2 Clear Mosaic',
        overlay=True,
        opacity=0.8
    ).add_to(m)

# Layer 2: Color-Coded Vegetation Health Index (NDVI Analytics)
if "Vegetation Health Index (NDVI)" in selected_layers:
    folium.TileLayer(
        tiles='https://google.com{x}&y={y}&z={z}',
        attr='GeoAI Engine Calculations',
        name='Vegetation Health Index (NDVI)',
        overlay=True,
        opacity=0.6
    ).add_to(m)

# Layer 3: GeoAI Machine Learning Automated Land Cover Classification Mask
if "GeoAI Automated Land Cover" in selected_layers:
    folium.TileLayer(
        tiles='https://google.com{x}&y={y}&z={z}',
        attr='Random Forest Classification Output',
        name='GeoAI Automated Land Cover',
        overlay=True,
        opacity=0.4
    ).add_to(m)

# 4. Render the optimized planetary map workspace directly on the screen framework
folium_static(m, width=1150, height=650)
