# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:22:30 2024

@author: revna
"""
import pandas as pd
import plotly.io as pio
from dash import Dash,html,dcc,Input,Output
import plotly.express as px
import dash_bootstrap_components as dbc

pio.renderers.default='browser'

#Plotly and Dash
ringo = pd.read_csv('22ringo.csv')

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.layout = dbc.Container([
#First Row
    dbc.Row([
        dbc.Col([
             dbc.Card(
                  [
                  dbc.CardImg(src="assets/NCG.png" , 
                              className = 'align-self-right',top=True)
                   ],style = {'width':"6rem"}),
                 ]),
        
        dbc.Col([html.H1("Quality Parameters using RINGO ",
                         className="text-left text-primary")],
                width={'size':9}),
        
        
          ], justify='start'),
           
         
# Second Row
    dbc.Row([
        dbc.Col([
           dcc.Dropdown(id='site-dropdown',options=ringo['SITE'].unique(),
                                       value='BART') 
            ],width={'size':3}),
        dbc.Col([
            dcc.Dropdown(id='quality-dropdown',options={'MP1':'Multipath12','MP2':
                            'Multipath21','MP5':'Multipath15','CRMP1':'Slips Ratio MP12',
                            'CRMP2':'Slips Ratio MP21','CRGf':'Slips Ratio GF',
                            'CRMP5':'Slips Ratio MP15','CRMW':'Slips Ratio MW',
                            'CRIOD':'Slips Ratio IOD'},value='MP1')
            ],width={'size': 4,'offset':0}),
           
            
        dbc.Col([
             dcc.Checklist(
                         id='const-check', value=['G','R'],                     # used to identify component in callback
                         options={'G':'GPS','R':'GLONASS','E':'GALELIO','C':'BIDEO',
                                  'J':'QUZZ'},inline=True,inputStyle={"margin-left": "20px"}),                    
                         ]),
                   ],justify='start'),

              
        html.Br(), 
        
    # dbc.Row([
    #        dbc.Col([
    #            html.P("Select Constelation",style={"textDecoration":"underline"})
    #                ],width={'size': 3}),
    #        dbc.Col([
    #     dcc.Checklist(
    #                 id='const-check', value=['GPS'],                     # used to identify component in callback
    #                 options={'G':'GPS','R':'GLONASS','E':'GALELIO','C':'BIDEO',
    #                          'J':'QUZZ'},inline=True,inputStyle={"margin-left": "20px"}),                    
    #                 ]),
    #     ],justify='start'),
    
    
    dbc.Row([
        dcc.Graph(id='quality-graph')
               
        ],justify='start')
   ],fluid=True) 
    
@app.callback(
    Output('quality-graph','figure'),
    Input('site-dropdown','value'),
    Input('quality-dropdown','value'),
    Input('const-check','value')
)

def update_graph(selected_site,selected_quality,selected_const):
     siteRingo=ringo[ringo['SITE']==selected_site]
     filtered_site= siteRingo[siteRingo['CONST'].isin(selected_const)]
     
     line_fig=px.line(filtered_site,template="plotly_dark",
                      x='DOY',y=selected_quality,
                      color='CONST',
                      labels={
                     "CONST": "Satellite Constellation",
                     "DOY": "Day Of Year (2023)",
                     "MP1": "Multipath12"
                 },
                      title=f'{selected_quality} in {selected_site}'
                      )
     return line_fig
    
    
if __name__=='__main__':
    app.run_server(debug=True)
    
    
    
    
  
