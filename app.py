import streamlit as st
import ee
import folium
from streamlit_folium import folium_static

# 1. Initialize Page Settings
st.set_page_config(page_title="GeoAI Eco-Monitor", layout="wide", page_icon="🌍")
st.title("🌍 Geospatial Analytics & GeoAI Monitoring Engine")
st.markdown("Automated Remote Sensing & Machine Learning Dashboard powered by Google Earth Engine.")

# 2. Sidebar Controls
st.sidebar.header("🎛️ Engine Controls")
zoom_level = st.sidebar.slider("Map Zoom Level", min_value=4, max_value=12, value=6)
selected_layers = st.sidebar.multiselect(
    "Select Display Layers",
    ["Sentinel-2 Clear Mosaic", "Vegetation Health Index (NDVI)"],
    default=["Sentinel-2 Clear Mosaic", "Vegetation Health Index (NDVI)"]
)

# 3. Securely Initialize Earth Engine using your project ID
if 'ee_initialized' not in st.session_state:
    try:
        ee.Initialize(project='trade-vault-p')
        st.session_state['ee_initialized'] = True
    except Exception as e:
        st.error(f"Authentication failed: Please check your configuration permissions.")

# 4. Reconstruct Your Geospatial Core Logic
if st.session_state.get('ee_initialized'):
    # Define Core Points & Imagery Extraction
    point = ee.Geometry.Point([37.0, 0.0])
    sentinel_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                           .filterBounds(point)
                           .filterDate('2025-01-01', '2025-12-31')
                           .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)))
    clear_composite = sentinel_collection.median()
    
    # Create standard Folium Map
    m = folium.Map(location=[0.0, 37.0], zoom_start=zoom_level, tiles="OpenStreetMap")
    
    # Add Google Satellite Basemap manually to bypass geemap dependencies
    folium.TileLayer(
        tiles='https://google.com{x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Layer 1: Raw Sentinel Mosaic
    if "Sentinel-2 Clear Mosaic" in selected_layers:
        viz_params = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}
        map_id_dict = ee.Image(clear_composite).getMapId(viz_params)
        folium.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name='Sentinel-2 Clear Mosaic',
            overlay=True
        ).add_to(m)
        
    # Layer 2: Analytical NDVI Index
    if "Vegetation Health Index (NDVI)" in selected_layers:
        ndvi = clear_composite.normalizedDifference(['B8', 'B4'])
        # Simplified beautiful hex palette for standard folium mapping
        map_id_dict_ndvi = ee.Image(ndvi).getMapId({
            'min': 0.0, 
            'max': 0.8, 
            'palette': ['FFFFFF', 'CE7E45', 'DF923D', '99B718', '207401', '011301']
        })
        folium.TileLayer(
            tiles=map_id_dict_ndvi['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name='Vegetation Health Index (NDVI)',
            overlay=True
        ).add_to(m)

    # Render map cleanly on the dashboard web framework
    folium_static(m, width=1100, height=650)
