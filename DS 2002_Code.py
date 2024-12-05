# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:39:28 2024

@author: cakus
"""

# OPENING THE DATA
import pandas as pd
import numpy as np

file_path = r"C:\Users\cakus\Downloads\Sentencing_Data_Imported.csv"
data_raw = pd.read_csv(file_path)

columns_to_keep = ['AGE', 'MONSEX', 'NEWRACE', 'NEWEDUC', 'WGT1', 'BASEHI', 
                   'IS924C', 'NEWCNVTN', 'CITIZEN', 'COMBDRG2', 'SENTTCAP', 
                   'XCRHISSR', 'OFFGUIDE', 'CIRCDIST', 'CITIZEN', 'MONCIRC', 'SENTRNGE']
data1 = data_raw[columns_to_keep]


# FILTERING THE DATA
# only COMBDRG 1 and 2 (powder &coke). XCRHISSR == 6, OFFGUIDE == 10

data = data1[(data1['XCRHISSR'] == 6) & 
             (data1['OFFGUIDE'] == 10) & 
             (data1['COMBDRG2'].isin([1, 2]))]

# Subsetting into coke and powder only
data = data[data['COMBDRG2'].isin([1, 2])]

# 100,000 GRAMS ONLY
# Filter out rows where WGT1 > 100,000
data = data[data['WGT1'] <= 100000]

# MAPPING RELEVANT CATEGORICAL VARIABLES
race_mapping = {
    1: "White",
    2: "Black",
    3: "Hispanic",
    6: "Other"
}

newcnvtn_mapping = {
    0: "Plea",
    1: "Trial"
}

drug_type_mapping = {
    1: "Powder Cocaine",
    2: "Crack Cocaine"
}

education_mapping = {
    1: "Less than H.S. graduate",
    3: "H.S. graduate",
    5: "Some college",
    6: "College graduate"
}

moncirc_mapping = {
    0: "DC",
    1: "First",
    2: "Second",
    3: "Third",
    4: "Fourth",
    5: "Fifth",
    6: "Sixth",
    7: "Seventh",
    8: "Eighth",
    9: "Ninth",
    10: "Tenth",
    11: "Eleventh"
}

IS924C_mapping = {
    0: "No Enhancement Charge",
    1: "Weapon Enhancement Charge"
}

MONSEX_mapping = {
    0: "Male",
    1: "Female"
}

# Apply the mappings to the dataset
data['NEWRACE'] = data['NEWRACE'].map(race_mapping).astype('category')
data['NEWCNVTN'] = data['NEWCNVTN'].map(newcnvtn_mapping).astype('category')
data['COMBDRG2'] = data['COMBDRG2'].map(drug_type_mapping).astype('category')
data['NEWEDUC'] = data['NEWEDUC'].map(education_mapping).astype('category')
data['MONCIRC'] = data['MONCIRC'].map(moncirc_mapping).astype('category')
data['IS924C'] = data['IS924C'].map(IS924C_mapping).astype('category')
data['MONSEX'] = data['MONSEX'].map(MONSEX_mapping).astype('category')

# Testing that the mapping is applied correctly; looking for unbalanced proportio
## data['NEWRACE'].value_counts()
## data['NEWEDUC'].value_counts()
## data['NEWCNVTN'].value_counts()
## data['COMBDRG2'].value_counts()
## data['MONCIRC'].value_counts()
## data['IS924C'].value_counts()
## data['SENTRNGE'].value_counts()

# Dropping missing values
data = data.dropna()
## print(data.isnull().sum())
















# HTML FILE
import plotly.io as pio
import plotly.express as px

# Calculate counts for each group
count_data = (
    data.groupby(['COMBDRG2', 'NEWCNVTN'])
    .size()
    .reset_index(name='Count')
)

# Create the grouped bar graph
fig1 = px.bar(
    count_data,
    x='COMBDRG2',
    y='Count',
    color='NEWCNVTN',
    title='Counts of Guilty Pleas and Trials by Cocaine Type',
    labels={
        'COMBDRG2': 'Cocaine Type',
        'NEWCNVTN': 'Plea/Trial Status',
        'Count': 'Count'
    },
    barmode='group',  # Grouped bar chart
    color_discrete_map={'Plea': 'blue', 'Trial': 'red'}  # Custom colors
)

# Add counts as text on top of the bars
fig1.update_traces(
    text=count_data['Count'],
    textposition='outside'
)

# Update layout for better aesthetics
fig1.update_layout(
    xaxis_title="Cocaine Type",
    yaxis_title="Count",
    legend_title="Plea/Trial Status",
    template='plotly_white'
)







# PLOTLY 2: Sentence Length vs Quantity of Cocaine, Grouped by Plea/Trial Status
fig2 = px.scatter(
    data,
    x='WGT1',  # Quantity of cocaine
    y='SENTTCAP',  # Sentence length
    animation_frame='NEWRACE',  # Race slider/animation
    color='NEWCNVTN',  # Plea/Trial status
    hover_data={
        'AGE': True,
        'SENTTCAP': True,
        'WGT1': True,
        'COMBDRG2': True  # Display as hover data
    },
    labels={
        'WGT1': 'Quantity of Cocaine (Grams)',
        'SENTTCAP': 'Sentence Length (Months)',
        'NEWCNVTN': 'Plea/Trial Status',
        'COMBDRG2': 'Cocaine Type',
        'AGE': 'Age'
    },
    title='Sentence Length vs Quantity of Cocaine, Grouped by Plea/Trial Status',
    color_discrete_map={'Plea': 'blue', 'Trial': 'red'}  # Custom colors
)
fig2.update_layout(
    xaxis_title='Quantity of Cocaine (Grams)',
    yaxis_title='Sentence Length (Months)',
    legend_title='Plea/Trial Status',
    template='plotly_white'
)










# PLOTLY 3

# Calculate median sentence length for each group
education_data = (
    data.groupby(['NEWEDUC', 'NEWCNVTN'])
    .agg(Median_Sentence=('SENTTCAP', 'median'))
    .reset_index()
)

# Create the grouped bar chart
fig3 = px.bar(
    education_data,
    x='NEWEDUC',  # Education level
    y='Median_Sentence',  # Median sentence length
    color='NEWCNVTN',  # Plea/Trial Status
    title='Median Sentence Length by Education Level, Grouped by Plea/Trial Status',
    labels={
        'NEWEDUC': "Defendant's Education Level",
        'Median_Sentence': 'Median Sentence (Months)',
        'NEWCNVTN': 'Plea/Trial Status'
    },
    barmode='group',  # Grouped bar chart
    color_discrete_map={'Plea': 'blue', 'Trial': 'red'}  # Custom colors
)

# Add hover information for only the Median Sentence
fig3.update_traces(
    hovertemplate=(
        "<b>Median Sentence (Months):</b> %{y}<extra></extra>"
    )
)

# Update layout for better aesthetics
fig3.update_layout(
    xaxis_title="Defendant's Education Level",
    yaxis_title="Median Sentence (Months)",
    legend_title="Plea/Trial Status",
    template='plotly_white'
)

# Show the plot
fig3.show()




# PLOTLY 4
import plotly.graph_objects as go

# Filter the data for Plea and Trial
data_plea = data[data['NEWCNVTN'] == 'Plea']
data_trial = data[data['NEWCNVTN'] == 'Trial']

# Create the violin plot
fig4 = go.Figure()

# Add trace for Plea Deal
fig4.add_trace(go.Violin(
    x=data_plea['NEWEDUC'],
    y=data_plea['SENTTCAP'],
    legendgroup='Plea Deal',  # Link the legend for Plea Deal
    scalegroup='Plea Deal',   # Link the scale for Plea Deal
    name='Plea Deal',
    side='negative',          # Plot on the left side
    box=dict(visible=True),   # Show boxplot
    meanline=dict(visible=True),  # Show mean line
    line_color='cornflowerblue'
))

# Add trace for Trial
fig4.add_trace(go.Violin(
    x=data_trial['NEWEDUC'],
    y=data_trial['SENTTCAP'],
    legendgroup='Trial',  # Link the legend for Trial
    scalegroup='Trial',   # Link the scale for Trial
    name='Trial',
    side='positive',      # Plot on the right side
    box=dict(visible=True),   # Show boxplot
    meanline=dict(visible=True),  # Show mean line
    line_color='red'
))

# Update layout
fig4.update_layout(
    title='Distribution of Sentence Length by Education, Grouped by Plea/Trial Status',
    xaxis_title='Education Level',
    yaxis_title='Sentence Length (Months)',
    violingap=0,         # No gap between violins
    violingroupgap=0,    # No group gap
    violinmode='overlay' # Overlay violins
)



# PLOT 5 (technically the first - Histogram)
fig5 = px.histogram(
    data,
    x='SENTTCAP',  # Column for sentence length
    title='Distribution of Sentence Length',
    labels={'SENTTCAP': 'Sentence Length (Months)'},
    nbins=22,  # Number of bins
    template='plotly_white'  # Aesthetic template
)

# Update layout for better visualization
fig5.update_layout(
    xaxis_title='Sentence Length (Months)',
    yaxis_title='Count',
    bargap=0.1  # Gap between bars
)










# Save each figure's HTML content
html_fig1 = pio.to_html(fig1, full_html=False)
html_fig2 = pio.to_html(fig2, full_html=False)
html_fig3 = pio.to_html(fig3, full_html=False)
html_fig4 = pio.to_html(fig4, full_html=False)
html_fig5 = pio.to_html(fig5, full_html=False)


# Combine the HTML content into one file
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Combined Plotly Graphs</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Histogram</h1>
    {html_fig5}
    <h1>Plot 1</h1>
    {html_fig1}
    <h1>Plot 2</h1>
    {html_fig2}
    <h1>Plot 3</h1>
    {html_fig3}
    <h1>Plot 4</h1>
    {html_fig4}
</body>
</html>
"""




# Write to an HTML file
output_path = "combined_plots.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"HTML file saved to {output_path}")

