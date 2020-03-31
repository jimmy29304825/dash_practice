import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
import pandas as pd
import dash_daq as daq
import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./matomo.csv')
df.visitDate = pd.to_datetime(df.visitDate)
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
        html.Div([
           html.Div(children='''請選擇對象''', className="section-banner"),  
           dcc.Dropdown(
               id='user_type',
               options=[
                   {'label': '會員', 'value': 'member'},
                   {'label': '非會員', 'value': 'userid'},
                   {'label': '全部', 'value': 'all'}
               ],
               value='member'
           )],
           style={'width': '50%', 'display': 'inline-block'}
        ),

       html.Div([
           html.Div(children='''請選擇時間區間''', className="section-banner"),  
           dcc.Dropdown(
               id='time_range',
               options=[
                   {'label': '前一天', 'value': '1'},
                   {'label': '近三個月', 'value': '90'},
                   {'label': '近半年', 'value': '180'},
                   {'label': '近一年', 'value': '365'}
               ],
               value='1'
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
#                    style={'width': '50%', 'display': 'inline-block'}
               ),
               html.Div(
                   id="card_2",
#                    style={'width': '50%', 'display': 'inline-block'}
               ),
           ],
       ),

       html.Br(),

       html.Div([
           html.Div(children='''不同裝置的瀏覽次數''', className="section-banner"),  
           dcc.Graph(           
               id="piechart_device",
              )
          ],
           style={'width': '50%', 'display': 'inline-block'}
          ),

       html.Div([
           html.Div(children='''不同時段的瀏覽次數''', className="section-banner"),  
           dcc.Graph(           
               id="barchart_time",
              )
          ],
           style={'width': '50%', 'display': 'inline-block'}
          ),

       html.Br(),

       html.Div([
           html.Div(children='''不同網站的瀏覽次數''', className="section-banner"),  
           dcc.Graph(           
               id="barchart_site",
              )
          ],
           style={'width': '50%', 'display': 'inline-block'}
          ),

       html.Div([
           html.Div(children='''不同來源的瀏覽次數''', className="section-banner"),  
           dcc.Graph(           
               id="piechart_refer",
              )
          ],
           style={'width': '50%', 'display': 'inline-block'}
          ),    
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
                    html.P("造訪會員數"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value=member_visit,
                        color="#92e0d3",
                        backgroundColor="#1e2130",
                        size=30,
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
                    html.P("會員總造訪次數"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value=visit_times,
                        color="#92e0d3",
                        backgroundColor="#1e2130",
                        size=30,
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
                    "marker": {"line": {"color": "white", "width": 0.5}},
                    "hoverinfo": "label+percent+value",
                    "textinfo": "label+percent",
                }
            ],
            "layout": {
                "margin": dict(l=10, r=10, t=10, b=10),
                "showlegend": False,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white", 'size': 15},
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
    data = [dff['before_work'].sum(), dff['work_morning'].sum(), dff['work_evening'].sum(), dff['after_work'].sum(), dff['midnight'].sum()]
    return {
            'data': [
                {'x': ['上班前', '上午', '下午', '下班後', '凌晨'], 'y': data, 'type': 'bar', 'name': 'member', 'text': data, 'textposition': 'outside'},
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
             "font":{"color": "pink", "size": 15},
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
                    "marker": {"line": {"color": "white", "width": 0.5}},
                    "hoverinfo": "label+percent+value",
                    "textinfo": "label+percent",
                }
            ],
            "layout": {
                "margin": dict(l=10, r=10, t=10, b=10),
                "showlegend": False,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white", 'size': 15},
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
    data = [dff['visit_YC'].sum(), dff['visit_HF'].sum(), ]
    return {
            'data': [
                {'x': ['永慶', '好房'], 'y': data, 'type': 'bar', 'name': 'member', 'text': data, 'textposition': 'outside'},
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
             "font":{"color": "pink", "size": 15},
            }
        }

   
   
if __name__ == '__main__':
    app.run_server(debug=True)