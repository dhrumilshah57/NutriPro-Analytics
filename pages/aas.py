import streamlit as st
import pandas as pd

# FAO/WHO reference amino acid pattern in mg of amino acid per gram of protein
reference_pattern = {
    'HIS': 15,  # Histidine
    'ILE': 30,  # Isoleucine
    'LEU': 59,  # Leucine
    'LYS': 45,  # Lysine
    'THR': 23,  # Threonine
    'TRP': 6,   # Tryptophan
    'VAL': 39,  # Valine
    'CYS': 22,  # Cysteine
    'MET': 22,  # Methionine
    'PHE': 38   # Phenylalanine
}

# Example digestibility values for demonstration
digestibility_factors = {
    'Buckwheat Flour Control': 0.78,
    'Extruded Buckwheat Flour': 0.85,
    'Sample 3': 0.90  # Add more values for specific samples
}

# Default digestibility if not specified
default_digestibility = 0.80

# Streamlit app layout
st.title('Amino Acid Score (AAS) Calculator')

# File uploader
uploaded_file = st.file_uploader("Upload your protein breakdown Excel file", type=["xlsx", "xls"])

# Display results after file upload
if uploaded_file:
    # Read the uploaded Excel file
    data = pd.read_excel(uploaded_file)

    # Ensure required amino acid columns and 'SAMPLE' column exist in the dataset
    if set(reference_pattern.keys()).issubset(data.columns) and 'SAMPLE' in data.columns:
        st.write("Uploaded Data:")
        st.dataframe(data)

        # Normalize values from grams per 100g of protein to mg per gram of protein (if necessary)
        for aa in reference_pattern.keys():
            data[aa] = data[aa] * 10  # Convert g/100g to mg/g by multiplying by 10

        # Add a column for digestibility based on the sample name or use default value
        data['Digestibility'] = data['SAMPLE'].map(digestibility_factors).fillna(default_digestibility)

        # Calculate AAS for each food item
        def calculate_aas(row):
            # Normalize amino acid values by the reference pattern
            scores = {aa: row[aa] / reference_pattern[aa] for aa in reference_pattern.keys() if aa in row}
            limiting_aa_score = min(scores.values())  # Limiting amino acid score
            limiting_aa = min(scores, key=scores.get)
            # Apply digestibility correction
            digestibility_corrected_score = limiting_aa_score * row['Digestibility']
            return digestibility_corrected_score, limiting_aa

        # Apply the AAS formula to each row
        data['AAS'], data['Limiting AA'] = zip(*data.apply(calculate_aas, axis=1))

        # Display the full table
        st.write("Calculated AAS Scores for All Items (with Digestibility):")
        st.dataframe(data[['SAMPLE', 'AAS', 'Limiting AA', 'Digestibility']])

        # Dropdown menu to select food item
        selected_sample = st.selectbox("Select a food item to view AAS score", data['SAMPLE'].unique())

        # Display AAS score for the selected item
        selected_item_data = data[data['SAMPLE'] == selected_sample]
        if not selected_item_data.empty:
            selected_aas = selected_item_data['AAS'].values[0]
            limiting_aa = selected_item_data['Limiting AA'].values[0]
            st.write(f"AAS for {selected_sample}: {selected_aas:.2f}")
            st.write(f"Limiting Amino Acid for {selected_sample}: {limiting_aa}")

        # Download button for the output
        st.download_button(label="Download Results", data=data.to_csv(index=False), mime='text/csv')
