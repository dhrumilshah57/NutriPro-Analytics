import pandas as pd
import streamlit as st
import plotly.express as px

# Reference patterns for age groups and years
reference_patterns = {
    "1991": {
        "Infants": {'HIS': 26, 'ILE': 46, 'LEU': 93, 'LYS': 66, 'M+C': 42, 'P+T': 72, 'THR': 43, 'TRP': 17, 'VAL': 55},
        "Pre-School (2-5 years)": {'HIS': 19, 'ILE': 28, 'LEU': 66, 'LYS': 58, 'M+C': 25, 'P+T': 63, 'THR': 34, 'TRP': 11, 'VAL': 35},
        "School (10-12 years)": {'HIS': 19, 'ILE': 28, 'LEU': 44, 'LYS': 44, 'M+C': 22, 'P+T': 22, 'THR': 28, 'TRP': 9, 'VAL': 25},
        "Adults": {'HIS': 16, 'ILE': 13, 'LEU': 19, 'LYS': 16, 'M+C': 17, 'P+T': 19, 'THR': 9, 'TRP': 5, 'VAL': 13}
    },
    "2007": {
        "Infants": {'HIS': 18, 'ILE': 31, 'LEU': 63, 'LYS': 52, 'M+C': 25, 'P+T': 46, 'THR': 27, 'TRP': 7.4, 'VAL': 42},
        "Pre-School (2-5 years)": {'HIS': 16, 'ILE': 31, 'LEU': 61, 'LYS': 48, 'M+C': 23, 'P+T': 41, 'THR': 25, 'TRP': 6.6, 'VAL': 40},
        "School (10-12 years)": {'HIS': 16, 'ILE': 30, 'LEU': 60, 'LYS': 48, 'M+C': 23, 'P+T': 41, 'THR': 25, 'TRP': 6.5, 'VAL': 40},
        "Adults": {'HIS': 15, 'ILE': 30, 'LEU': 59, 'LYS': 45, 'M+C': 22, 'P+T': 38, 'THR': 23, 'TRP': 6, 'VAL': 39}
    },
    "2013": {
        "Infants": {'HIS': 21, 'ILE': 55, 'LEU': 96, 'LYS': 69, 'M+C': 33, 'P+T': 94, 'THR': 44, 'TRP': 17, 'VAL': 55},
        "Pre-School (2-5 years)": {'HIS': 20, 'ILE': 32, 'LEU': 66, 'LYS': 57, 'M+C': 27, 'P+T': 52, 'THR': 31, 'TRP': 8.5, 'VAL': 43},
        "Adults": {'HIS': 16, 'ILE': 30, 'LEU': 61, 'LYS': 48, 'M+C': 23, 'P+T': 41, 'THR': 28, 'TRP': 6.6, 'VAL': 40}
    }
}

# Custom colors for limiting amino acids
amino_acid_colors = {
    'HIS': '#FFA500',  # Orange
    'ILE': '#ADD8E6',  # Light Blue
    'LEU': '#00008B',  # Dark Blue
    'LYS': '#008000',  # Green
    'M+C': '#FFFF00',  # Yellow
    'P+T': '#FFC0CB',  # Pink
    'THR': '#800080',  # Purple
    'TRP': '#FF0000',  # Red
    'VAL': '#008080'   # Teal
}

# Streamlit app title
st.title("Amino Acid Score (AAS) Analysis Tool")

st.write("""
This tool calculates the Amino Acid Score (AAS) for various protein samples across different age groups and years based on FAO/WHO reference patterns.
""")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file with amino acid data", type=["xlsx"])

if uploaded_file:
    # Load and process data
    xls = pd.ExcelFile(uploaded_file)
    sheet1 = xls.parse('Sheet1')

    # Combine M+C and P+T and normalize data
    sheet1['M+C'] = sheet1['MET'] + sheet1['CYS']
    sheet1['P+T'] = sheet1['PHE'] + sheet1['TYR']
    sheet1 = sheet1.drop(columns=['MET', 'CYS', 'PHE', 'TYR'])
    normalized_data = sheet1.copy()
    amino_acid_columns = [col for col in normalized_data.columns if col not in ['SAMPLE', 'PROTEIN %', 'M+C', 'P+T']]
    for col in amino_acid_columns + ['M+C', 'P+T']:
        normalized_data[col] = (normalized_data[col] / normalized_data['PROTEIN %']) * 1000

    # Calculate AAS for each year and age group
    results = []
    for year, groups in reference_patterns.items():
        for age_group, pattern in groups.items():
            scores = normalized_data[amino_acid_columns + ['M+C', 'P+T']].div(pd.Series(pattern), axis=1)
            limiting_scores = scores.min(axis=1)
            limiting_amino_acids = scores.idxmin(axis=1)

            temp = normalized_data[['SAMPLE']].copy()
            temp['Year'] = year
            temp['Age Group'] = age_group
            temp['AAS'] = limiting_scores
            temp['Limiting Amino Acid'] = limiting_amino_acids
            results.append(temp)

    result_df = pd.concat(results)

    # Year Selection Dropdown
    st.subheader("Filter Data by Year")
    selected_year = st.selectbox("Select Year", options=sorted(reference_patterns.keys()))

    # Filter data by selected year
    filtered_data = result_df[result_df['Year'] == selected_year]

    # Food Item Selection Dropdown
    st.subheader(f"Select Food Item for Year {selected_year}")
    food_item = st.selectbox("Select Food Item", filtered_data['SAMPLE'].unique())

    # Filter data further for selected food item
    food_data = filtered_data[filtered_data['SAMPLE'] == food_item]

    # Display summary table for the selected food item and year
    st.subheader(f"Amino Acid Scores for {food_item} in {selected_year}")
    item_df_reset = food_data.reset_index(drop=True)

    # Apply custom colors to the table
    def highlight_limiting_amino_acid(row):
        color = amino_acid_colors.get(row['Limiting Amino Acid'], '#FFFFFF')  # Default white
        return [f'background-color: {color}' if col == 'Limiting Amino Acid' else '' for col in row.index]

    styled_table = item_df_reset.style.apply(highlight_limiting_amino_acid, axis=1)
    st.dataframe(styled_table, use_container_width=True)

     # Bar Graph: Age Group vs AAS
    st.subheader("AAS Across Age Groups")
    fig3 = px.bar(
        food_data,
        x="Age Group",
        y="AAS",
        color="Limiting Amino Acid",
        color_discrete_map=amino_acid_colors,
        title="Amino Acid Scores (AAS) Across Age Groups"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Pie Chart of Limiting Amino Acids
    st.subheader("Distribution of Limiting Amino Acids")
    fig2 = px.pie(
        food_data, 
        names="Limiting Amino Acid", 
        title="Limiting Amino Acids Distribution", 
        color="Limiting Amino Acid",
        color_discrete_map=amino_acid_colors
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Download button
    st.download_button(
        label="Download Processed Data",
        data=result_df.to_csv(index=False),
        file_name="amino_acid_scores.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a file to begin analysis.")
