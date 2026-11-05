import streamlit as st
import ee
import geemap.foliumap as geemap

# 1. Initialize Page Settings
st.set_page_config(page_title="GeoAI Eco-Monitor", layout="wide", page_icon="🌍")
st.title("🌍 Geospatial Analytics & GeoAI Monitoring Engine")
st.markdown("Automated Remote Sensing & Machine Learning Dashboard powered by Google Earth Engine.")

# 2. Sidebar Controls
st.sidebar.header("🎛️ Engine Controls")
zoom_level = st.sidebar.slider("Map Zoom Level", min_value=4, max_value=12, value=6)
selected_layers = st.sidebar.multiselect(
    "Select Display Layers",
    ["Sentinel-2 Clear Mosaic", "Vegetation Health Index (NDVI)", "GeoAI Automated Land Cover"],
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
    
    # Render Interactive Visual Viewport using the folium-backed layout
    Map = geemap.Map(center=[0.0, 37.0], zoom=zoom_level)
    Map.add_basemap('HYBRID')
    
    # Layer 1: Raw Sentinel Mosaic
    if "Sentinel-2 Clear Mosaic" in selected_layers:
        Map.addLayer(clear_composite, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, 'Sentinel-2 Clear Mosaic')
        
    # Layer 2: Analytical NDVI Index
    if "Vegetation Health Index (NDVI)" in selected_layers:
        ndvi = clear_composite.normalizedDifference(['B8', 'B4'])
        ndvi_palette = ['#FFFFFF', '#CE7E45', '#DF923D', '#F1B555', '#99B718', '#207401', '#011301']
        Map.addLayer(ndvi, {'min': 0.0, 'max': 0.8, 'palette': ndvi_palette}, 'Vegetation Health Index (NDVI)')
        
    # Layer 3: Machine Learning Model Deployment
    if "GeoAI Automated Land Cover" in selected_layers:
        forest_mask = ndvi.gt(0.6).remap([0, 1], [1, 2], 0).rename('landcover')
        prediction_bands = ['B2', 'B3', 'B4', 'B8']
        sample_dataset = clear_composite.select(prediction_bands).addBands(forest_mask).stratifiedSample(
            numPoints=50, classBand='landcover', region=point.buffer(30000), scale=30, geometries=True
        )
        geo_ai_classifier = ee.Classifier.smileRandomForest(numberOfTrees=10).train(
            features=sample_dataset, classProperty='landcover', inputProperties=prediction_bands
        )
        classified_map = clear_composite.select(prediction_bands).classify(geo_ai_classifier)
        Map.addLayer(classified_map, {'min': 1, 'max': 2, 'palette': ['#228B22', '#FF4500']}, 'GeoAI Automated Land Cover')

    # Draw the dynamic map layout directly into the Streamlit Web Frame
    Map.to_streamlit(height=650)
