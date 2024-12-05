
# Amino Acid Score (AAS) Analysis Tool

![AAS Analysis Tool](https://github.com/dhrumilshah57/NutriPro-Analytics/blob/main/MainImage.png)

*A web-based application for analyzing amino acid profiles of protein samples using FAO/WHO reference patterns.*

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Data Format](#data-format)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

The **Amino Acid Score (AAS) Analysis Tool** calculates the Amino Acid Score (AAS) for various protein samples across multiple years and age groups based on FAO/WHO reference patterns. This tool helps evaluate the nutritional adequacy of protein sources for specific populations.

## Features

- **File Upload:** Upload `.xlsx` files with amino acid data.
- **Data Normalization:** Converts amino acid values to mg/g protein.
- **AAS Calculation:** Determines Amino Acid Scores for selected years and age groups.
- **Interactive Filters:**
  - Select years (e.g., 1991, 2007, 2013).
  - Choose specific food items for detailed analysis.
- **Visualizations:**
  - **Pie Chart:** Displays limiting amino acid distributions with custom colors.
  - **Bar Graph:** Shows AAS across age groups.
- **Styled Tables:** Highlights limiting amino acids with predefined color coding.
- **Download Results:** Save processed data as CSV files.

## Demo

![AAS Analysis Tool Demo](https://github.com/yourusername/aas-analysis-tool/blob/main/images/demo.gif)

*Include an interactive GIF or screenshots demonstrating the app.*

## Installation

### Prerequisites

Ensure you have **Python 3.7 or higher** installed. [Download Python](https://www.python.org/downloads/).

### Steps

1. Clone the Repository:

   ```bash
   git clone https://github.com/dhrumilshah57/NutriPro-Analytics
   ```

2. Create a Virtual Environment (Optional but Recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Application:

   ```bash
   streamlit run app.py
   ```

   *Replace `app.py` with your main script name if different.*

## Usage

1. **Upload Your Data:**
   - Use the "Upload an Excel file with amino acid data" button to select your `.xlsx` file.

2. **Filter by Year:**
   - Choose a reference year (e.g., 1991, 2007, 2013) using the dropdown.

3. **Select Food Item:**
   - Pick a specific food item for detailed analysis.

4. **View Results:**
   - **Table:** Shows AAS and limiting amino acid for selected year and food item.
   - **Pie Chart:** Displays distribution of limiting amino acids.
   - **Bar Graph:** Plots AAS across different age groups.

5. **Download Results:**
   - Save processed data using the "Download Processed Data" button.

## Data Format

The uploaded `.xlsx` file should contain the following structure in `Sheet1`:

![AAS Analysis Table](https://github.com/dhrumilshah57/NutriPro-Analytics/blob/main/MainImage2.png)

### Columns:

- **SAMPLE:** Name of the protein sample.
- **PROTEIN %:** Protein percentage of the sample.
- **Amino Acids (HIS, ILE, LEU, LYS, MET, CYS, PHE, TYR, THR, TRP, VAL):** Amounts of each amino acid in mg.

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add Your Feature"
   ```

4. Push to the branch:

   ```bash
   git push origin feature/YourFeatureName
   ```

5. Open a Pull Request for review.


## Acknowledgements

- [Streamlit](https://streamlit.io/) for its intuitive web app framework.
- [Plotly](https://plotly.com/) for interactive data visualizations.
- [FAO/WHO](https://www.fao.org/) for reference patterns used in AAS calculations.

---
