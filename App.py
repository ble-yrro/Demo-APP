# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 07:20:51 2020

@author: bleyr
"""

import dash
import dash_auth
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go

import pathlib
import pandas as pd
import numpy as np
from Authentification import Code_auth

#-----------------app authentification----------------------------------------

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server


auth = dash_auth.BasicAuth(app,Code_auth)

#----------------------Create controls-----------------------------------------

epicentre_options = [ {"label": 'Épicentre'+str(i), "value": str(i)}
                      for i in range(1,21) ]
backg_color={'background': '#111111','text': '#7FDBFF'}

#------------------------ Create app layout-----------------------------------

app.layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("ETS.png"),
                                id="plotly-image",
                                style={
                                    "height": "60px",
                                    "width": "auto",
                                    "margin-bottom": "25px",
                                },
                            )
                        ],
                        className="one-third column",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2(
                                        "OUTIL D'ÉVALUATION SISMIQUE DES PONTS",
                                        style={"margin-bottom": "0px", "color":"white"},
                                    )
                                ]
                            )
                        ],
                        className="two-half column",
                        id="title",
                    ),
                ],
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"},
            ),
            
#-------------------débute des zones de dropdown et de la cate epicentre-------

            html.Div(  
                [
                    html.Div(
                        [
                            html.H6("Choisir épicentres",style={"margin-left": "40px", "color":"black"},
                                    className="control_label"),
                            dcc.Dropdown(
                                id="select_epicentre",
                                options=epicentre_options,
                                multi=False,
                                value='1',
                                className="dcc_control",
                            ),
                            html.H6("Choisir magnitudes",style={"margin-left": "40px", "color":"black"}, 
                                    className="control_label"),
                            dcc.Dropdown(
                                id="select_magnitude",
                                options=[
                                    {"label": "Magnitude 5 ", "value": "5"},
                                    {"label": "Magnitude 6", "value": "6"},
                                    {"label": "Magnitude 7", "value": "7"},
                                ],
                                multi=False,
                                value='5',
                                className="dcc_control",
                            ),
                        ],
                        className="pretty_container three columns", 
                        id="cross-filter-options",
                    ), 

#--------------------- debut de  la zone pour la carte des épicentre-------------

                    html.Div( 
                        [
                           
                                html.Div(children=
                                    [ 
                                      dcc.Graph(id="map0",config={'displayModeBar': False, 'scrollZoom': True},
                                  style={'background':'#00FC87','width': '100%','height':'100%'}),
                                             ],
                                    id="countGraphContainer",
                                    className="pretty_container",
                                ),
                        ],
                        id="right-column",
                        className="ten columns",
                        
                    ), 
                ],
                className="row flex-display",
            ),

#-------------------debut blocs carte  et histo médian-------------------------

                  html.Div(
                [
                    html.Div([
                        dcc.Graph(id="map1",config={'displayModeBar': False, 'scrollZoom': True},
                                  style={'width': '100%','height':'100%'}
                          )
                        ],id="right-container-toto",
                        className="pretty_container eight columns",
                        ),
                    html.Div([
                               html.Div([
                                    html.Div([html.H6(id="perte_médian")],
                                        id="perte-med",
                                        className="mini_container ",
                                    ),
                                ],
                                id="right-container-perte-median",
                                className="row container-display",
                            ),
                              html.Div(
                                [dcc.Graph(id="histo1"
                                                               ,)],
                                id="right-container-médian",
                                className="pretty_container",
                            ),
                        ],
                        id="right-column-médian",
                        className="four columns",
                    ),
                ],
                className="row flex-display",
            ),
                  
#-------------------debut blocs faible carte et histo -------------------------

      html.Div(
                [
                    html.Div([ dcc.Graph(id="map2", config={'displayModeBar': False, 'scrollZoom': True},
                                  style={'width': '100%','height':'100%'})
                              ],
                            className="pretty_container eight columns",
                            ),
                    
                    html.Div([
                            html.Div([
                                    html.Div([html.H6(id="perte_faible")],
                                        id="perte-faib",
                                        className="mini_container ",
                                    ),
                                ],
                                id="right-container-perte-faible",
                                className="row container-display",
                            ),
                            html.Div(
                                [dcc.Graph(id="histo2")],
                                id="right-container-faible",
                                className="pretty_container",
                            ),
                        ],
                        id="right-column-faible",
                        className="four columns",
                    ),
                ],
                className="row flex-display",
            ),
      html.Div(
                [
                    html.Div([
                               dcc.Graph(id="map3",config={'displayModeBar': False, 'scrollZoom': True},
                                  style={'width': '100%','height':'100%'}) 
                              ],
                            className="pretty_container eight columns",
                            ),
                    html.Div([
                            html.Div([
                                    html.Div([html.H6(id="perte_élévé"), ],
                                        id="perte-élév",
                                        className="mini_container ",
                                    ),
                                ],
                                id="right-container-perte-élévé",
                                className="row container-display",
                            ),
                            html.Div(
                                [dcc.Graph(id="histo3")],
                                id="right-container-élévé",
                                className="pretty_container",
                            ),
                        ],
                        id="right-column-élévé",
                        className="four columns",
                    ),
                ],
                className="row flex-display",
            ),
        ],
        id="mainContainer",
        style={'backgroundColor': "#192444","display": "flex", "flex-direction": "column"},
    )

@app.callback( 
                Output('map0', 'figure'),
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_epicentre(selected_epicenter,selected_magnitude):
    
    if selected_epicenter is not None and selected_magnitude is not None:

        PATH = pathlib.Path(__file__).parent
        DATA_PATH = PATH.joinpath("data").resolve()
        file_name='epicentre.xlsx'
        df=pd.read_excel(DATA_PATH.joinpath(file_name))
        df['latitude']=np.round(df['latitude'],2)
        df['longitude']=np.round(df['longitude'],2)
        titre='CARTE DES ÉPICENTRES'

#---------------CREATE THE MAP-------------------------------------------------

    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="Nom", height=500,
                     title=titre )
    
    fig.update_layout(mapbox=dict(style='open-street-map',center=dict(lat=46.85, lon=-71.3),
                                  zoom=9),margin={"r":1,"t":40,"l":1,"b":1})
    
    fig.update_traces(mode='markers', marker_size=20,marker_color='red',
                      )
    
    return fig

@app.callback( 
                [Output('map1', 'figure'),Output('histo1', 'figure'),
                 Output("perte_médian", "children")],
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_median(selected_epicenter,selected_magnitude):
    
    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------
       
        PATH = pathlib.Path(__file__).parent
        DATA_PATH = PATH.joinpath("data").resolve()
        file_name='epi'+selected_epicenter+'_M'+selected_magnitude+'_med.xlsx'
        df=pd.read_excel(DATA_PATH.joinpath(file_name))
        df['lat']=np.round(df['lat'],2)
        df['long']=np.round(df['long'],2)
        df["Etat de Dommage"]=df["Damage_State"]
        df["Nom"]=df["Classe_Sismique"]
        
        # df["tri"]=df["lat"]
        
        for i in range(0,len(df)):
            
            df["Nom"][i]="Pont" +str(int(i+1))
            
        df.sort_values(by='MRD_pour')

#----------------CREATE THE COLOR CODE----------------------------------------

        damage_color_code=dict(Aucun='blue',Leger='green',Modere='yellow',Etendu='orange',
                        Complet='red')
        
        titre=" MODÈLE D'ALÉA MÉDIAN (" +'ÉPICENTRE ' +selected_epicenter+ ','+'MAGNITUDE '+selected_magnitude+")"
        
#---------------CREATE THE MAP------------------------------------------------

    fig = px.scatter_mapbox(df, lat="lat", lon="long", 
                            hover_data=['Classe_Sismique',"Etat de Dommage"],
                        color_discrete_map=damage_color_code, color="Etat de Dommage",
                        zoom=9.8, height=550,title=titre)
    
    fig.update_layout(mapbox=dict(style='open-street-map',center=dict(lat=46.85, lon=-71.3),
                                  zoom=9.8),margin={"r":1,"t":40,"l":1,"b":1})
    
    fig.update_traces(mode='markers', marker_size=15)
    
#-----------------------CREATE BAR PLOT----------------------------------------

    x=list(damage_color_code.keys())
    
    y = []
    
    for i in x:
        
        indice= df['Etat de Dommage']==i
        
        nombre=[len(df['Etat de Dommage'][indice])]
        
        if nombre is not None and len(nombre) > 0:
            
            y=np.append(y,nombre)
            
        else:
            y=np.append(y,[0])

    fig1 = go.Figure(data=[go.Bar(x=x, y=y,)]) 

    fig1.update_traces(marker_color=['blue','green','yellow','orange','red'], 
                       marker_line_color=['blue','green','yellow','orange','red'],
                       marker_line_width=1.5, opacity=1)
    
    fig1.update_layout(title_text='Nombre de ponts par état de dommage',
                       xaxis_tickangle=-45,yaxis_title="Nombre de ponts")
    
    pertes=np.round(int(sum(df["Economic_Loss"])/1000),0)

    return fig,fig1,html.P("Pertes Économiques: " +str(pertes) +" K$")


@app.callback( 
                [Output('map2', 'figure'),Output('histo2', 'figure'),
                 Output("perte_faible", "children")],
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_low(selected_epicenter,selected_magnitude):
    
    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------
        
        PATH = pathlib.Path(__file__).parent
        DATA_PATH = PATH.joinpath("data").resolve()
        file_name='epi'+selected_epicenter+'_M'+selected_magnitude+'_low.xlsx'
        df=pd.read_excel(DATA_PATH.joinpath(file_name))
        df['lat']=np.round(df['lat'],2)
        df['long']=np.round(df['long'],2)
        df["Etat de Dommage"]=df["Damage_State"]
        df["Nom"]=df["Classe_Sismique"]
        
        df["tri"]=df["lat"]
        
        for i in range(0,len(df)):
            
            df["Nom"][i]="Pont" +str(int(i+1))

        df.sort_values(by='MRD_pour')
        
#----------------CREATE THE COLOR CODE----------------------------------------

        damage_color_code=dict(Aucun='blue',Leger='green',Modere='yellow',Etendu='orange',
                        Complet='red')
        
        titre=" MODÈLE D'ALÉA FAIBLE (" + 'ÉPICENTRE ' + selected_epicenter + ',' + 'MAGNITUDE ' + selected_magnitude +")"

#---------------CREATE THE MAP------------------------------------------------

    fig = px.scatter_mapbox(df, lat="lat", lon="long", 
                            hover_data=['Classe_Sismique',"Etat de Dommage",],
                            
                            color_discrete_map=damage_color_code, color="Etat de Dommage", 
                            zoom=9.8, height=550)
    
    fig.update_layout(mapbox=dict(style='open-street-map',center=dict(lat=46.85, lon=-71.3),
                    zoom=9.8),margin={"r":1,"t":40,"l":1,"b":1},title=titre)
    
    fig.update_traces(mode='markers', marker_size=15)
    
#-----------------------CREATE BAR PLOT----------------------------------------

    x=list(damage_color_code.keys())
    
    y = []
    
    for i in x:
        
        indice= df['Etat de Dommage']==i
        
        nombre=[len(df['Etat de Dommage'][indice])]
        
        if nombre is not None and len(nombre) > 0:
            
            y=np.append(y,nombre)
            
        else:
            y=np.append(y,[0])

    fig1 = go.Figure(data=[go.Bar(x=x, y=y,)]) #hovertext=[str(y[0]), str(y[1]), str(y[2]),str(y[3]),str(y[4])]

    fig1.update_traces(marker_color=['blue','green','yellow','orange','red'], 
                       marker_line_color=['blue','green','yellow','orange','red'],
                       marker_line_width=1.5, opacity=1)
    
    fig1.update_layout(title_text='Nombre de ponts par état de dommage',
                       xaxis_tickangle=-45,yaxis_title="Nombre de ponts")
    
    pertes=np.round(int(sum(df["Economic_Loss"])/1000),0)
    print(df)
    return fig, fig1,html.P("Pertes Économiques: " +str(pertes) +" K$")


@app.callback( 
                [Output('map3', 'figure'),Output('histo3', 'figure'),
                 Output("perte_élévé", "children")], 
                
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
             )

def update_graph_high(selected_epicenter,selected_magnitude):
    
    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------
        
        PATH = pathlib.Path(__file__).parent
        DATA_PATH = PATH.joinpath("data").resolve()
        file_name='epi'+selected_epicenter+'_M'+selected_magnitude+'_high.xlsx'
        df=pd.read_excel(DATA_PATH.joinpath(file_name))
        
        df['lat']=np.round(df['lat'],2)
        df['long']=np.round(df['long'],2)
        
        df["Etat de Dommage"]=df["Damage_State"]
        df["Nom"]=df["Damage_State"]
        
        df["tri"]=df["lat"]
        
        for i in range(0,len(df)):
            
            df["Nom"][i]="Pont" +str(int(i+1))

        df.sort_values(by='MRD_pour')

#----------------CREATE THE COLOR CODE----------------------------------------

        damage_color_code=dict(Aucun='blue',Leger='green',Modere='yellow',Etendu='orange',Complet='red')

        titre=" MODÈLE D'ALÉA ÉLÉVÉ (" +'ÉPICENTRE ' +selected_epicenter+ ','+'MAGNITUDE '+selected_magnitude+")"
        
        
#---------------CREATE THE MAP------------------------------------------------

    fig = px.scatter_mapbox(df, lat="lat", lon="long", 
                            hover_data=['Classe_Sismique',"Etat de Dommage",],
                        color_discrete_map=damage_color_code, color="Etat de Dommage", 
                        zoom=9.8, height=550,title=titre)
    
    fig.update_layout(mapbox=dict(style='open-street-map',center=dict(lat=46.85, lon=-71.3),
                                  zoom=9.8),margin={"r":1,"t":40,"l":1,"b":0})
    
    fig.update_traces(mode='markers', marker_size=15)

#-----------------------CREATE BAR PLOT----------------------------------------

    x=list(damage_color_code.keys())
    
    y = []
    
    for i in x:
        
        indice= df['Etat de Dommage']==i
        
        nombre=[len(df['Etat de Dommage'][indice])]
        
        if nombre is not None and len(nombre) > 0:
            
            y=np.append(y,nombre)
            
        else:
            y=np.append(y,[0])

    fig1 = go.Figure(data=[go.Bar(x=x, y=y,)]) #hovertext=[str(y[0]), str(y[1]), str(y[2]),str(y[3]),str(y[4])]

    fig1.update_traces(marker_color=['blue','green','yellow','orange','red'], 
                       marker_line_color=['blue','green','yellow','orange','red'],
                       marker_line_width=1.5, opacity=1)
    
    fig1.update_layout(title_text='Nombre de ponts par état de dommage',
                       xaxis_tickangle=-45,yaxis_title="Nombre de ponts")
    
    pertes=np.round(int(sum(df["Economic_Loss"])/1000),0)
    
    return fig,fig1, html.P("Pertes Économiques: " +str(pertes) +" K$")

if __name__ == "__main__":
    app.run_server(debug=False)
