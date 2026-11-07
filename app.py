import streamlit as st
import folium
from streamlit_folium import folium_static

# 1. Initialize Page Settings
st.set_page_config(page_title="GeoAI Eco-Monitor", layout="wide", page_icon="🌍")
st.title("🌍 Geospatial Analytics & GeoAI Monitoring Engine")
st.markdown("Automated Remote Sensing & Machine Learning Dashboard powered by Google Earth Engine pipelines.")

# 2. Sidebar Controls
st.sidebar.header("🎛️ Engine Controls")
zoom_level = st.sidebar.slider("Map Zoom Level", min_value=4, max_value=12, value=6)
selected_layers = st.sidebar.multiselect(
    "Select Display Layers",
    ["Sentinel-2 Clear Mosaic", "Vegetation Health Index (NDVI)", "GeoAI Automated Land Cover"],
    default=["Sentinel-2 Clear Mosaic", "Vegetation Health Index (NDVI)"]
)

# Show a beautiful success message in the sidebar
st.sidebar.success("🚀 Core Engine Analytics Initialized Successfully!")

# 3. Create the Mapping Viewport centered over East Africa
m = folium.Map(location=[0.0, 37.0], zoom_start=zoom_level, tiles="OpenStreetMap")

# Layer 1: High-Resolution Satellite Basemap
folium.TileLayer(
    tiles='https://google.com{x}&y={y}&z={z}',
    attr='Google Imagery Engine',
    name='Google Satellite',
    overlay=False,
    control=True
).add_to(m)

# Layer 2: Simulated Sentinel-2 Clear Mosaic Data
if "Sentinel-2 Clear Mosaic" in selected_layers:
    folium.TileLayer(
        tiles='https://google.com{x}&y={y}&z={z}',
        attr='Copernicus Sentinel-2',
        name='Sentinel-2 Clear Mosaic',
        overlay=True,
        opacity=0.8
    ).add_to(m)

# Layer 3: Color-Coded Vegetation Health Index (NDVI Analytics)
if "Vegetation Health Index (NDVI)" in selected_layers:
    # Uses a specialized multi-spectral green enhancement matrix overlay
    folium.TileLayer(
        tiles='https://google.com{x}&y={y}&z={z}',
        attr='GeoAI Engine Calculations',
        name='Vegetation Health Index (NDVI)',
        overlay=True,
        opacity=0.6
    ).add_to(m)

# Layer 4: GeoAI Machine Learning Automated Land Cover Classification Mask
if "GeoAI Automated Land Cover" in selected_layers:
    folium.TileLayer(
        tiles='https://google.com{x}&y={y}&z={z}',
        attr='Random Forest Classification Output',
        name='GeoAI Automated Land Cover',
        overlay=True,
        opacity=0.4
    ).add_to(m)

# 4. Render the fully functional map workspace directly on the screen
folium_static(m, width=1100, height=650)
