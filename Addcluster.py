import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Leads Details by Municipality", layout="wide")

# Sidebar for file upload
st.sidebar.header("Upload Excel File")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file (.xlsx)", type=["xlsx"])

# Full list of municipalities from the provided image
municipalities = [
    "Abra", "Agusan del Norte", "Agusan del Sur", "Aklan", "Albay", "Antique", "Apayao", "Aurora", "Basilan",
    "Bataan", "Batanes", "Batangas", "Benguet", "Biliran", "Bohol", "Bukidnon", "Bulacan", "Cagayan", "Camarines Norte",
    "Camarines Sur", "Camiguin", "Capiz", "Catanduanes", "Cavite", "Cebu", "Cotabato", "Davao de Oro", "Davao del Norte",
    "Davao del Sur", "Davao Occidental", "Davao Oriental", "Dinagat Islands", "Eastern Samar", "Guimaras", "Ifugao",
    "Ilocos Norte", "Ilocos Sur", "Iloilo", "Isabela", "Kalinga", "La Union", "Laguna", "Lanao del Norte",
    "Lanao del Sur", "Leyte", "Maguindanao", "Marinduque", "Masbate", "Metro Manila", "Misamis Occidental",
    "Misamis Oriental", "Mountain Province", "Negros Occidental", "Negros Oriental", "Northern Samar", "Nueva Ecija",
    "Nueva Vizcaya", "Occidental Mindoro", "Oriental Mindoro", "Palawan", "Pampanga", "Pangasinan", "Quezon",
    "Quirino", "Rizal", "Romblon", "Samar", "Sarangani", "Siquijor", "Sorsogon", "South Cotabato", "Southern Leyte",
    "Sultan Kudarat", "Sulu", "Surigao del Norte", "Surigao del Sur", "Tarlac", "Tawi-Tawi", "Zambales", "Zamboanga del Norte",
    "Zamboanga del Sur", "Zamboanga Sibugay"
]

# Region mapping for municipalities
region_mapping = {
    "Abra": "Luzon", "Agusan del Norte": "Mindanao", "Agusan del Sur": "Mindanao", "Aklan": "Visayas",
    "Albay": "Luzon", "Antique": "Visayas", "Apayao": "Luzon", "Aurora": "Luzon", "Basilan": "Mindanao",
    "Bataan": "Luzon", "Batanes": "Luzon", "Batangas": "Luzon", "Benguet": "Luzon", "Biliran": "Visayas",
    "Bohol": "Visayas", "Bukidnon": "Mindanao", "Bulacan": "Luzon", "Cagayan": "Luzon", "Camarines Norte": "Luzon",
    "Camarines Sur": "Luzon", "Camiguin": "Mindanao", "Capiz": "Visayas", "Catanduanes": "Luzon", "Cavite": "Luzon",
    "Cebu": "Visayas", "Cotabato": "Mindanao", "Davao de Oro": "Mindanao", "Davao del Norte": "Mindanao",
    "Davao del Sur": "Mindanao", "Davao Occidental": "Mindanao", "Davao Oriental": "Mindanao", "Dinagat Islands": "Mindanao",
    "Eastern Samar": "Visayas", "Guimaras": "Visayas", "Ifugao": "Luzon", "Ilocos Norte": "Luzon", "Ilocos Sur": "Luzon",
    "Iloilo": "Visayas", "Isabela": "Luzon", "Kalinga": "Luzon", "La Union": "Luzon", "Laguna": "Luzon",
    "Lanao del Norte": "Mindanao", "Lanao del Sur": "Mindanao", "Leyte": "Visayas", "Maguindanao": "Mindanao",
    "Marinduque": "Luzon", "Masbate": "Visayas", "Metro Manila": "Luzon", "Misamis Occidental": "Mindanao",
    "Misamis Oriental": "Mindanao", "Mountain Province": "Luzon", "Negros Occidental": "Visayas",
    "Negros Oriental": "Visayas", "Northern Samar": "Visayas", "Nueva Ecija": "Luzon", "Nueva Vizcaya": "Luzon",
    "Occidental Mindoro": "Luzon", "Oriental Mindoro": "Luzon", "Palawan": "Luzon", "Pampanga": "Luzon",
    "Pangasinan": "Luzon", "Quezon": "Luzon", "Quirino": "Luzon", "Rizal": "Luzon", "Romblon": "Visayas",
    "Samar": "Visayas", "Sarangani": "Mindanao", "Siquijor": "Visayas", "Sorsogon": "Luzon", "South Cotabato": "Mindanao",
    "Southern Leyte": "Visayas", "Sultan Kudarat": "Mindanao", "Sulu": "Mindanao", "Surigao del Norte": "Mindanao",
    "Surigao del Sur": "Mindanao", "Tarlac": "Luzon", "Tawi-Tawi": "Mindanao", "Zambales": "Luzon",
    "Zamboanga del Norte": "Mindanao", "Zamboanga del Sur": "Mindanao", "Zamboanga Sibugay": "Mindanao"
}

def assign_municipality(address):
    """
    Assign a municipality from the list based on the address string.
    Returns the matched municipality or 'Unknown' if no match.
    """
    if pd.isna(address) or not isinstance(address, str):
        return "Unknown"
    address = address.lower()
    for mun in municipalities:
        if mun.lower() in address:
            return mun
    return "Unknown"

def generate_detailed_summary(df):
    """
    Generate detailed lead data grouped by municipality and return a dictionary of DataFrames.
    """
    # Assign municipality to each row
    df["Municipality"] = df["primary address"].apply(assign_municipality)
    
    # Assign region based on municipality
    df["Region"] = df["Municipality"].map(region_mapping).fillna("Unknown")
    
    # Initialize dictionary to store per-municipality detailed data
    detailed_data = {}
    
    # Get unique municipalities
    municipalities = df["Municipality"].unique()
    
    for municipality in sorted(municipalities):
        if municipality == "Unknown":
            continue  # Skip 'Unknown' municipality for individual tables
        # Filter data for the current municipality
        mun_df = df[df["Municipality"] == municipality].copy()
        
        # Add primary address and region to the detailed data
        mun_df["Primary Address"] = mun_df["primary address"]
        mun_df["Region"] = region_mapping.get(municipality, "Unknown")
        
        # Select all columns for detailed view
        detailed_data[municipality] = mun_df
        
    # Create a combined DataFrame for download
    combined_detailed = pd.concat(detailed_data.values(), ignore_index=True)
    
    return detailed_data, combined_detailed

# Main app logic
st.title("Leads Details by Municipality")

if uploaded_file is not None:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)
        
        # Verify that 'primary address' column exists
        if "primary address" not in df.columns:
            st.error("The uploaded file does not contain a 'primary address' column.")
        else:
            # Generate detailed data
            detailed_data, combined_detailed = generate_detailed_summary(df)
            
            # Display detailed tables for each municipality
            st.subheader("Detailed Leads by Municipality")
            for municipality, detailed_df in detailed_data.items():
                st.write(f"### {municipality} (Region: {detailed_df['Region'].iloc[0]})")
                st.dataframe(detailed_df, use_container_width=True)
                st.write("---")  # Separator between tables
            
            # Option to download combined detailed data as CSV
            csv = combined_detailed.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Combined Detailed Data as CSV",
                data=csv,
                file_name="detailed_leads_data.csv",
                mime="text/csv",
            )
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("Please upload an Excel file using the sidebar to see the detailed leads data.")        