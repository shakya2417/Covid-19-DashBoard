import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go



import pandas as pd
import numpy as np

ts_death=pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
ts_recovered=pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
ts_confirm=pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

ts_confirm.columns=list(ts_confirm.columns)
ts_recovered.columns=list(ts_recovered.columns)
ts_death.columns=list(ts_death.columns)

ts_confirm.columns.values[:2]=['State','Country']
ts_recovered.columns.values[:2]=['State','Country']
ts_death.columns.values[:2]=['State','Country']

last_date=ts_confirm.columns[-1]

df11=ts_confirm.copy()
df22=ts_recovered.copy()
df33=ts_death.copy()

df11.drop('State',axis=True,inplace=True)
df22.drop('State',axis=True,inplace=True)
df33.drop('State',axis=True,inplace=True)

df11.drop(['Lat','Long'],axis=True,inplace=True)
df22.drop(['Lat','Long'],axis=True,inplace=True)
df33.drop(['Lat','Long'],axis=True,inplace=True)


ts_co=df11.groupby('Country',as_index=False).sum()
ts_re=df22.groupby('Country',as_index=False).sum()
ts_de=df33.groupby('Country',as_index=False).sum()

s1=ts_co.transpose().reset_index()
s2=ts_re.transpose().reset_index()
s3=ts_de.transpose().reset_index()

s1.drop(0,inplace=True)
s2.drop(0,inplace=True)
s3.drop(0,inplace=True)


col1=list(ts_co["Country"].unique())
col1.insert(0,'Date')
s1.columns=col1

col2=list(ts_re["Country"].unique())
col2.insert(0,'Date')
s2.columns=col2

col3=list(ts_de["Country"].unique())
col3.insert(0,'Date')
s3.columns=col3

import datetime
s1['Date']=pd.to_datetime(s1.Date).dt.date
datelist1=pd.to_datetime(s1.Date)

s2['Date']=pd.to_datetime(s2.Date).dt.date
datelist2=pd.to_datetime(s2.Date)

s3['Date']=pd.to_datetime(s3.Date).dt.date
datelist3=pd.to_datetime(s3.Date)





options1 = []
for country in s1.columns.values[1:]:
    options1.append({'label':'{}'.format(country), 'value':country})


options2 = []
for country in s2.columns.values[1:]:
    options2.append({'label':'{}'.format(country), 'value':country})

options3 = []
for country in s3.columns.values[1:]:
    options3.append({'label':'{}'.format(country), 'value':country})







trace_11=(go.Scatter(x=s1['Date'],y=s1['India'],
            name='India',line=dict(width = 2,
                                    color = 'rgb(229, 151, 50)'),opacity=0.8))
trace_22=(go.Scatter(x=s2['Date'],y=s2['India'],
            name='India',line=dict(width = 2,
                                    color = 'rgb(229, 151, 50)'),opacity=0.8))

trace_33=(go.Scatter(x=s3['Date'],y=s3['India'],
            name='India',line=dict(width = 2,
                                    color = 'rgb(229, 151, 50)'),opacity=0.8))
layout_line=go.Layout(height = 500,yaxis=dict(
        type='log',autorange=True),yaxis_title='Log Scale',
    margin = dict(t = 0, b = 0, l = 0, r = 0),
    font = dict(color = '#FFFFFF', size = 11),
    template='plotly_dark',hovermode='closest',hoverlabel_font_color='white',hoverlabel_font_size=15)
fig1=go.Figure(data = [trace_11],layout = layout_line)
fig2=go.Figure(data = [trace_22],layout = layout_line)
fig3=go.Figure(data = [trace_33],layout = layout_line)



######mapbox Data
##setting date for url
import pytz
from datetime import date, timedelta
from datetime import datetime
from pytz import timezone
tz_India = pytz.timezone('Asia/Kolkata')
dat=(datetime.now(tz_India)-timedelta(days=1)).strftime('%m-%d-%y')
dat=str(dat)+'20'


df=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+dat+'.csv')


def cases(val):
  if val==0:
    return 0.1
  elif val>=1 and val<5:
    return 4
  elif val>=5 and val<10:
    return 6
  elif val>=10 and val<25:
    return 8
  elif val>=25 and val<100:
    return 10
  elif val>=100 and val<200:
    return 13
  elif val>=200 and val<500:
    return 17
  elif val>=500 and val<1000:
    return 21
  elif val>=1000 and val<2000:
    return 25
  elif val>=2000 and val<5000:
    return 30
  elif val>=5000 and val<20000:
    return 35
  elif val>=20000 and val<27000:
    return 40
  elif val>=27000 and val<38000:
    return 45
  elif val>=38000 and val<50000:
    return 50
  elif val>=50000 and val<65000:
    return 55
  elif val>=65000 and val<85000:
    return 60
  elif val>85000:
    return 65

df['mar_size']=df['Confirmed'].apply(cases)

#mapbox ploting start here..
data=go.Scattermapbox(lon = df['Long_'],lat = df['Lat'],
        
       text = '<b>'+df['Combined_Key']+'</b>'+ ' <br>'+['Confirmed Cases: {}'.format(df['Confirmed'][i]) for i in range(len(df))]+'<br>'+
                       ['Active Cases: {}'.format(df['Active'][i]) for i in range(len(df))]+'<br>'+
                       ['Recovered Cases: {}'.format(df['Recovered'][i]) for i in range(len(df))]+'<br>'+
                       ['Deaths: {}'.format(df['Deaths'][i]) for i in range(len(df))],
        hovertemplate=
        "%{text}<br>"+
        "<extra></extra>",
        hoverlabel_font_color='white',hoverlabel_font_size=20,hoverlabel_bgcolor='#100e17',hoverlabel_bordercolor='cyan',
        
        mode = 'markers',
        marker = dict(
            size = df['mar_size'],
            opacity = 0.6,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle',
            color = '#66CDAA'
        ))
layout=dict(height = 600,
    margin = dict(t = 0, b = 0, l = 0, r = 0),
    font = dict(color = '#FFFFFF', size = 11),
    paper_bgcolor = '#000000',hovermode='closest',mapbox=dict(accesstoken='pk.eyJ1Ijoic2hha3lhMjQxNyIsImEiOiJjazd6d3A4bHkwOWIxM2ZtdTM1NXV6aWJ5In0.5dpYa-G0a58wpEARZELMyg',
                                                  bearing=0,center=go.layout.mapbox.Center(lat=33.8,lon=9.5),
                                                  pitch=5,zoom=2,style ='dark'))
#mapbox plotting ends here.



# tabs data start here.
df.drop(['Lat','Long_','FIPS'],axis=1,inplace=True)
def active(data):
  for i in range(len(data)):
    data['Active'][i]=data['Confirmed'][i]-data['Recovered'][i]-data['Deaths'][i]

active(df)

df_group=df.groupby('Country_Region',as_index=False).sum()





##confirm Bar
import plotly.graph_objs as go
threshold1=int(df_group[df_group['Country_Region']=='India']['Confirmed'].values)
df_con_bar=df_group[df_group['Confirmed']>=threshold1]
trace_con = go.Bar(
    x=df_con_bar['Country_Region'],  # NOC stands for National Olympic Committee
    y=df_con_bar['Confirmed'],
    marker=dict(color=df_con_bar['Confirmed']) # set the marker color to gold
,text=df_con_bar['Confirmed'],textposition='outside',hovertext='<b>'+df_con_bar['Country_Region']+'</b><br>Confirmed Cases:'+df_con_bar['Confirmed'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")

layout_bar=go.Layout(height = 500,
    margin = dict(t = 0, b = 0, l = 0, r = 0),
    font = dict(color = '#FFFFFF', size = 11),
    template='plotly_dark',hovermode='closest',hoverlabel_font_color='white',hoverlabel_font_size=15,)





#Active bar

threshold2=int(df_group[df_group['Country_Region']=='India']['Active'].values)
df_con_bar=df_group[df_group['Confirmed']>=threshold2]
trace_act = go.Bar(
    x=df_con_bar['Country_Region'],  # NOC stands for National Olympic Committee
    y=df_con_bar['Active'],
    marker=dict(color=df_con_bar['Active']) # set the marker color to gold
,text=df_con_bar['Active'],textposition='outside',hovertext='<b>'+df_con_bar['Country_Region']+'</b><br>Active Cases:'+df_con_bar['Active'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")



#Recovered Bar
threshold3=int(df_group[df_group['Country_Region']=='India']['Recovered'].values)
df_con_bar=df_group[df_group['Recovered']>=threshold3]
trace_rec = go.Bar(
    x=df_con_bar['Country_Region'],  # NOC stands for National Olympic Committee
    y=df_con_bar['Recovered'],
    marker=dict(color=df_con_bar['Recovered']) # set the marker color to gold
,text=df_con_bar['Recovered'],textposition='outside',hovertext='<b>'+df_con_bar['Country_Region']+'</b><br>Recovered Cases:'+df_con_bar['Recovered'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")



#Deaths bar
threshold4=int(df_group[df_group['Country_Region']=='India']['Deaths'].values)
df_con_bar=df_group[df_group['Deaths']>=threshold4]
trace_d = go.Bar(
    x=df_con_bar['Country_Region'],  # NOC stands for National Olympic Committee
    y=df_con_bar['Deaths'],
    marker=dict(color=df_con_bar['Deaths']) # set the marker color to gold
,text=df_con_bar['Deaths'],textposition='outside',hovertext='<b>'+df_con_bar['Country_Region']+'</b><br>Deaths Cases:'+df_con_bar['Deaths'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")






#pie Charts starts here....

#confirmed Pie
pie_con=go.Pie(labels=df_group['Country_Region'],
            values=df_group['Confirmed'],
            textposition='inside',hovertext='<b>'+df_group['Country_Region']+'</b><br>Confirmed Cases:'+df_group['Confirmed'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")
layout_pie=go.Layout(height = 500,
    margin = dict(t = 0, b = 0, l = 0, r = 0),
    font = dict(color = '#FFFFFF', size = 11),
    template='plotly_dark',hovermode='closest',hoverlabel_font_color='white',hoverlabel_font_size=15,
    )

#Pie Recovered
pie_rec=go.Pie(labels=df_group['Country_Region'],
            values=df_group['Recovered'],
            textposition='inside',hovertext='<b>'+df_group['Country_Region']+'</b><br>Recovered Cases:'+df_group['Recovered'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")

#pie Active
pie_act=go.Pie(labels=df_group['Country_Region'],
            values=df_group['Active'],
            textposition='inside',hovertext='<b>'+df_group['Country_Region']+'</b><br>Active Cases:'+df_group['Active'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")


pie_d=go.Pie(labels=df_group['Country_Region'],
            values=df_group['Deaths'],
            textposition='inside',hovertext='<b>'+df_group['Country_Region']+'</b><br>Deaths Cases:'+df_group['Deaths'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")


#tabs Styling
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '8px',
    'fontWeight': '90',
    'color':'white',
    'backgroundColor': '#100e17'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#e52f6f',
    'color': 'white',
    'padding': '6px'
}

style_tab_heading={'color':'white',
              'text-align': 'center',
               'margin': '48px 0', 
               'fontFamily': 'system-ui',}

style_span={'font-size':'35px','text-transform':'uppercase','font-weight':'normal',
'color':'white','fontFamily': 'Times New Roman'}

style_dropdown={'width': '500px','fontSize' : '20px','padding-left' : '50px'}

style_intro={'text-align':'center','display':'inline-block'}
style_up={'text-align':'center','display':'inline-block'}






external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


app.layout=html.Div([
    html.Div([


        html.H1(' COVID-19 DashBaord', style={'color':'white','font-size':'50px','font-weight':'300',
              'textAlign': 'center', 'margin': '48px 0', 'fontFamily': 'system-ui'}),
        html.Div([

            html.Div([
              html.Span('Active Cases',className="panel-title",
                  style=style_span),

              
                html.H4(str(df_group['Active'].sum()),style={'color':'white','font-size':'30px'}),


              ],style={'text-align':'center'},className="panel-heading"),

              ],style=style_up),
        

            html.Div([
              html.Span('Confirm Cases',className="panel-title",
                  style=style_span),

              
                html.H4(str(df_group['Confirmed'].sum()),style={'color':'white','font-size':'30px'}),


              ],style=style_up,className="panel-heading"),
        

            html.Div([
              html.Span('Recovered Cases',className="panel-title",
                  style=style_span),

                html.H4(str(df_group['Recovered'].sum()),style={'color':'white','font-size':'30px'}),


              ],style=style_up,className="panel-heading"),

              
        

            html.Div([
              html.Span('Deaths ',className="panel-title",
                  style=style_span),

                html.H4(str(df_group['Deaths'].sum()),style={'color':'white','font-size':'30px'}),

                ],style=style_up,className="panel-heading"),

              
            ],#last one
        className="panel panel-default",style={'background-color':'#100e17','border':'10px #2F4F4F solid'
        ,'margin':'10px'}),



    html.Div([
                  dcc.Graph(id='Mapbox',
                    figure={'data':[data],
                    'layout':layout})
                ],style={'color':'green','border':'10px #2F4F4F solid','border-top':'0px #2F4F4F solid',
                'border-bottom':'0px #2F4F4F solid','margin':'10px'}),

    html.Div([
      dcc.Tabs(id="main tab", children=[
              dcc.Tab(label='Total Confirmed', children=[
                     html.Div([
                        html.H1("Countries with Confirmed Cases Greater than India",style=style_tab_heading),
                          dcc.Graph(id='Confirmed_bar',
                            figure={'data':[trace_con],'layout':layout_bar}
                          ),
                        html.H1('Pie Chart of Confirmed Cases Worldwide',style=style_tab_heading),
                          dcc.Graph(id='Confirmed_Pie',
                            figure={'data':[pie_con],'layout':layout_pie}
                          ),
                    #line charts
                        html.H1('Time Series Plot',style=style_tab_heading),
                        html.Div([
                                  html.H3("Search Countries to Comapre with India",style=style_tab_heading),
                                  dcc.Dropdown(id = 'opt1', options = options1,
                                              value = 'India')
                                      ], style = style_dropdown),
                          dcc.Graph(id = 'plot1', figure = fig1),
                              # dropdown
                              
                              # range slider
                              html.Div([
                                  html.H5("Slide here to Change Time Period",style=style_tab_heading),
                                  dcc.RangeSlider(id = 'slider1',
                                                  #marks =dict(s1['Date']),
                                                  min = 0,
                                                  max = len(s1['Date']),
                                                  value = [1, len(s1['Date'])])
                                      ], style = {'width' : '80%',
                                                  'fontSize' : '20px',
                                                  'padding-left' : '100px',
                                                  'display': 'inline-block'})


                     ]),
                     ],style=tab_style, selected_style=tab_selected_style),

                  
                  dcc.Tab(label='Total Recovered', children=[
                     html.Div([
                        html.H1("Countries with Recovered Cases Greater than India",style=style_tab_heading),
                          dcc.Graph(id='Recovered_bar',
                            figure={'data':[trace_rec],'layout':layout_bar}
                          ),
                        html.H1('Pie Chart of Recovered Cases Worldwide',style=style_tab_heading),
                          dcc.Graph(id='Recovered_Pie',
                            figure={'data':[pie_rec],'layout':layout_pie}),
                        html.H1('Time Series Plot',style=style_tab_heading),
                        html.Div([
                              html.H3("Search Countries to Comapre with India",style=style_tab_heading),
                              dcc.Dropdown(id = 'opt2', options = options2,
                                          value = 'India')
                                  ], style = style_dropdown),
                          dcc.Graph(id = 'plot2', figure = fig2),
                    # dropdown
                          
                          # range slider
                          html.Div([
                              html.H5("Slide here to Change Time Period",style=style_tab_heading),
                              dcc.RangeSlider(id = 'slider2',
                                              #marks =dict(s1['Date']),
                                              min = 0,
                                              max = len(s2['Date']),
                                              value = [1, len(s2['Date'])])
                                  ], style = {'width' : '80%',
                                              'fontSize' : '20px',
                                              'padding-left' : '100px',
                                              'display': 'inline-block'})




                          ])
                     ],style=tab_style, selected_style=tab_selected_style),

                  dcc.Tab(label='Total Deaths', children=[
                     html.Div([
                        html.H1("Countries with Deaths Greater than India",style=style_tab_heading),
                          dcc.Graph(id='Deaths_bar',
                            figure={'data':[trace_d],'layout':layout_bar}
                          ),
                        html.H1('Pie Chart of Deaths Worldwide',style=style_tab_heading),
                          dcc.Graph(id='Deaths_Pie',
                            figure={'data':[pie_d],'layout':layout_pie}
                          ),

                        html.H1('Time Series Plot',style=style_tab_heading),
                        html.Div([
                              html.H3("Search Countries to Comapre with India",style=style_tab_heading),
                                  dcc.Dropdown(id = 'opt3', options = options3,
                                              value = 'India')
                                      ], style = style_dropdown),
                          dcc.Graph(id = 'plot3', figure = fig3),
                           
                              html.H5("Slide here to Change Time Period",style=style_tab_heading),
                              # range slider
                              html.Div([
                                dcc.RangeSlider(id = 'slider3',
                                                  #marks =dict(s1['Date']),
                                                  min = 0,
                                                  max = len(s3['Date']),
                                                  value = [1, len(s3['Date'])])
                                      ], style = {'width' : '80%',
                                                  'fontSize' : '20px',
                                                  'padding-left' : '100px',
                                                  'display': 'inline-block'}),
                                  
                                  


                     ]),

                  ],style=tab_style, selected_style=tab_selected_style),
                  dcc.Tab(label='Total Active', children=[
                     html.Div([
                        html.H2("Countries with Active Cases Greater than India ",style=style_tab_heading),
                          dcc.Graph(id='Active_bar',
                            figure={'data':[trace_act],'layout':layout_bar}
                          ),
                        html.H2('Pie Chart of Active Cases Worldwide',style=style_tab_heading),
                          dcc.Graph(id='Active_Pie',
                            figure={'data':[pie_act],'layout':layout_pie})
                          ])
                     ],style=tab_style, selected_style=tab_selected_style),





              ],style={'color':'black',
          'fontFamily': 'system-ui','font-size':'25px'},
          content_style={
          'borderLeft': '1px solid #d6d6d6',
          'borderRight': '1px solid #d6d6d6',
          'borderBottom': '1px solid #d6d6d6',
          'padding': '4px'},
          parent_style={
          'maxWidth': '1400px',
          'margin': '0 auto'}
      ) #tabs End here

        ],style={'background-color':'#100e17','border':'10px #2F4F4F solid','border-bottom':'0px #2F4F4F solid',
        'margin':'10px'}),
    #intro start here..
    html.Div([

            html.Div([
              html.Span('Created By:',className="panel-title",
                  style={'font-size':'25px','text-transform':'uppercase','font-weight':'normal','color':'white'}),

              
                html.H4('Ramakant Shakya',style={'color':'white','font-size':'20px'}),
                html.H4('(Data Science Enthusiast)',style={'color':'white','font-size':'20px'}),
                


              ],style=style_intro,className="panel-heading"),


            html.Div([
              html.Span('Linkedin',className="panel-title",
                  style={'font-size':'25px','text-transform':'uppercase','font-weight':'normal','color':'white'}),

              

                html.H4(html.A("Linkedin Profile", href='https://www.linkedin.com/in/ramakantshakya/', target="_blank",
                  style={'color':'white','font-size':'20px'})
                  ,),
                html.H4(html.A("Github Profile", href='https://github.com/shakya2417', target="_blank",
                  style={'color':'white','font-size':'20px'})
                  ,),
                


              ],style=style_intro,className="panel-heading"),

              
        

            html.Div([
              html.Span('Any Suggestion',className="panel-title",
                  style={'font-size':'25px','text-transform':'uppercase','font-weight':'normal','color':'white'}),

              
                html.H4('Mait at:',style={'color':'white','font-size':'20px'}),
                html.H4('ramakantshakya@gmail.com',style={'color':'white','font-size':'20px'})
                


              ],style=style_intro,className="panel-heading"),

              
      

            html.Div([
              html.Span('Last Updated ',className="panel-title",
                  style={'font-size':'25px','text-transform':'uppercase','font-weight':'normal','color':'white'}),

              
                html.H4(str(df['Last_Update'][0])+'(Johns Hopkins)',style={'color':'white','font-size':'20px'}),
                html.H4('Data: Johns Hopkins University',style={'color':'white','font-size':'20px'})
                
                  

                ],style=style_intro,className="panel-heading"),

              
            ],#last one of intro
        className="panel panel-default",style={'background-color':'#100e17',
        'border':'10px #2F4F4F solid','margin':'10px'}),


    



        ],style={'background-color':'#2F4F4F'})












# Step 5. Add callback functions
@app.callback(Output('plot1', 'figure'),
             [Input('opt1', 'value'),
             Input('slider1', 'value')])
def update_figure(input1,input2):
    # filtering the data
    st1 = s1[(s1.Date > datelist1[input2[0]]) & (s1.Date < datelist1[input2[1]])]
    # updating the plot
    s1trace_1 = go.Scatter(x = st1.Date, y = st1['India'],
                        name = 'India',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))

    s1trace_2 = go.Scatter(x = st1.Date, y = st1[input1],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    fig1 = go.Figure(data = [s1trace_1, s1trace_2], layout = layout_line)
    return fig1


@app.callback(Output('plot2', 'figure'),
             [Input('opt2', 'value'),
             Input('slider2', 'value')])
def update_figure(input1,input2):
    # filtering the data
    st2 = s2[(s2.Date > datelist2[input2[0]]) & (s2.Date < datelist2[input2[1]])]
    # updating the plot
    s2trace_1 = go.Scatter(x = st2.Date, y = st2['India'],
                        name = 'India',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))

    s2trace_2 = go.Scatter(x = st2.Date, y = st2[input1],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    fig2 = go.Figure(data = [s2trace_1, s2trace_2], layout = layout_line)
    return fig2


@app.callback(Output('plot3', 'figure'),
             [Input('opt3', 'value'),
             Input('slider3', 'value')])
def update_figure(input1,input2):
    # filtering the data
    st3 = s3[(s3.Date > datelist3[input2[0]]) & (s3.Date < datelist3[input2[1]])]
    # updating the plot
    s3trace_1 = go.Scatter(x = st3.Date, y = st3['India'],
                        name = 'India',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))

    s3trace_2 = go.Scatter(x = st3.Date, y = st3[input1],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    fig3 = go.Figure(data = [s3trace_1, s3trace_2], layout = layout_line)
    return fig3


    
if __name__ == '__main__':
    app.run_server()














































