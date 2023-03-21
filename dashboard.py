import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("# Sales Dashboard")

sheet = st.file_uploader("Upload Excel Spreadsheet")
st.write("#")
st.markdown("## Filter Data")
ca, cb, cc = st.columns((1, 1, 1))
st.write("#")
c1, c2, c3, c4, c5 = st.columns((5, 1,5, 1,5))


if sheet is not None:
    df = pd.read_excel(sheet, sheet_name="Sales", header = None)  
    header_idx = df[df.eq("Item").any(1)].index.values[0]
    footer_idx = df[df.eq("Total").any(1)].index.values[0]-1

    ncol = np.shape(df)[1]
    months = ["January", "February", "March", "April", "June", "July", "August", "September", "October", "November", "December"]

    clean_df = pd.read_excel(sheet, sheet_name="Sales", header = header_idx, nrows = footer_idx-header_idx, usecols=range(np.shape(df)[1])[1:])
    
    filtcol1 = ca.selectbox("Filter Column:", ["None","Item Type", "Venue", "Sale Date"])
    if filtcol1 == "None":
        filtrule1 = cb.selectbox("Filter Rule:", [])
    elif filtcol1 in ["Item Type", "Venue"]:
        filtrule1 = cb.selectbox("Filter Rule:", ["is", "is not"])
    else:
        filtrule1 = cb.selectbox("Filter Rule:", ["equals", "less than", "greater than"])

    if filtcol1 == "None":
        filtby1 = cc.selectbox("Filter by:", [])
    elif filtcol1 in ["Item Type", "Venue"]:
        filtby1 = cc.selectbox("Filter by:", np.unique(clean_df.loc[:, filtcol1]))
    else:
        filtby1 = cc.selectbox("Filter by:", months)
    
    # Analyze Revenue Source
    c1.markdown("## Analyze Revenue Source")


    srce = c1.selectbox("Select source:", ["Item Type", "Venue"])
    clean_df
    

    fig = px.pie(clean_df, values='Net Revenue', names=srce, title='Net Revenue by Item Type')

    c1.plotly_chart(fig, theme=None, use_container_width=True)

    c3.markdown("## Revenue Over Time")
    split_check = c3.checkbox("Split Items", value=False, key=None)
  
    sales_summary = clean_df.groupby(clean_df.loc[:, "Sale Date"].dt.month)['Net Revenue'].sum().reset_index()
    fig2 = px.line(sales_summary, x=sales_summary.loc[:, "Sale Date"], y=sales_summary.loc[:, "Net Revenue"], markers=True, 
    labels={
                     "x": "Month",
                     "y": "Net Revenue",
                 })

    fig2.update_layout(
        {
        'plot_bgcolor': 'rgba(0,0,0,0)',
    },
    yaxis_range=[0,1.1*np.max(sales_summary.loc[:, "Net Revenue"])]
    )
    fig2.update_xaxes(
        color="#FFF",
        tickvals = [1,2,3,4,5,6,7,8,9,10,11,12],
        ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        )
    fig2.update_yaxes(color="#FFF")
    fig2.update_traces(marker_size=15)

    c3.plotly_chart(fig2, theme=None, use_container_width=True)

    c5.markdown("## Top Selling Items")
    maxn = c5.number_input("How many top sellers would you like to see?", min_value=0, value= 10)

    temp = clean_df.copy(deep=True)
    temp.loc[temp.loc[:, "Venue"] == "Commission", "Item"] = "Commission"
    unit_summary = temp.groupby(temp.loc[:,"Item"])['Number Sold'].sum().reset_index()
    unit_summary = unit_summary.sort_values('Number Sold', ascending=False)
    unit_summary = unit_summary.head(maxn)
    fig3 = px.bar(unit_summary, x='Item', y='Number Sold',
        labels={
                     "Item": "",
                     "Number Sold": "Number Sold",
                 })
    fig3.update_xaxes(tickangle = 90,automargin = True, color="#FFF")
    fig3.update_yaxes(color="#FFF")
    
    fig3.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)'
    })
    c5.plotly_chart(fig3, theme=None, use_container_width=True)

    st.markdown("## Net Revenue to date: " + "$" + str(np.round(np.sum(clean_df.loc[:, "Net Revenue"]), 2)))
   