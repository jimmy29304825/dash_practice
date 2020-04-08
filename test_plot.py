import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime


df = pd.read_csv('./matomo_new.csv')  # 讀取資料
df['訪問日期'] = pd.to_datetime(df['訪問日期'])  # 轉換日期格式
df_yesterday = df.query("訪問日期 == '%s'" % df['訪問日期'].max())


# YC
df_yesterday_function_HF = df_yesterday[df_yesterday['訪問網站'] == '好房網'].iloc[:, [1,2,33,35,37,38,41,43,45]].groupby(['訪問網站', '使用裝置']).sum().reset_index()
df_yesterday_function_HF = df_yesterday_function_HF.melt(id_vars=['訪問網站', '使用裝置'], var_name="功能", value_name="人次")
df_yesterday_function_HF = df_yesterday_function_HF.sort_values(by=['人次','訪問網站', '使用裝置', '功能'], ascending=False).reset_index(drop=True)


fig = go.Figure()
fig.add_trace(go.Bar(
    y=df_yesterday_function_HF['功能'].unique(),
    x=df_yesterday_function_HF[df_yesterday_function_HF['使用裝置'] == 'app']['人次'],
    name='app',
    orientation='h',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))
fig.add_trace(go.Bar(
    y=df_yesterday_function_HF['功能'].unique(),
    x=df_yesterday_function_HF[df_yesterday_function_HF['使用裝置'] == 'MobilePhone']['人次'],
    name='MobilePhone',
    orientation='h',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))
fig.add_trace(go.Bar(
    y=df_yesterday_function_HF['功能'].unique(),
    x=df_yesterday_function_HF[df_yesterday_function_HF['使用裝置'] == 'Desktop']['人次'],
    name='Desktop',
    orientation='h',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))

fig.update_layout(barmode='stack')
fig.show()