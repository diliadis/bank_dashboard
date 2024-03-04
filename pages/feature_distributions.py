import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


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

def plot_histograms(df, variable_descriptions_df):
    # Visualize the distribution of the columns in the Soc_Dem dataframe
    st.subheader('Visualize the distribution of the columns in the dataframe')
    column = st.selectbox('Select a column', df.columns[1:])
    
    # Plot the same histogram using st.plotly_chart
    st.subheader('Feature description: '+str(variable_descriptions_df[variable_descriptions_df['Variable'] == column]['Description'].values[0]))
    fig = px.histogram(df, x=column, nbins=20, title=f"Histogram of {column}")
    fig.update_layout(width=600, height=500)
    # st.plotly_chart(fig)
    return fig

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
    
    soc_dem_df = dfs_dict['Soc_Dem']
    products_df = dfs_dict['Products_ActBalance']
    in_out_df = dfs_dict['Inflow_Outflow']
    sales_df = dfs_dict['Sales_Revenues']
    
    Soc_Dem_tab, Products_ActBalance_tab, Inflow_Outflow_tab, Sales_Revenues_tab = st.tabs(['Soc_Dem', 'Products_ActBalance', 'Inflow_Outflow', 'Sales_Revenues'])
    
    with Soc_Dem_tab:
        st.subheader('Soc_Dem')
        st.dataframe(soc_dem_df)
        st.plotly_chart(plot_histograms(soc_dem_df, Soc_Dem_variable_descriptions_df))
    
    with Products_ActBalance_tab:
        st.subheader('Products_ActBalance')
        st.dataframe(products_df)
        st.plotly_chart(plot_histograms(products_df, Products_ActBalance_variable_descriptions_df))
        
    with Inflow_Outflow_tab:
        st.subheader('Inflow_Outflow')
        st.dataframe(in_out_df)
        st.plotly_chart(plot_histograms(in_out_df, Inflow_Outflow_variable_descriptions_df))

    with Sales_Revenues_tab:
        st.subheader('Sales_Revenues')
        st.dataframe(sales_df)
        st.plotly_chart(plot_histograms(sales_df, Sales_Revenues_variable_descriptions_df))

    

        
        
if __name__ == '__main__':
    main()