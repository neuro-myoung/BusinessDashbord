import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("# Sales Dashboard")

sheet = st.file_uploader("Upload Excel Spreadsheet", accept_multiple_files = True)
st.write("#")

st.markdown("## Select Date Range")
ca, cb, cc, cd, ce, cf = st.columns((1, 1, 1, 1, 1, 1))
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

tab1, tab2, tab3 = st.tabs(["Revenue", "Expenses", "Inventory"])

if len(sheet) > 0:
    with tab1:
        st.write("#")
        c1, c2, c3, c4, c5 = st.columns((5, 1,5, 1,5))
            
        if len(sheet) > 1:
            dfList = []
            dfList2 = []
            dfList3 = []
            for i,k in enumerate(sheet):
                df = pd.read_excel(sheet[i], sheet_name="Sales", header = None)
                header_idx = df[df.eq("Item").any(1)].index.values[0]
                footer_idx = df[df.eq("Total").any(1)].index.values[0]-1
                ncol = np.shape(df)[1]
                clean_df = pd.read_excel(sheet[i], sheet_name="Sales", header = header_idx, nrows = footer_idx-header_idx, usecols=range(np.shape(df)[1])[1:])
                dfList.append(clean_df)
                df2 = pd.read_excel(sheet[i], sheet_name="Expenses", header = None)
                header_idx2 = df2[df2.eq("Expense Type").any(1)].index.values[0]
                footer_idx2 = df2[df2.eq("Total").any(1)].index.values[0]-1
                ncol2 = np.shape(df2)[1]
                clean_df2 = pd.read_excel(sheet[i], sheet_name="Expenses", header = header_idx2, nrows = footer_idx2-header_idx2, usecols=range(np.shape(df2)[1])[0:])
                dfList2.append(clean_df2)
                df3 = pd.read_excel(sheet[i], sheet_name="Inventory List", header = None)
                header_idx3 = df3[df3.eq("Inventory ID").any(1)].index.values[0]
                footer_idx3 = df3[df3.eq("Total Value").any(1)].index.values[0]-1
                ncol3 = np.shape(df3)[1]
                clean_df3 = pd.read_excel(sheet[i], sheet_name="Inventory List", header = header_idx3, nrows = footer_idx3-header_idx3, usecols=range(np.shape(df3)[1])[1:])
                dfList3.append(clean_df3)
            clean_df = pd.concat(dfList, axis=0)
            clean_df2 = pd.concat(dfList2, axis=0)
            clean_df3 = pd.concat(dfList3, axis=0)
        else:  
            df = pd.read_excel(sheet[0], sheet_name="Sales", header = None)
            header_idx = df[df.eq("Item").any(1)].index.values[0]
            footer_idx = df[df.eq("Total").any(1)].index.values[0]-1
            ncol = np.shape(df)[1]
            clean_df = pd.read_excel(sheet[0], sheet_name="Sales", header = header_idx, nrows = footer_idx-header_idx, usecols=range(np.shape(df)[1])[1:])
            df2 = pd.read_excel(sheet[0], sheet_name="Expenses", header = None)
            header_idx2 = df2[df2.eq("Expense Type").any(1)].index.values[0]
            footer_idx2 = df2[df2.eq("Total").any(1)].index.values[0]-1
            ncol2 = np.shape(df2)[1]
            clean_df2 = pd.read_excel(sheet[0], sheet_name="Expenses", header = header_idx2, nrows = footer_idx2-header_idx2, usecols=range(np.shape(df2)[1])[0:])
            df3 = pd.read_excel(sheet[0], sheet_name="Inventory List", header = None)
            header_idx3 = df3[df3.eq("Inventory ID").any(1)].index.values[0]
            footer_idx3 = df3[df3.eq("Total Value").any(1)].index.values[0]-1
            ncol3 = np.shape(df3)[1]
            clean_df3 = pd.read_excel(sheet[0], sheet_name="Inventory List", header = header_idx3, nrows = footer_idx3-header_idx3, usecols=range(np.shape(df3)[1])[1:])

        filtyear = ca.selectbox("Select Year:", ["All"] + [str(i) for i in np.unique(clean_df.loc[:, "Sale Date"].dt.year)])
        mList = ["All"] + [months[i-1] for i in np.unique(clean_df.loc[:, "Sale Date"].dt.month)]
    
        filtmonth = cb.selectbox("Select Month:", mList)

        if (filtyear != "All") & (filtmonth == "All"):
            sub_df = clean_df[clean_df["Sale Date"].dt.year == int(filtyear)]
            track_df = clean_df[clean_df["Sale Date"].dt.year == int(filtyear)]
            sub_df2 = clean_df2[clean_df2["Date"].dt.year == int(filtyear)]
            track_df2 = clean_df2[clean_df2["Date"].dt.year == int(filtyear)]
        elif (filtyear != "All") & (filtmonth != "All"):
            sub_df = clean_df[clean_df["Sale Date"].dt.year == int(filtyear)]
            track_df = sub_df
            sub_df = sub_df[sub_df["Sale Date"].dt.month == months.index(filtmonth)+1]
            sub_df2 = clean_df2[clean_df2["Date"].dt.year == int(filtyear)]
            track_df2 = sub_df2
            sub_df2 = sub_df2[sub_df2["Date"].dt.month == months.index(filtmonth)+1]
        else:
            sub_df = clean_df
            track_df = clean_df
            sub_df2 = clean_df2
            track_df2 = clean_df2
        
        c1.markdown("## Analyze Revenue Source")
        srce = c1.selectbox("Select source:", ["Item Type", "Venue"])

        fig = px.pie(sub_df, values='Net Revenue', names=srce, title='Net Revenue by Item Type')

        c1.plotly_chart(fig, theme=None, use_container_width=True)

        c3.markdown("## Revenue Over Time")
        options = c3.multiselect(
            'Select Years to Plot',
            [str(i) for i in np.unique(clean_df.loc[:, "Sale Date"].dt.year)])

        clean_df.loc[:, "year"] = [str(i) for i in clean_df.loc[:, "Sale Date"].dt.year]
        gdf = clean_df.groupby("year")
        maxval = 0
        cmap=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

        fig2 = px.line(
            labels={
                "x": "Month",
                "y": "Net Revenue",
                "year": "year"
             })
        fig2.update_xaxes(
            color="#FFF",
            tickvals = [1,2,3,4,5,6,7,8,9,10,11,12],
            ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            )
        fig2.update_yaxes(color="#FFF")

        for i in range(len(options)):
            t = gdf.get_group(options[i])
            sales_summary = t.groupby(t.loc[:, "Sale Date"].dt.month)['Net Revenue'].sum().reset_index()
            sales_summary.loc[:, "year"] = options[i]

            if np.max(sales_summary.loc[:, "Net Revenue"]) > maxval:
                maxval = np.max(sales_summary.loc[:, "Net Revenue"])


            if i == 0:
                fig2.add_trace(px.line(sales_summary, x=sales_summary.loc[:, "Sale Date"], y=sales_summary.loc[:, "Net Revenue"], markers=True, color=px.Constant(cmap[i]), 
                color_discrete_map="identity").data[0])
                
            else:
                fig2.add_trace(px.line(sales_summary, x=sales_summary.loc[:, "Sale Date"], y=sales_summary.loc[:, "Net Revenue"], markers=True, color=px.Constant(cmap[i]), 
                    color_discrete_map="identity").data[0])
            
        fig2.update_traces(marker_size=15)

        fig2.update_layout(
                {
                'plot_bgcolor': 'rgba(0,0,0,0)',
                },
                yaxis_range=[0,1.1*maxval],
            )

        c3.plotly_chart(fig2, theme=None, use_container_width=True)

        c5.markdown("## Top Selling Items")
        maxn = c5.number_input("How many top sellers would you like to see?", min_value=0, value= 10)

        temp = sub_df.copy(deep=True)
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

        sub_df

        st.markdown("## Gross Revenue to date: " + "$" + str(np.round(np.sum(clean_df.loc[:, "Gross Revenue"]), 2)))
        st.markdown("## :green[Net Revenue to date:] " + "$" + str(np.round(np.sum(clean_df.loc[:, "Net Revenue"]), 2)))
        
    
    with tab2:
        st.write("#")

        c1b, c2b, c3b, c4b, c5b = st.columns((5, 1,5, 1,5))

        c1b.markdown("## Analyze Expense Sources")
        srce = c1b.selectbox("Select Type:", ["Expense Type", "Search Tags"])

        figb = px.pie(sub_df2, values='Amount', names=srce, title='Expenses by Source')

        c1b.plotly_chart(figb, theme=None, use_container_width=True)

        c3b.markdown("## Expenses Over Time")
        optionsb = c3b.multiselect(
            'Select Years to Plot',
            [str(i) for i in np.unique(clean_df2.loc[:, "Date"].dt.year)])

        clean_df2.loc[:, "year"] = [str(i) for i in clean_df2.loc[:, "Date"].dt.year]
        gdfb = clean_df2.groupby("year")
        maxvalb = 0

        fig2b = px.line(
            labels={
                "x": "Month",
                "y": "Expenses",
                "year": "year"
             })
        fig2b.update_xaxes(
            color="#FFF",
            tickvals = [1,2,3,4,5,6,7,8,9,10,11,12],
            ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            )
        fig2b.update_yaxes(color="#FFF")

        for i in range(len(optionsb)):
            tb = gdfb.get_group(optionsb[i])
            sales_summaryb = tb.groupby(tb.loc[:, "Date"].dt.month)['Amount'].sum().reset_index()
            sales_summaryb.loc[:, "year"] = optionsb[i]

            if np.max(sales_summaryb.loc[:, "Amount"]) > maxvalb:
                maxvalb = np.max(sales_summaryb.loc[:, "Amount"])


            if i == 0:
                fig2b.add_trace(px.line(sales_summaryb, x=sales_summaryb.loc[:, "Date"], y=sales_summaryb.loc[:, "Amount"], markers=True, color=px.Constant(cmap[i]), 
                color_discrete_map="identity").data[0])
                
            else:
                fig2.add_trace(px.line(sales_summaryb, x=sales_summaryb.loc[:, "Date"], y=sales_summaryb.loc[:, "Amount"], markers=True, color=px.Constant(cmap[i]), 
                    color_discrete_map="identity").data[0])
            
        fig2b.update_traces(marker_size=15)

        fig2b.update_layout(
                {
                'plot_bgcolor': 'rgba(0,0,0,0)',
                },
                yaxis_range=[0,1.1*maxvalb],
            )
        c3b.plotly_chart(fig2b, theme=None, use_container_width=True)

        c5b.markdown("## Top Expenses")
        maxnb = c5b.number_input("How many top expenses would you like to see?", min_value=0, value= 10)

        clean_df2 = clean_df2.sort_values('Amount', ascending=False)
        fig3b = px.bar(clean_df2, x='Description', y='Amount',
            labels={
                        "Description": "",
                        "Amount": "Amount ($)",
                    })
        fig3b.update_xaxes(tickangle = 90,automargin = True, color="#FFF")
        fig3b.update_yaxes(color="#FFF")
        
        fig3b.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)'
        })
        c5b.plotly_chart(fig3b, theme=None, use_container_width=True)

        clean_df2

        st.markdown("## :red[Total Expenses to date:] " + "$" + str(np.round(np.sum(clean_df2.loc[:, "Amount"]), 2)))


    with tab3:
        c1c, c2c, c3c = st.columns((5, 1, 5,))

        clean_df3.loc[clean_df3.loc[:, "Class"] == "Original", "Name"] = "Original"

        c1c.markdown("## Percent Inventory Value")
        srcec = c1c.selectbox("Select Type:", ["Class", "Name"])

        figc = px.pie(clean_df3, values='Inventory Value', names=srcec, title='Inventory Value by Source')
        figc.update_traces(textposition='inside')
        figc.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

        c1c.plotly_chart(figc, theme=None, use_container_width=True)

        c3c.markdown("## Quantity in stock")
        maxnc = c3c.number_input("How many items would you like to see?", min_value=0, value= 10)
        clean_df3 = clean_df3.sort_values('Quantity in Stock', ascending=False)
        unit_summaryc = clean_df3.head(maxnc)
        fig3c = px.bar(unit_summaryc, x='Name', y='Quantity in Stock',
            labels={
                        "Name": "",
                        "Quantity in Stock": "Quantity (units)",
                    })
        fig3c.update_xaxes(tickangle = 90,automargin = True, color="#FFF")
        fig3c.update_yaxes(color="#FFF")
        
        fig3c.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)'
        })
        c3c.plotly_chart(fig3c, theme=None, use_container_width=True)

        st.markdown("## Flagged for Restock")
        sub_df3 = clean_df3.query("`Quantity in Stock` < `Reorder Level`")
        sub_df3

        st.markdown("## Total Estimated Inventory Value: " + "$" + str(np.round(np.sum(clean_df3.loc[:, "Inventory Value"]), 2)))

       
