#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="RESKU Missing in MD Status", layout="wide")

st.title("RESKU Missing in MD Status")

# File uploaders
st.sidebar.header("Upload Files")
power_file = st.sidebar.file_uploader("Upload 'RESKU Missing in MD'File", type=["xlsx"])
mapping_file = st.sidebar.file_uploader("Upload 'Mapping File'", type=["xlsx"])

if power_file and mapping_file:
    df_power = pd.read_excel(power_file)
    df_Mapping = pd.read_excel(mapping_file,sheet_name='Mapping')
    df_Mapping['RE SKU-Mapping file'] = df_Mapping['RE SKU-Mapping file'].astype(str).str.strip()
    df_power['RESKU'] = df_power['RESKU'].astype(str).str.strip()

    def determine_status(row):
        match = df_Mapping[df_Mapping['RE SKU-Mapping file'] == row['RESKU']]
        
        if match.empty:
            return "Not Available in Mapping"
        
        m = match.iloc[0]

        if pd.notnull(m['Id']) and pd.notnull(m['SKU ID']):
            if m['Country'] == row['Country']:
                return "Exist in PMD"
            else:
                return "Not Available for this Country"
        elif pd.isnull(m['Id']) and pd.isnull(m['SKU ID']):
            return "Self-Discovered Product, yet to Onboard"

        return "Not Available in Mapping"

    # Apply the function and create new column
    df_power['Status'] = df_power.apply(determine_status, axis=1)

    # Show the dataframe
    st.subheader("Result with Status")
    st.dataframe(df_power)

    # Save to a buffer instead of disk
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_power.to_excel(writer, index=False)
    output.seek(0)  # Important: move the pointer to the start

    # Download button
    st.download_button(
        label="Download Result as Excel",
        data=output,
        file_name="SKU_Status_Result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Please upload both Excel files to begin.")


# In[ ]:




