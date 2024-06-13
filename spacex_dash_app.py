# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
#print(spacex_df.columns)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[{'label':'All sites', 'value':'ALL'},
                                {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}],
                                value='ALL', placeholder='Place holder here',searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,
                                step=1000,marks={0:'0',2500:'2500',5000:'5000',7500:'7500',10000:'10000'},
                                value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
Input(component_id='site-dropdown',component_property='value'))
def get_pie_chart(entered_site):
    filtered=spacex_df
    if(entered_site=='ALL'):
        fig=px.pie(data_frame=filtered,values='class',names='Launch Site',
        title='Pie chart of succesful landings by launch sites')
        return fig
    else:
        #Filter data
        filtered=filtered[filtered['Launch Site']==entered_site]
        
        #Count total of times that landing is ok or not
        data=filtered['class'].value_counts()
    
        #Reconvert to dataframe with columns
        mydat=data.to_frame().reset_index()
        #print(mydat) #by default value counts call the counting as count
    
        fig=px.pie(data_frame=mydat,values='count',names='class',
        title='Pie chart of succesful and unsuccesful landings in '+str(entered_site))
        

        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
Input(component_id='site-dropdown',component_property='value'),
Input(component_id='payload-slider',component_property='value'))

def getscatterplot(entered_site,payload):
    filtered=spacex_df
    if(entered_site=='ALL'):
        fig=px.scatter(filtered,x="Payload Mass (kg)",y="class",
        color='Booster Version Category')
        return fig
    else:
        #Filter data
        filtered=filtered[filtered['Launch Site']==entered_site]
        fig=px.scatter(filtered,x='Payload Mass (kg)',y='class',
        color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()


# INSIGHTS
#Which site has the largest successful launches?
#KSC LC 39A has the largest succesful number of launches

#Which site has the highest launch success rate?
#CCAFS SLC 40 has the highest launch success rate


#Which payload range(s) has the highest launch success rate?
#2000 -5000 kg

#Which payload range(s) has the lowest launch success rate?
#0 -2000 kg and 6000 kg - 9000 kg

#Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
#launch success rate?
#The FT version has the highest success rate