# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:22:30 2024

@author: Revathi Nagarajan
This program takes as input a csv file of quality parameters 
obtained from RINGO software and graphs the individual parameters
to understand its daily variation and hence draw conclusions of
the site/station
"""
import pandas as pd
import plotly.io as pio
from dash import Dash,html,dcc,Input,Output
import plotly.express as px
import dash_bootstrap_components as dbc

def get_dropdown_label_from_value(dropdown_value: str):
    value=['MP1','MP2','MP5','CRMP1','CRMP2','CRMP5','CRGf','CRMW','CRIOD' ]  
    label=['Multipath12','Multipath21','Multipath15','Obs per Slip:MP12',
    'Obs per Slip:MP21','Obs per Slip:MP15','Obs per Slip:GF','Obs per Slip:MW',
    'Obs per Slip:IOD']
    for i in range(len(value)):
       if dropdown_value==value[i]:
           return label[i]

pio.renderers.default='browser'

# Plotly and Dash Reading RINGO output 
ringo = pd.read_csv('22ringo.csv')

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
                            meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                            )
server=app.server
# Layout section : Bootstrap               
app.layout = dbc.Container([
# First Row
    dbc.Row([
        dbc.Col([
             dbc.Card(
                  [
                  dbc.CardImg(src="assets/NCG.png" , 
                              className = 'align-self-right',top=True)
                   ],style = {'width':"8rem"}),
                 ]),
        dbc.Col([html.H1("Quality Parameters using RINGO ",
                         className="text-left text-primary")],
                width={'size':9}),
            ], justify='start'),
    html.Br(),  
                 
# Second Row
    dbc.Row([
        dbc.Col([
           html.H3('Choose Site'
                ,style={'font-size':'20px','color':'blue',
                        'text-decoration': 'underline'}
               ),
           dcc.Dropdown(id='site-dropdown',options=ringo['SITE'].unique(),
                                       value='BART'
                                       ) 
            ],width={'size':3}),
        dbc.Col([
            html.H3('Choose Parameter (single)'
                 ,style={'font-size':'20px','color':'blue',
                         'text-decoration': 'underline'}
                ),
            dcc.Dropdown(id='quality-dropdown',options={'MP1':'Multipath12','MP2':
                            'Multipath21','MP5':'Multipath15','CRMP1':'Obs per Slip:MP12',
                            'CRMP2':'Obs per Slip:MP21','CRMP5':'Obs per Slip:MP15',
                            'CRGF':'Obs per Slip:GF','CRMW':'Obs per Slip:MW',
                            'CRIOD':'Obs per Slip:IOD'},value='MP1')
            ],width={'size': 3,'offset':0}),
        dbc.Col([
            html.H3('Choose Constellation (single/multi)'
                 ,style={'font-size':'20px','color':'blue',
                         'text-decoration': 'underline'}
                ),
            dbc.Checklist(
                id="const-check",
                options=[
                    {"label": "GPS", "value": "G"},
                    {"label": "GLONASS", "value": "R"},
                    {"label": "GALILEO", "value": "E"},
                    {"label": "BEIDOU", "value": "C"},
                    {"label": "QZSS", "value": "J"},
                      ],
                value=["G"],inline=True,
                      ),
               ]) 
            ]),
    html.Br(), 
# Third Row        
    dbc.Row([
            dcc.Graph(id='quality-graph',responsive=True)
            ]),
   ])

# Connect the Plotly graph with Dash COmponents    
@app.callback(
    Output('quality-graph','figure'),
    Input('site-dropdown','value'),
    Input('quality-dropdown','value'),
    Input('const-check','value')
)

def update_graph(selected_site,selected_quality,selected_const):
     mytitle=get_dropdown_label_from_value(selected_quality)
     selection=ringo[ringo['SITE']==selected_site]
     selection= selection[selection['CONST'].isin(selected_const)]
# Plotly Express
     line_fig=px.line(selection,template="plotly_dark",
                      
                      x='DOY',y=selected_quality,
                      color='CONST',
                      color_discrete_map={
                     "G": "#FF6347",
                     "R": "#F0E68C",
                     "E":"#1E90FF",#006400" ,
                      "C":"#9ACD32",#FF1493" ,#000080" ,
                      "J":"#BA55D3",#8B008B "
                      },
                      labels={
                     "CONST": "Satellite Constellation",
                     "DOY": "Day Of Year (2023)",
                     "MP1": "Multipath12","MP2":"Multipath21",'MP5':'Multipath15',
                     'CRMP1':'Slips Ratio MP12','CRMP2':'Slips Ratio MP21',
                     'CRGf':'Slips Ratio GF','CRMP5':'Slips Ratio MP15',
                     'CRMW':'Slips Ratio MW', 'CRIOD':'Slips Ratio IOD'
                      },
                      
                      title=f' {mytitle} in {selected_site}',
                      
                      )
     line_fig.update(layout=dict(title=dict(
         x=0.5,
         y=0.9,
         )))
     return line_fig
    
if __name__=='__main__':
    app.run_server(debug=True)
    
    
    
    
  
