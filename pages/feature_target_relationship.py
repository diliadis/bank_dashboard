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
    
    dfs_dict[selected_featureset_name]
    
    # Visualize the distribution of the columns in the Soc_Dem dataframe
    st.subheader('Visualize the distribution of the columns in the dataframe')
    feature_selection = st.selectbox('Select a feature', dfs_dict[selected_featureset_name].columns[1:])
    # target_selection = st.selectbox('Select a target target', [col for col in sales_df.columns[1:] if 'revenue' in col.lower()])
        
    for target_selection in [col for col in sales_df.columns[1:] if 'revenue' in col.lower()]:
        # Plot the same histogram using st.plotly_chart
        # st.subheader('Feature description: '+str(variable_descriptions_df[variable_descriptions_df['Variable'] == feature_selection]['Description'].values[0]))
        
        df = pd.merge(dfs_dict[selected_featureset_name], sales_df, how="right", on=["Client"])

        #st.dataframe(df)
        
        # plot a scatter plot of the feature against the target
        fig = px.scatter(df[df[target_selection.replace('Revenue', 'Sale')] == 1], x=feature_selection, y=target_selection, title=f"Scatter plot of {feature_selection} against {target_selection}")
        fig.update_layout(width=600, height=500)
        st.plotly_chart(fig)
            
if __name__ == '__main__':
    main()