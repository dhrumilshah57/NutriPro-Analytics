import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# FAO/WHO reference amino acid patterns for different age groups (in mg of amino acid per gram of protein)
reference_patterns = {
    'Adults (2010)': {'HIS': 15, 'ILE': 30, 'LEU': 59, 'LYS': 45, 'THR': 23, 'TRP': 6, 'VAL': 39, 'CYS': 22, 'MET': 22, 'PHE': 38},
    'Adolescents (2005)': {'HIS': 18, 'ILE': 34, 'LEU': 63, 'LYS': 47, 'THR': 25, 'TRP': 7, 'VAL': 41, 'CYS': 24, 'MET': 24, 'PHE': 40},
    'Infants (1990)': {'HIS': 20, 'ILE': 40, 'LEU': 72, 'LYS': 50, 'THR': 30, 'TRP': 8, 'VAL': 44, 'CYS': 30, 'MET': 28, 'PHE': 45}
}

# RDI values (Recommended Daily Intake) based on different age groups (mg per gram of protein)
rdi_values = {
    'Adults (2010)': {'HIS': 15, 'ILE': 30, 'LEU': 59, 'LYS': 45, 'THR': 23, 'TRP': 6, 'VAL': 39, 'CYS': 22, 'MET': 22, 'PHE': 38},
    'Adolescents (2005)': {'HIS': 18, 'ILE': 34, 'LEU': 63, 'LYS': 47, 'THR': 25, 'TRP': 7, 'VAL': 41, 'CYS': 24, 'MET': 24, 'PHE': 40},
    'Infants (1990)': {'HIS': 20, 'ILE': 40, 'LEU': 72, 'LYS': 50, 'THR': 30, 'TRP': 8, 'VAL': 44, 'CYS': 30, 'MET': 28, 'PHE': 45}
}

# Example digestibility values for demonstration
digestibility_factors = {'Buckwheat Flour Control': 0.78, 'Extruded Buckwheat Flour': 0.85, 'Sample 3': 0.90}
default_digestibility = 0.80

# Streamlit app layout
st.title('Amino Acid Score (AAS) Calculator')

# Dropdown for selecting the reference pattern
selected_pattern = st.selectbox("Select Reference Pattern", list(reference_patterns.keys()))
current_pattern = reference_patterns[selected_pattern]
rdi_pattern = rdi_values[selected_pattern]  # RDI for the selected age group

# Sidebar for displaying RDI values
st.sidebar.header(f"Recommended Daily Intake (RDI) for {selected_pattern}")
for aa, rdi_value in rdi_pattern.items():
    st.sidebar.write(f"{aa}: {rdi_value} mg/g protein")

# File uploader
uploaded_file = st.file_uploader("Upload your protein breakdown Excel file", type=["xlsx", "xls"])

# Display results after file upload
if uploaded_file:
    data = pd.read_excel(uploaded_file)

    if set(current_pattern.keys()).issubset(data.columns) and 'SAMPLE' in data.columns:
        st.write("Uploaded Data:")
        st.dataframe(data)

        # Normalize amino acid values (if necessary)
        for aa in current_pattern.keys():
            data[aa] = data[aa] * 10  # Convert g/100g to mg/g by multiplying by 10

        # Add a column for digestibility
        data['Digestibility'] = data['SAMPLE'].map(digestibility_factors).fillna(default_digestibility)

        # Function to calculate AAS
        def calculate_aas(row):
            scores = {aa: row[aa] / current_pattern[aa] for aa in current_pattern.keys()}
            limiting_aa_score = min(scores.values())  # Limiting amino acid score
            limiting_aa = min(scores, key=scores.get)
            digestibility_corrected_score = limiting_aa_score * row['Digestibility']
            return digestibility_corrected_score, limiting_aa

        # Apply AAS calculation
        data['AAS'], data['Limiting AA'] = zip(*data.apply(calculate_aas, axis=1))

        # Display the table with AAS and digestibility
        st.write("Calculated AAS Scores for All Items:")
        st.dataframe(data[['SAMPLE', 'AAS', 'Limiting AA', 'Digestibility']])

        # Dropdown to select food item for detailed view
        selected_sample = st.selectbox("Select a food item to view AAS score", data['SAMPLE'].unique())
        selected_item_data = data[data['SAMPLE'] == selected_sample]
        if not selected_item_data.empty:
            selected_aas = selected_item_data['AAS'].values[0]
            limiting_aa = selected_item_data['Limiting AA'].values[0]
            st.write(f"AAS for {selected_sample}: {selected_aas:.2f}")
            st.write(f"Limiting Amino Acid for {selected_sample}: {limiting_aa}")

        # Bar plot of AAS scores
        st.subheader("Amino Acid Score (AAS) Comparison Across Samples")
        st.markdown("""
        The bar chart below shows the AAS scores of different samples. The AAS score is calculated based on the limiting amino acid 
        (the amino acid that is present in the lowest proportion relative to the human nutritional requirement) and adjusted for 
        protein digestibility.
        """)

        def plot_aas_bar(data):
            fig, ax = plt.subplots()
            ax.bar(data['SAMPLE'], data['AAS'], color='skyblue')
            ax.set_xlabel('Sample')
            ax.set_ylabel('AAS Score')
            ax.set_title('AAS Scores by Sample')
            st.pyplot(fig)

        plot_aas_bar(data)

        # Radar chart for selected sample
        st.subheader("Amino Acid Profile for Selected Sample Compared to RDI")
        st.markdown("""
        The radar chart below compares the amino acid profile of the selected sample to the Recommended Daily Intake (RDI) values for the selected age group.
        Each spoke of the chart represents an essential amino acid, and the values show how much of each amino acid is present in the sample compared 
        to the RDI for that age group.
        """)

        def radar_plot(selected_item_data, current_pattern, rdi_pattern):
            categories = list(current_pattern.keys())
            sample_values = [selected_item_data[aa].values[0] for aa in categories]
            rdi_values = [rdi_pattern[aa] for aa in categories]

            fig = go.Figure()

            # Add trace for sample values
            fig.add_trace(go.Scatterpolar(r=sample_values, theta=categories, fill='toself', name='Sample Profile'))
            # Add trace for RDI values
            fig.add_trace(go.Scatterpolar(r=rdi_values, theta=categories, fill='toself', name='RDI'))

            fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
            st.plotly_chart(fig)

        radar_plot(selected_item_data, current_pattern, rdi_pattern)

        # AAS Comparison across Age Groups
        st.subheader("Comparison of AAS Across Age Groups")
        st.markdown("""
        The following graph shows how the Amino Acid Score (AAS) for a selected protein source varies across different reference patterns 
        (infants, adolescents, adults). This helps identify how age-dependent nutritional requirements affect the overall protein quality.
        """)

        def plot_aas_comparison(data, protein_source, reference_patterns):
            fig, ax = plt.subplots()
            scores = []
            age_groups = reference_patterns.keys()
            for pattern in reference_patterns:
                current_pattern = reference_patterns[pattern]
                sample_data = data[data['SAMPLE'] == protein_source]
                scores.append(min(sample_data[aa].values[0] / current_pattern[aa] for aa in current_pattern))
            ax.plot(list(age_groups), scores, marker='o')
            ax.set_title(f"AAS Comparison for {protein_source} Across Age Groups")
            ax.set_xlabel('Age Group')
            ax.set_ylabel('AAS')
            st.pyplot(fig)

        selected_sample_for_comparison = st.selectbox("Select a protein source for AAS comparison", data['SAMPLE'].unique())
        plot_aas_comparison(data, selected_sample_for_comparison, reference_patterns)

        # Download button for the output
        st.download_button(label="Download Results", data=data.to_csv(index=False), mime='text/csv')

else:
    st.write("Please upload an Excel file to calculate AAS.")
