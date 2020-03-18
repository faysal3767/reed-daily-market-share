# Import required modules for the project
import pandas as pd
import numpy as  np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st

# Set a password
password = st.text_input("Please Enter Your Password to Proceed")
if password =="6925tA":

	# Read in actual revenue and market share data
	actualRevenue = pd.read_csv("actualRevenueHeroku.csv")
	marketShare = pd.read_csv("marketShareHeroku.csv")

	# Set date index and transpose. These data are required for plotting
	actualRevenueT = actualRevenue.set_index("date").T
	marketShareT = marketShare.set_index("date").T

	# Select chart type
	chartType = st.radio("Select a chart type",
		("Line Chart (Time Series:Revenue and Market Share by Providers)", 
		"Bar Chart (Revenue and Market Share by Date)", 
		"Comparison Chart (Compares Providers' with One Another)", 
		"Projection Chart (Projects Revenue for Providers)"))

	# Assertion for line chart
	if chartType=="Line Chart (Time Series:Revenue and Market Share by Providers)":
		# Select box to select a provider
		provider = st.sidebar.selectbox(
		"Select a provider",
		 (actualRevenueT.index))

		# Check assertion
		if provider==provider:
			# Create subplots with different y-axis (since revenue scale is much bigger than share scale)for the selected provider.
			# One for actual revenue and the other for market share.
			# Create figure with secondary y-axis
			diffYAxis=make_subplots(
				rows=1,
				cols=1,
				specs=[[{"secondary_y": True}]]
				)

			# Add trace for revenue data
			diffYAxis.add_trace(
			    go.Scatter(
			    x=actualRevenueT.columns, 
			    y=actualRevenueT.loc[provider],
			    name="actualRevenue(£)"),
			    secondary_y=False,
			    )

			# Add trace for market share
			diffYAxis.add_trace(
			    go.Scatter(
			    x=marketShareT.columns, 
			    y=marketShareT.loc[provider], 
			    name="marketShare(%)"),
			    secondary_y=True
			    )

			# Add figure title, dimension, and background color
			diffYAxis.update_layout(
			    title_text=f"Actual Revenue and Market Share for {actualRevenueT.loc[provider].name}",
			    width=1200,
			    height=600,
			    paper_bgcolor="rgb(243, 243, 243)",
			    plot_bgcolor="rgb(243, 243, 243)"
			    )

			# Set x-axis title. Date is common axis here
			diffYAxis.update_xaxes(title_text="Date")

			# Set y-axes titles in bold
			diffYAxis.update_yaxes(title_text="<b>Actual Revenue(£)</b>", secondary_y=False)
			diffYAxis.update_yaxes(title_text="<b>Market Share(%)</b>", secondary_y=True)
			st.plotly_chart(diffYAxis)


	# Assertion for subplots of bar chart
	elif chartType=="Bar Chart (Revenue and Market Share by Date)":
		# Select box to select date
	    date = st.sidebar.selectbox(
	    "Select a date",
	    (actualRevenueT.columns.values))

	    # Check assertin of date
	    if date==date:
	    	# Filter by date. Then sort values by a day's revenue and market share
	    	revenueSorted = actualRevenueT[date].sort_values(ascending=False)
	    	shareSorted = marketShareT[date].sort_values(ascending=False)
	    	# Create two subplots of bar chart
	    	subplotsBar=make_subplots(
	    		rows=1, 
	    		cols=2,
	    		vertical_spacing=0.3,
	    		subplot_titles=("Actual Revenue", "Market Share"))

	    	# Add trace for revenue data
	    	subplotsBar.add_trace(
	    		go.Bar(
	    		y=revenueSorted.index, 
	    		x=np.round(revenueSorted,2),
	    		orientation="h",
	    		text=revenueSorted,
	            textposition="auto", 
	            name="actualRevenue(£)",
	            textfont=dict(family="sans serif",size=14),
	            marker = dict(color=revenueSorted, colorscale = "Rainbow")),
	            row=1,
	            col=1
	            )

	    	# Add trace fot market share
	    	subplotsBar.add_trace(
	    		go.Bar(y=shareSorted.index,
	    		x=np.round(shareSorted,2),
	    		orientation="h",
	    		text=shareSorted,
	            textposition="auto", 
	            name="marketShare(%)",
	            textfont=dict(family="sans serif",size=15),
	            marker=dict(color = shareSorted, colorscale="Rainbow")),
	            row=1,
	            col=2
	            )

	    	# Update the layout. Add title, dimension, and background color
	    	subplotsBar.update_layout(
	    		height=600, 
	    		width=1000, 
	    		title_text=f"{date}: Actual Revenue and Market Share",showlegend=False,
	    		paper_bgcolor="rgb(243, 243, 243)",
	            plot_bgcolor="rgb(243, 243, 243)"
	            )

	    	# Set y-axis title
	    	subplotsBar.update_yaxes(title_text="Provider",row=1, col=1)

	    	# Set x-axes titles in bold
	    	subplotsBar.update_xaxes(title_text="<b>Actual Revenue(£)</b>", row=1, col=1)
	    	subplotsBar.update_xaxes(title_text="<b>Market Share(%)</b>", row=1, col=2)
	    	st.plotly_chart(subplotsBar)

	#Assertion for comparison chart
	elif chartType=="Comparison Chart (Compares Providers' with One Another)":
		# Select 1st provider, the 2nd provider will be compared with.
		firstProvider= st.sidebar.selectbox(
		"Select 1st provider",
		 (actualRevenueT.index))

		# Select 2nd provider
		# Select providers except selected in 1st provider
		# It selects a provider other than selected in 1st provider
		secondProvider= st.sidebar.selectbox(
		"Select 2nd provider",
		 (actualRevenueT.index[actualRevenueT.index!=firstProvider]))

		# Check assertion of providers
		if (firstProvider==firstProvider) & (secondProvider==secondProvider):
			# Create subplots of line chart for comparing two providers
			subplotsCompare = make_subplots(
				rows=2, 
				cols=1, 
				vertical_spacing=0.4,
				subplot_titles=(f"{actualRevenueT.loc[firstProvider].name} vs {actualRevenueT.loc[secondProvider].name} Actual Revenue", 
				f"{marketShareT.loc[firstProvider].name} vs {marketShareT.loc[secondProvider].name} Market Share"
				)
				)

			# Add trace for 1st provider revenue
			subplotsCompare.add_trace(
			    go.Scatter(
			    	x=actualRevenueT.columns, 
			    	y=actualRevenueT.loc[firstProvider], 
			    	name=f"{actualRevenueT.loc[firstProvider].name}: actualRevenue(£)"
			    	),
			    row=1, 
			    col=1
			    )

			# Add trace for 2nd provider revenue
			subplotsCompare.add_trace(
			    go.Scatter(
			    	x=actualRevenueT.columns, 
			    	y=actualRevenueT.loc[secondProvider], 
			    	name=f"{actualRevenueT.loc[secondProvider].name}: actualRevenue(£)"
			    	),
			    row=1,
			    col=1
			    )

			# Add trace for 1st provider market share
			subplotsCompare.add_trace(
			    go.Scatter(
			    	x=marketShareT.columns, 
			    	y=marketShareT.loc[firstProvider], 
			    	name=f"{marketShareT.loc[firstProvider].name}: marketShare(%)"
			    	),
			    row=2,
			    col=1
			    )

			# Add trace for 2nd provider market share
			subplotsCompare.add_trace(
			    go.Scatter(
			    	x=marketShareT.columns, 
			    	y=marketShareT.loc[secondProvider], 
			    	name=f"{marketShareT.loc[secondProvider].name}: marketShare(%)"
			    	),
			    row=2,
			    col=1,
			    )

			# Set y-axes titles in bold
			subplotsCompare.update_yaxes(title_text="<b>Actual Revenue(£)</b>", row=1, col=1)
			subplotsCompare.update_yaxes(title_text="<b>Market Share(%)</b>", row=2, col=1)

			# Update layout of title
			subplotsCompare.update_layout(
				height=600, 
				width=1000,
	    		paper_bgcolor="rgb(243, 243, 243)",
	            plot_bgcolor="rgb(243, 243, 243)"
	            )
			st.plotly_chart(subplotsCompare)


	# Assertion for projection chart
	elif chartType=="Projection Chart (Projects Revenue for Providers)":
		# Add a slider to select days
		daysForProjection = st.slider(
			"Select days for projection",
			min_value=7, 
			max_value=730, 
			step=7
			)  
		# Check assertion for days
		if daysForProjection==daysForProjection:
			# Access the last average columns
			accessAverageColumnRevenue = actualRevenueT.iloc[:,-1]
			# Total revenue after n days = nDays* average after n days
			# Calculate projected revenue after n days depending on slider value
			projectedRevenueAfterNDays = np.round(daysForProjection*accessAverageColumnRevenue)
			# Sort the values to plot
			projectedRevenueAfterNDaysSorted = projectedRevenueAfterNDays.sort_values(ascending=False)

			# Create a bar chart with the projected value
			traceForProjection=go.Bar(
				y=projectedRevenueAfterNDaysSorted.index,
	            x=projectedRevenueAfterNDaysSorted,
	            text=projectedRevenueAfterNDaysSorted,
	            textposition="auto",
	            textfont=dict(family="sans serif",size=12),
	            orientation="h",
	            marker=dict(color=projectedRevenueAfterNDays, colorscale="Rainbow")
	            )

			# Update layout
			layoutForProjection=go.Layout(
				hovermode= "closest", 
				title = f"Projected Revenue for Next {daysForProjection} Days",
	            width=1120,
	            height=750,
	            xaxis = dict(title="<b>Actual Revenue(£)</b>"),
	            yaxis=dict(title="<b>Providers</b>"), font = dict(size=15),
	            paper_bgcolor="rgb(243, 243, 243)",
	            plot_bgcolor="rgb(243, 243, 243)"
	            )
			# Construct the figure object
			plotForProjection = go.Figure(
				data = [traceForProjection], 
				layout = layoutForProjection
				)
			st.plotly_chart(plotForProjection)



else:
    st.subheader('Incorrect Password')
