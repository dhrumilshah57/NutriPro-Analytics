
import streamlit as st


def main():
    st.title("NutriPro Analytics")

    # App Description
    st.write(
        """
    Welcome to NutriPro Analytics, an advanced tool for analyzing and visualizing the nutritional value of protein sources.

    ### About NutriPro Analytics:
    NutriPro Analytics offers several features designed to streamline protein analysis, including:

    - Automated extraction of protein data from PDFs.
    - Calculation of amino acid scores based on FAO/WHO reference patterns.
    - Machine learning predictions for incomplete nutritional data.

    #### Developer Information:
    NutriPro Analytics is developed using Streamlit, a powerful framework for building interactive web applications with Python.

    **Developers:** Jainish Shah, Durva Brahmbhatt, Dhrumil Shah, Devansh Mehta, Dhwani Sheth
    """
    )


if __name__ == "__main__":
    main()
