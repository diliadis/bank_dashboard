import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import random
import string

@st.cache_data
def load_dataset(file_dir):
    if file_dir.endswith('.xlsx'):
        # the excel file has multiple sheets, so we need all the sheets in different dataframes
        return pd.read_excel(file_dir, sheet_name=None)
        # return pd.read_excel(file_dir)
    elif file_dir.endswith('.csv'):
        return pd.read_csv(file_dir)
    else:
        raise ValueError('File type not supported')    

def main():
    
    with st.sidebar:
        st.image('images/KBC.jpg', width=300)
    
    st.title('KBC data science dashboard task')
    dfs_dict = load_dataset('Task_Data_Scientist_Dataset.xlsx')
    
    variable_descriptions_df = dfs_dict['Description']
    
    # iterate the Sheet columnn and for every cell that is not empty, copy the value from the previous row
    for i in range(1, len(variable_descriptions_df)):
        if pd.isna(variable_descriptions_df['Sheet'][i]):
            variable_descriptions_df.loc[i, 'Sheet'] = variable_descriptions_df['Sheet'][i-1]
    
    Soc_Dem_variable_descriptions_df = variable_descriptions_df[variable_descriptions_df['Sheet'] == 'Soc_Dem']
    Products_ActBalance_variable_descriptions_df = variable_descriptions_df[variable_descriptions_df['Sheet'] == 'Products_ActBalance']
    Inflow_Outflow_variable_descriptions_df = variable_descriptions_df[variable_descriptions_df['Sheet'] == 'Inflow_Outflow']
    Sales_Revenues_variable_descriptions_df = variable_descriptions_df[variable_descriptions_df['Sheet'] == 'Sales_Revenues']
    
    # create a dictionary out of the variable_descriptions_df
    
    # soc_dem_df = dfs_dict['Soc_Dem']
    # products_df = dfs_dict['Products_ActBalance']
    # in_out_df = dfs_dict['Inflow_Outflow']
    sales_df = dfs_dict['Sales_Revenues']
        
    selected_featureset_name = st.selectbox('Select a feature set', ['Soc_Dem', 'Products_ActBalance', 'Inflow_Outflow', 'Sales_Revenues'])
    selected_target_name = st.selectbox('Select a target', sales_df.columns[1:])
    
    upper_target_threshold = st.number_input('Insert the upper threshold for the target', value=sales_df[selected_target_name].max())
    lower_target_threshold = st.number_input('Insert the lower threshold for the target', value=sales_df[selected_target_name].min())

    df = pd.merge(dfs_dict[selected_featureset_name], sales_df, how="right", on=["Client"])

    # plot a scatter plot of the feature against the target
    if 'Revenue' in selected_target_name:
        st.info('revenue mode')
        temp_term = selected_target_name.replace('Revenue', 'Sale')
        temp_df = df[(df[temp_term] == 1) & ((df[selected_target_name]<=upper_target_threshold) & (df[selected_target_name]>=lower_target_threshold))]
        st.info(len(temp_df))
        st.dataframe(temp_df)
        fig = px.scatter_matrix(temp_df, dimensions=dfs_dict[selected_featureset_name].columns[1:], color=selected_target_name, color_continuous_scale=px.colors.sequential.Viridis)
        fig.update_traces(diagonal_visible=False)
        fig.update_traces(showupperhalf=False)
        st.info(selected_target_name)
    else:
        fig = px.scatter_matrix(df, dimensions=dfs_dict[selected_featureset_name].columns[1:], color=selected_target_name)
    fig.update_layout(width=1200, height=1000)
    st.plotly_chart(fig)
            
if __name__ == '__main__':
    main()