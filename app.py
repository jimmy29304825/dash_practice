import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
import pandas as pd
import dash_daq as daq
import datetime
import plotly.express as px
import dash_table

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__)


df = pd.read_csv('./matomo.csv')
df.visitDate = pd.to_datetime(df.visitDate)

df_sum = df.groupby(['visitDate']).sum().reset_index()[[
                 'visitDate', 
                 'itemMessage',
                 'itemPhoneGo',
                 'itemSearch',
                 'itemSearchFollow',
                 'itemView',
                 'itemViewFollow',
                 'communitySaerch',
                 'communityView',
                 'communityViewFollow',
                 'sell',
                 'evertrust',
                 'evertrustFollow',
                 'newsView',
                 'newsFollow',
                 'tvView',
                 'tvFollow',
]]
df_sum = df_sum.melt(id_vars=["visitDate"], 
                     var_name="function", 
                     value_name="count")
df_sum = df_sum.sort_values(by=['visitDate', 'count'], ascending=False)
df_sum.visitDate = pd.to_datetime(df_sum.visitDate)

user_type={'member': 'member',
           'userid': 'userid',
           'all': 'all',
          }
date={
    '1': 0,
    '90': 1,
    '180':2,
    '365': 3,
}

app.layout = html.Div(
    id="big-app-container",
    children=[
     
        html.H1(children='''Matomo Dashboard''', className="section-banner"),  
        html.H2(children='''ver 1.0''', className="section-banner", style = {'text-align':'right',}),  
     
        html.Br(),
     
        html.Div([
            html.H2(children='''Target''', className="section-banner"),  
            dcc.Dropdown(
                id='user_type',
                options=[
                    {'label': 'Members', 'value': 'member'},
                    {'label': 'Non-Members', 'value': 'userid'},
                    {'label': 'All', 'value': 'all'}
                ],
                value='member',
            )],
            style={'width': '50%', 'display': 'inline-block'}
        ),
        
        html.Div([
            html.H2(children='''Times''', className="section-banner"),  
            dcc.Dropdown(
                id='time_range',
                options=[
                    {'label': 'Yesterday', 'value': '1'},
                    {'label': 'Last 3 Month', 'value': '90'},
                   {'label': 'Last Halt Year', 'value': '180'},
                    {'label': 'Last 1 Year', 'value': '365'}
                ],
                value='1',
            )],
            style={'width': '50%', 'display': 'inline-block'}
        ),
        
       html.Br(),
        
        html.Div(
            id="quick-stats",
            className="row",
           children=[
               html.Div(
                   id="card_1",
               ),
               html.Div(
                   id="card_2",
               ),
           ],
        ),
        
        html.Br(),
        
        html.Div([
            html.H2(children='''Devices''', className="section-banner"),  
            dcc.Graph(           
                id="piechart_device",
            )
        ],
            style={'width': '50%', 'display': 'inline-block'}
        ),
        
        html.Div([
            html.H2(children='''Time Period''', className="section-banner"),  
            dcc.Graph(           
                id="barchart_time",
            )
        ],
            style={'width': '50%', 'display': 'inline-block'}
        ),
        
        html.Br(),
        
        html.Div([
            html.H2(children='''Visit's Site''', className="section-banner"),  
            dcc.Graph(           
                id="barchart_site",
            )
        ],
            style={'width': '50%', 'display': 'inline-block'}
        ),
        
        html.Div([
            html.H2(children='''Referer Source''', className="section-banner"),  
            dcc.Graph(           
                id="piechart_refer",
            )
        ],
            style={'width': '50%', 'display': 'inline-block'}
        ),
        
        html.Br(),
        
        html.Div([
            html.H2(children='''Function Usage Rank''', className="section-banner"),  
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in ['function', 'count', 'percent']],
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'function'},
                        'textAlign': 'center',
                    }
                ],
#                 style_as_list_view=True,
                style_header={'backgroundColor': '#323540', 'textAlign': 'center',},
                style_cell={
                    'backgroundColor': '#525769',
                    'color': 'white',
                    "font-size": 20,
                },
                
            )],
            style={'width': '50%', 'display': 'inline-block'},
        ), 
        
        html.Div([
            html.H2(children='''Ads clicks''', className="section-banner"),  
            dcc.Graph(           
                id="piechart_ad",
            )
        ],
            style={'width': '50%', 'display': 'inline-block'}
        ),
        html.Br(),
        html.Br(),
        html.Br(),
    ])


# 總瀏覽會員數
@app.callback(
    Output('card_1', 'children'),
    [Input('user_type', 'value'),
     Input('time_range', 'value')])
def mamber_visit(user_type, time_range):
    time_range = date[time_range]
    dff = df[df.visitDate >= df.visitDate.max() - datetime.timedelta(days=time_range)]
    member_visit = str(len(dff))
    return [
                    html.H2("Users"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value=member_visit,
                        color="#ffffff",
                        backgroundColor="#2b4780",
                        size=50,
                    ),
                ]
   
# 會員總瀏覽次數
@app.callback(
    Output('card_2', 'children'),
    [Input('user_type', 'value'),
     Input('time_range', 'value')])
def visit_sum(user_type, time_range):
    time_range = date[time_range]
    dff = df[df.visitDate >= df.visitDate.max() - datetime.timedelta(days=time_range)]
    visit_times= str(dff.visit_times.sum())
    return [
                    html.H2("Visits"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value=visit_times,
                        color="#ffffff",
                        backgroundColor="#2b4780",
                        size=50,
                    ),
                ]

# 不同裝置使用比例
@app.callback(
    Output('piechart_device', 'figure'),
    [Input('user_type', 'value'),
     Input('time_range', 'value')])
def device_pie(user_type, time_range):
    time_range = date[time_range]
    dff = df[df.visitDate >= df.visitDate.max() - datetime.timedelta(days=time_range)]
    data = [dff['app'].sum(), dff['MobilePhone'].sum(), dff['Desktop'].sum(), ]
    return {
            "data": [
                {
                    "labels": ['App', 'Desktop', 'MobilePhone'],
                    "values": data,
                    "type": "pie",
                    "hole": .3,
                    "marker": {"colors": px.colors.sequential.Cividis, "line": {"color": "white", "width": 0.5}},
                    "hoverinfo": "label+percent+value",
                    "textinfo": "label+percent",
                }
            ],
            "layout": {
                "margin": dict(l=10, r=10, t=10, b=10),
                "showlegend": False,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white", 'size': 15, 'family': "Microsoft JhengHei"},
                "autosize": True,
            },
        }
   
   
# 不同時段的流量
@app.callback(
    Output('barchart_time', 'figure'),
    [Input('user_type', 'value'),
     Input('time_range', 'value')])
def time_bar(user_type, time_range):
    time_range = date[time_range]
    dff = df[df.visitDate >= df.visitDate.max() - datetime.timedelta(days=time_range)]
    data = [
     format(dff['before_work'].sum(), ",d"),  
     format(dff['work_morning'].sum(), ",d"), 
     format(dff['work_evening'].sum(), ",d"), 
     format(dff['after_work'].sum(), ",d"), 
     format(dff['midnight'].sum(), ",d"), 
    ]
    return {
            'data': [
             {'x': ['Before Work', 'Working Morning', 'Working Evening', 'After Work', 'Midnight'],
              'y': data, 
              'type': 'bar',
              'name': 'member',
              'text': data, 
              'textposition': 'outside', 
              'cliponaxis': False,
              'marker': {'color':px.colors.sequential.Cividis, "line": {"color": "white", "width": 1}},
             },
             
            ],
            'layout': {
             "paper_bgcolor": "rgba(0,0,0,0)",
             "plot_bgcolor": "rgba(0,0,0,0)",
             "xaxis": dict(
              showline=False, showgrid=False, zeroline=False
             ),
             "yaxis": dict(
              showgrid=False, showline=False, zeroline=False
             ),
             "autosize": True,
             "font":{"color": "white", "size": 15, 'family': "Microsoft JhengHei"},
            }
        }

   
# 不同來源使用比例
@app.callback(
    Output('piechart_refer', 'figure'),
    [Input('user_type', 'value'),
     Input('time_range', 'value')])
def device_pie(user_type, time_range):
    time_range = date[time_range]
    dff = df[df.visitDate >= df.visitDate.max() - datetime.timedelta(days=time_range)]
    data = [dff['referer_type_direct'].sum(), 
            dff['referer_type_searchEngine'].sum(), 
            dff['referer_type_otherWeb'].sum(), 
            dff['referer_type_campiagn'].sum(),]
    return {
            "data": [
                {
                    "labels": ['direct', 'SearchEngine', 'OtherWeb', 'Campiagn'],
                    "values": data,
                    "type": "pie",
                    "marker": {"colors": px.colors.sequential.Cividis, "line": {"color": "white", "width": 0.5}},
                    "hoverinfo": "label+percent+value",
                    "textinfo": "label+percent",
                }
            ],
            "layout": {
                "margin": dict(l=10, r=10, t=10, b=10),
                "showlegend": False,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white", 'size': 15, 'family': "Microsoft JhengHei"},
                "autosize": True,
            },
        }
   
   
# 不同網站的流量
@app.callback(
    Output('barchart_site', 'figure'),
    [Input('user_type', 'value'),
     Input('time_range', 'value')])
def time_bar(user_type, time_range):
    time_range = date[time_range]
    dff = df[df.visitDate >= df.visitDate.max() - datetime.timedelta(days=time_range)]
    data = [
     format(dff['visit_YC'].sum(), ",d"), 
     format(dff['visit_HF'].sum(), ",d"), 
    ]
    return {
            'data': [
             {'x': ['YC', 'HF'], 
              'y': data, 
#               "orientation": 'h',
              'type': 'bar', 
              'name': 'member', 
              'text': data, 
              'textposition': 'outside', 
              'cliponaxis': False,
              'marker': {'color':px.colors.sequential.Cividis, "line": {"color": "white", "width": 1}},
             },
            ],
            'layout': {
             "paper_bgcolor": "rgba(0,0,0,0)",
             "plot_bgcolor": "rgba(0,0,0,0)",
             "xaxis": dict(
              showline=False, showgrid=False, zeroline=False
             ),
             "yaxis": dict(
              showgrid=False, showline=False, zeroline=False
             ),
             "autosize": True,
             "font":{"color": "white", "size": 15, 'family': "Microsoft JhengHei"},
            }
        }

   # 不同網站的流量
@app.callback(
    Output('table', 'data'),
    [Input('user_type', 'value'),
     Input('time_range', 'value')])
def function_table(user_type, time_range):
    time_range = date[time_range]
    df_sum.visitDate = pd.to_datetime(df_sum.visitDate)
    dff_sum = df_sum[df_sum.visitDate >= df_sum.visitDate.max() - datetime.timedelta(days=time_range)]
    dff_sum =dff_sum.groupby(['function']).sum()
    dff_sum['percent'] = (dff_sum['count'] /  dff_sum['count'].sum() * 100).round(decimals=2)
    dff_sum['percent'] = pd.Series(["{0:.2f}%".format(val) for val in dff_sum['percent']], index = dff_sum.index)
    dff_sum = dff_sum.sort_values(by=['count'], ascending=False)
    dff_sum = dff_sum.reset_index()
    return dff_sum.to_dict('records')

   
# 不同裝置使用比例
@app.callback(
    Output('piechart_ad', 'figure'),
    [Input('user_type', 'value'),
     Input('time_range', 'value')])
def device_pie(user_type, time_range):
    time_range = date[time_range]
    dff = df[df.visitDate >= df.visitDate.max() - datetime.timedelta(days=time_range)]
    data = [dff['adsShow'].sum() - dff['adsClick'].sum(), dff['adsClick'].sum()]
    return {
            "data": [
                {
                    "labels": ['no click', 'click'],
                    "values": data,
                    "type": "pie",
                    'cliponaxis': False,
                    "marker": {"colors": px.colors.sequential.Cividis, "line": {"color": "white", "width": 0.5}},
                    "hoverinfo": "label+percent+value",
                    "textinfo": "label+percent",
                }
            ],
            "layout": {
                "margin": dict(l=10, r=10, t=60, b=10),
                "showlegend": False,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white", 'size': 15, 'family': "Microsoft JhengHei"},
                "autosize": True,
                
            },
        }
   
   
if __name__ == '__main__':
    app.run_server(debug=True)