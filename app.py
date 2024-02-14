import pandas as pd
import streamlit as st
from deepmultilingualpunctuation import PunctuationModel
from multiprocessing import Pool
from io import StringIO

# Initialize PunctuationModel
model = PunctuationModel()

# Define function to process each review
def process_review(review):
    if isinstance(review, str):
        return model.restore_punctuation(review)
    else:
        return ""

# Define number of parallel processes
num_processes = 4  # Adjust according to your system's capabilities

# Define Streamlit app
def main():
    st.title("Punctuation Processing App")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        st.write("Original DataFrame:")
        st.write(df)

        # Add progress bar
        progress_bar = st.progress(0)

        # Use multiprocessing Pool to parallelize the process
        with Pool(processes=num_processes) as pool:
            # Apply processing to each review in parallel
            punct_reviews = pool.map(process_review, df['Review'])
        
        # Add punctuated reviews to DataFrame
        df['punct_review'] = punct_reviews

        # Update progress bar
        progress_bar.progress(100)

        # Download processed CSV file
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="Download Processed CSV File",
            data=csv_data,
            file_name="processed_file.csv",
            mime="text/csv"
        )

        st.write("Processed DataFrame:")
        st.write(df)

# Run Streamlit app
if __name__ == "__main__":
    main()
