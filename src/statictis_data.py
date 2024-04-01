import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns

# Preposcessing Data

df = pd.read_csv('../dataset/TAB_Betting_Data.csv')

print(df.head())

print(df.shape)

df.BET_ACCOUNT_NUM_HASH.nunique()

print(df.isnull().sum())

list_cate_turnover = ['FOB_RACING_TURNOVER', 'FOB_SPORT_TURNOVER', 'PARI_RACING_TURNOVER', 'PARI_SPORT_TURNOVER']
for mis_col in list_cate_turnover:
     df[mis_col].fillna(0, inplace=True)
     
print(df.isnull().sum())

print(df.drop_duplicates().shape)

df['DATE_DIM']=pd.to_datetime(df['DATE_DIM'])

dict_nameofday = {'Mon':'Monday', 'Tue':'Tuesday', 'Wed':'Wednesday', 'Thu': 'Thursday', 'Fri':'Friday', 'Sat':'Saturday', 'Sun':'Sunday'}
dict_gender = {'M':'Male', 'F':'Female', 'U':'Undefined'}

df['DAY_OF_WEEK_FULL']=df['DAY_OF_WEEK'].apply(lambda x:dict_nameofday[x])
df['GENDER_FULL']=df['GENDER'].apply(lambda x:dict_gender[x])

print(df.shape)

# EDA
df_customer = df.drop_duplicates(subset='BET_ACCOUNT_NUM_HASH')[['GENDER_FULL', 'AGE_BAND']]

# Distribution of gender
fig = px.histogram(df_customer, x='GENDER_FULL')
fig.show()

# Distrubution of age
fig = px.histogram(df_customer, x='AGE_BAND')
fig.show()

# Distribution of total turnover through datetime
df_total_turnover = df.groupby(df['DATE_DIM'])['TOTAL_TURNOVER'].sum().reset_index()
top_dates = df_total_turnover.sort_values(by=['TOTAL_TURNOVER'],ascending=False).head(3)
vals = []
for tgl, tot in zip(top_dates["DATE_DIM"], top_dates["TOTAL_TURNOVER"]):
    tgl = tgl.strftime("%d %B")
    val = "%d (%s)"%(tot, tgl)
    vals.append(val)
top_dates['tgl'] = vals
top_dates

fig = go.Figure(data=go.Scatter(x=df_total_turnover['DATE_DIM'].astype(dtype=str), 
                                y=df_total_turnover['TOTAL_TURNOVER'],
                                marker_color='black', text="totals"))
fig.update_layout({"title": 'Total Turnover of customer from 2021-01-01 to 2022-12-31',
                   "xaxis": {"title":"Time"},
                   "yaxis": {"title":"Total turnovers"},
                   "showlegend": False})
fig.add_traces(go.Scatter(x=top_dates['DATE_DIM'], y=top_dates['TOTAL_TURNOVER'],
                          textposition='top left',
                          textfont=dict(color='#233a77'),
                          mode='markers+text',
                          marker=dict(color='red', size=6),
                          text = top_dates["tgl"]))
fig.show()

# Revenue from each betting method
from dash import Dash, dcc, html, Input, Output

df_turnover_by_month = df.groupby(df['DATE_DIM'].dt.to_period('M'))[['FOB_RACING_TURNOVER', 'FOB_SPORT_TURNOVER', 'PARI_RACING_TURNOVER', 'PARI_SPORT_TURNOVER']].sum().reset_index()

options = []
for col in list_cate_turnover:
    options.append({'label':'{}'.format(col, col), 'value':col})

app = Dash(__name__)
app.layout = html.Div([
    html.H4('Turnover betting method analysis'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select betting:"),
    dcc.Dropdown(
        id="betting",
    #     options=[
    #    {'label': 'Fixed-odds Racing events', 'value': 'FOB_RACING_TURNOVER'},
    #    {'label': 'Fixed-odds Sports events', 'value': 'FOB_SPORT_TURNOVER'},
    #    {'label': 'Pari-mutuel Racing betting', 'value': 'PARI_RACING_TURNOVER'},
    #    {'label': 'Pari-mutuel Sports betting', 'value': 'PARI_SPORT_TURNOVER'}
    #     ],
        options=options,
        value="FOB_RACING_TURNOVER",
        clearable=False,
    ),
])

@app.callback(
    Output("time-series-chart", "figure"), 
     Input("betting", "value"))

def display_time_series(betting):
    global df_turnover_by_month
    fig = px.line(df_turnover_by_month, x=df_turnover_by_month['DATE_DIM'].astype(dtype=str), y=df_turnover_by_month[betting]).update_layout(
    xaxis_title="Date")
    return fig

app.run_server(debug=True)

df_turnover = df.groupby(df['DATE_DIM'])[['FOB_RACING_TURNOVER', 'FOB_SPORT_TURNOVER', 'PARI_RACING_TURNOVER', 'PARI_SPORT_TURNOVER']].sum().reset_index()
fig = px.line(df_turnover, x="DATE_DIM", y=df_turnover.columns,
              hover_data={"DATE_DIM": "|%B %d, %Y"},
              title='Turnover of each betting method')
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y",
    ticklabelmode="period")
fig.show()

# Distribution for total turnover of each betting method
df_turnover = df.groupby(df['DATE_DIM'])[['FOB_RACING_TURNOVER', 'FOB_SPORT_TURNOVER', 'PARI_RACING_TURNOVER', 'PARI_SPORT_TURNOVER']].sum().reset_index()
fig = px.line(df_turnover, x="DATE_DIM", y=df_turnover.columns,
              hover_data={"DATE_DIM": "|%B %d, %Y"},
              title='Total turnover value of each betting method')
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y",
    ticklabelmode="period")
fig.show()

# Distribution for number of betting method betted by customer through datetime
count_by_betting = df.groupby(df['DATE_DIM'])[['FOB_RACING_TURNOVER', 'FOB_SPORT_TURNOVER', 'PARI_RACING_TURNOVER', 'PARI_SPORT_TURNOVER']].count().reset_index()
fig = px.line(count_by_betting, x="DATE_DIM", y=count_by_betting.columns,
              hover_data={"DATE_DIM": "|%B %d, %Y"},
              title='Number of betting method')
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y",
    ticklabelmode="period")
fig.show()

