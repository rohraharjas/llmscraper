import streamlit as st
import pandas as pd
from typing import Optional, Dict
from utils.file_handlers import process_uploaded_file
from services.sheets_service import connect_google_sheet
from services.search_service import perform_web_search
from services.llm_service import process_with_llm
import os
from dotenv import load_dotenv
from groq import Groq
from serpapi import Client

def initialize_session_state():
    """Initialize session state variables"""
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'selected_column' not in st.session_state:
        st.session_state.selected_column = None

def display_data_preview(df: pd.DataFrame):
    """Display a preview of the loaded data"""
    st.subheader("Data Preview")
    st.dataframe(df.head())
    st.write(f"Total rows: {len(df)}")

def handle_file_upload() -> Optional[pd.DataFrame]:
    """Handle file upload and return dataframe"""
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    if uploaded_file is not None:
        return process_uploaded_file(uploaded_file)
    return None

def handle_google_sheets() -> Optional[pd.DataFrame]:
    """Handle Google Sheets connection and return dataframe"""
    sheet_url = st.text_input("Enter Google Sheet URL")
    if sheet_url:
        return connect_google_sheet(sheet_url)
    return None

def process_data(df: pd.DataFrame, column: str, prompt: str) -> Dict:
    """Process data through search and LLM pipeline"""
    groq_client=Groq(api_key=os.getenv("GROQ"))
    serpapi_client = Client(api_key=os.getenv("SERPAPI"))
    results = {}
    progress_bar = st.progress(0)
    
    for idx, entity in enumerate(df[column]):
        # Perform web search
        search_results = perform_web_search(entity, prompt, serpapi_client)
        
        # Process with LLM
        extracted_info = process_with_llm(search_results, prompt, entity, groq_client)
        
        results[entity] = extracted_info
        progress_bar.progress((idx + 1) / len(df))
    
    return results

def main():
    load_dotenv()
    st.title("AI Data Extraction Agent")
    
    initialize_session_state()
    
    # Data Input Section
    st.header("1. Data Input")
    input_method = st.radio("Choose input method:", 
                           ["Upload CSV", "Connect Google Sheet"])
    
    if input_method == "Upload CSV":
        df = handle_file_upload()
    else:
        df = handle_google_sheets()
    
    if df is not None:
        st.session_state.data = df
        display_data_preview(df)
        
        # Column Selection
        st.header("2. Configure Extraction")
        available_columns = df.columns.tolist()
        selected_column = st.selectbox("Select the main column for extraction:",
                                     available_columns)
        st.session_state.selected_column = selected_column
        
        # Query Configuration
        prompt_template = st.text_area(
            "Enter your extraction prompt:",
            "Get me the email address of {entity}"
        )
        
        if st.button("Start Extraction"):
            with st.spinner("Processing data..."):
                results = process_data(df, selected_column, prompt_template)
                st.session_state.results = results
        
        # Results Display
        if st.session_state.results:
            st.header("3. Results")
            results_df = pd.DataFrame.from_dict(
                st.session_state.results, 
                orient='index',
                columns=['Extracted Information']
            )
            st.dataframe(results_df)
            
            # Download Results
            csv = results_df.to_csv(index=True)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="extracted_results.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()