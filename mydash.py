import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pytz
from datetime import date, timedelta
from datetime import datetime
from pytz import timezone



#State data ends here

##setting date for url

tz_India = pytz.timezone('Asia/Kolkata')
dat=(datetime.now(tz_India)-timedelta(days=2)).strftime('%m-%d-20%y')
#dat=str(dat)+'20'




#importing time series data
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






#time series plot
trace_11=(go.Scatter(x=s1['Date'],y=s1['India'],
            name='India',line=dict(width = 2,
                                    color = 'rgb(229, 151, 50)'),opacity=0.8))
trace_22=(go.Scatter(x=s2['Date'],y=s2['India'],
            name='India',line=dict(width = 2,
                                    color = 'rgb(229, 151, 50)'),opacity=0.8))

trace_33=(go.Scatter(x=s3['Date'],y=s3['India'],
            name='India',line=dict(width = 2,
                                    color = 'rgb(229, 151, 50)'),opacity=0.8))
layout_line=go.Layout(height = 500,xaxis=dict(fixedrange=True),
  yaxis=dict(fixedrange=True,
        type='log',autorange=True),yaxis_title='Log Scale',
    margin = dict(t = 0, b = 0, l = 0, r = 0),
    font = dict(color = '#FFFFFF', size = 11),
    template='plotly_dark',hovermode='closest',hoverlabel_font_color='white',hoverlabel_font_size=15)
fig1=go.Figure(data = [trace_11],layout = layout_line)
fig2=go.Figure(data = [trace_22],layout = layout_line)
fig3=go.Figure(data = [trace_33],layout = layout_line)



#Reading data again
df=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+dat+'.csv')
#df=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/07-04-2020.csv')
last_updat=df['Last_Update'][0]
df.drop(['FIPS','Admin2','Last_Update','Incident_Rate','Case_Fatality_Ratio'],axis=1,inplace=True)




def active(data):
  for i in range(len(data)):
    data['Active'][i]=data['Confirmed'][i]-data['Recovered'][i]-data['Deaths'][i]

active(df)

def cases(val):
  if val==0:
    return 0.1
  elif val>=1 and val<100:
    return 2
  elif val>=100 and val<200:
    return 4
  elif val>=200 and val<300:
    return 6
  elif val>=300 and val<500:
    return 8
  elif val>=500 and val<1000:
    return 10
  elif val>=1000 and val<5000:
    return 12
  elif val>=5000 and val<15000:
    return 15
  elif val>=15000 and val<35000:
    return 18
  elif val>=35000 and val<60000:
    return 23
  elif val>=60000 and val<90000:
    return 27
  elif val>=90000 and val<110000:
    return 32
  elif val>=110000 and val<150000:
    return 36
  elif val>=150000 and val<200000:
    return 39
  elif val>=200000 and val<250000:
    return 44
  elif val>=250000 and val<350000:
    return 47
  elif val>=350000 and val<450000:
    return 50
  elif val>=450000 and val<500000:
    return 54
  elif val>=500000 and val<650000:
    return 60
  elif val>=650000 and val<750000:
    return 65
  elif val>750000:
    return 70
df['mar_size']=df['Confirmed'].apply(cases)
df['Confirmed']=df['Confirmed'].astype(int)
df['Recovered']=df['Recovered'].astype(int)
df['Active']=df['Active'].astype(int)
df['Deaths']=df['Deaths'].astype(int)

#State data
df_State=df[df['Country_Region']=='India']


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
                                                  bearing=0,center=go.layout.mapbox.Center(lat=22.9,lon=78.6),
                                                  pitch=5,zoom=2,style ='dark'),worldviews='in')
#mapbox plotting ends here.



# tabs data start here.
#df.drop(['Lat','Long_'],axis=1,inplace=True)


#df_group=df.groupby('Country_Region',as_index=False).sum()





## Bar plots
#confirm bar
trace_con = go.Bar(
    x=df_State['Province_State'], 
    y=df_State['Confirmed'],
    marker=dict(color=df_State['Confirmed']) 
,text=df_State['Confirmed'],textposition='outside',hovertext='<b>'+df_State['Province_State']+'</b><br>Confirmed Cases:'+df_State['Confirmed'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")


layout_bar=go.Layout(height = 500,
  xaxis=dict(fixedrange=True,categoryorder='total ascending'),
  yaxis=dict(fixedrange=True),
    margin = dict(t = 0, b = 0, l = 0, r = 0),
    font = dict(color = '#FFFFFF', size = 11),
    template='plotly_dark',hovermode='closest',hoverlabel_font_color='white',hoverlabel_font_size=15,)





#Active bar


trace_act = go.Bar(
    x=df_State['Province_State'], 
    y=df_State['Active'],
    marker=dict(color=df_State['Active']) 
,text=df_State['Active'],textposition='outside',hovertext='<b>'+df_State['Province_State']+'</b><br>Active Cases:'+df_State['Active'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")




#Recovered Bar
trace_rec = go.Bar(
    x=df_State['Province_State'], 
    y=df_State['Recovered'],
    marker=dict(color=df_State['Recovered']) 
,text=df_State['Recovered'],textposition='outside',hovertext='<b>'+df_State['Province_State']+'</b><br>Recovered Cases:'+df_State['Recovered'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")




#Deaths bar
trace_d = go.Bar(
    x=df_State['Province_State'], 
    y=df_State['Deaths'],
    marker=dict(color=df_State['Deaths']) 
,text=df_State['Deaths'],textposition='outside',hovertext='<b>'+df_State['Province_State']+'</b><br>Deaths:'+df_State['Deaths'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")






#pie Charts starts here....

#confirmed Pie
pie_con=go.Pie(labels=df_State['Province_State'],
            values=df_State['Confirmed'],
            textposition='inside',hovertext='<b>'+df_State['Province_State']+'</b><br>Confirmed Cases:'+df_State['Confirmed'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")
layout_pie=go.Layout(height = 500,
    margin = dict(t = 0, b = 0, l = 0, r = 0),
    font = dict(color = '#FFFFFF', size = 11),
    template='plotly_dark',hovermode='closest',hoverlabel_font_color='white',hoverlabel_font_size=15,
    )

#Pie Recovered
pie_rec=go.Pie(labels=df_State['Province_State'],
            values=df_State['Recovered'],
            textposition='inside',hovertext='<b>'+df_State['Province_State']+'</b><br>Recovered Cases:'+df_State['Recovered'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")

#pie Active
pie_act=go.Pie(labels=df_State['Province_State'],
            values=df_State['Active'],
            textposition='inside',hovertext='<b>'+df_State['Province_State']+'</b><br>Active Cases:'+df_State['Active'].apply(str),
hovertemplate=
        "%{hovertext}<br>"+
        "<extra></extra>")


pie_d=go.Pie(labels=df_State['Province_State'],
            values=df_State['Deaths'],
            textposition='inside',hovertext='<b>'+df_State['Province_State']+'</b><br>Deaths :'+df_State['Deaths'].apply(str),
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

style_span={'font-size':'35px','font-weight':'normal',
'color':'white','fontFamily': 'Times New Roman'}

style_dropdown={'width': '500px','fontSize' : '20px','padding-left' : '50px'}

style_intro={'text-align':'center','width':'300px','display':'inline-block'}
style_up={'text-align':'center','width':'300px','display':'inline-block'}






#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets =['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


app.layout=html.Div([
    html.Div([


            
                html.H1(' COVID-19 India DashBaord', style={'color':'white','font-size':'50px','font-weight':'300',
              'textAlign': 'center', 'margin': '48px 0', 'fontFamily': 'system-ui'}),
                html.H3('Last Updated:'+last_updat, style={'color':'white','font-weight':'300',
              'text-align': 'right','position':'top','margin': '48px 0', 'fontFamily': 'system-ui'}),
                
        
        dbc.Row([

          dbc.Col(
            html.Div([
              html.Span('Active Cases',className="panel-title",
                  style=style_span),

              
                html.H2(str(df_State['Active'].apply(int).sum()),style={'color':'white','font-size':'20px'}),


              
              ],style=style_up),),
        
          dbc.Col(
            html.Div([
              html.Span('Confirm Cases',className="panel-title",
                  style=style_span),
              
                html.H2(str(df_State['Confirmed'].apply(int).sum()),style={'color':'white','font-size':'20px'}),


              ],style=style_up,className="panel-heading"),),
        
          dbc.Col(

            html.Div([
              html.Span('Recovered Cases',className="panel-title",
                  style=style_span),

                html.H2(str(df_State['Recovered'].apply(int).sum()),style={'color':'white','font-size':'20px'}),


              ],style=style_up,className="panel-heading"),),

              
            dbc.Col(

            html.Div([
              html.Span('Deaths ',className="panel-title",
                  style=style_span),

                html.H2(str(df_State['Deaths'].apply(int).sum()),style={'color':'white','font-size':'20px'}),

                ],style=style_up,className="panel-heading"),),
            ]),

              
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
                        html.H1("Confirmed Cases in India",style=style_tab_heading),
                          dcc.Graph(id='Confirmed_bar',
                            figure={'data':[trace_con],'layout':layout_bar}
                          ),

                    #line charts
                        html.H1('Time Series Plot',style=style_tab_heading),
                        html.Div([
                                  html.H2("Search Countries to Compare with India",style=style_tab_heading),
                                  dcc.Dropdown(id = 'opt1', options = options1,
                                              value = 'India')
                                      ], style = style_dropdown),
                          dcc.Graph(id = 'plot1', figure = fig1),
                              # dropdown
                              
                              # range slider
                              html.Div([
                                  html.H2("Slide here to Change Time Period",style=style_tab_heading),
                                  dcc.RangeSlider(id = 'slider1',
                                                  #marks =dict(s1['Date']),
                                                  min = 0,
                                                  max = len(s1['Date']),
                                                  value = [1, len(s1['Date'])])
                                      ], style = {'width' : '80%',
                                                  'fontSize' : '20px',
                                                  'padding-left' : '100px',
                                                  'display': 'inline-block'}),
                          #pie chart
                        html.H1('Pie Chart of Confirmed Cases in India',style=style_tab_heading),
                          dcc.Graph(id='Confirmed_Pie',
                            figure={'data':[pie_con],'layout':layout_pie}
                          ),


                     ]),
                     ],style=tab_style, selected_style=tab_selected_style),

                  
                  dcc.Tab(label='Total Recovered', children=[
                     html.Div([
                        html.H1(" Recovered Cases in India",style=style_tab_heading),
                          dcc.Graph(id='Recovered_bar',
                            figure={'data':[trace_rec],'layout':layout_bar}
                          ),
                        
                        html.H1('Time Series Plot',style=style_tab_heading),
                        html.Div([
                              html.H3("Search Countries to Compare with India",style=style_tab_heading),
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
                                              'display': 'inline-block'}),
                          html.H1('Pie Chart of Recovered Cases in India',style=style_tab_heading),
                          dcc.Graph(id='Recovered_Pie',
                            figure={'data':[pie_rec],'layout':layout_pie}),




                          ])
                     ],style=tab_style, selected_style=tab_selected_style),

                  dcc.Tab(label='Total Deaths', children=[
                     html.Div([
                        html.H1(" Deaths in India",style=style_tab_heading),
                          dcc.Graph(id='Deaths_bar',
                            figure={'data':[trace_d],'layout':layout_bar}
                          ),
                        

                        html.H1('Time Series Plot',style=style_tab_heading),
                        html.Div([
                              html.H2("Search Countries to Compare with India",style=style_tab_heading),
                                  dcc.Dropdown(id = 'opt3', options = options3,
                                              value = 'India')
                                      ], style = style_dropdown),
                          dcc.Graph(id = 'plot3', figure = fig3),
                           
                              html.H2("Slide here to Change Time Period",style=style_tab_heading),
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
                            html.H1('Pie Chart of Deaths in India',style=style_tab_heading),
                          dcc.Graph(id='Deaths_Pie',
                            figure={'data':[pie_d],'layout':layout_pie}
                          ),
                                  
                                  


                     ]),

                  ],style=tab_style, selected_style=tab_selected_style),
                  dcc.Tab(label='Total Active', children=[
                     html.Div([
                        html.H1(" Active Cases in India ",style=style_tab_heading),
                          dcc.Graph(id='Active_bar',
                            figure={'data':[trace_act],'layout':layout_bar}
                          ),
                        html.H1('Pie Chart of Active Cases in India',style=style_tab_heading),
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
          #'maxWidth': '1400px',
          'margin': '0 auto'}
      ) #tabs End here

        ],style={'background-color':'#100e17','border':'10px #2F4F4F solid','border-bottom':'0px #2F4F4F solid',
        'margin':'10px'}),
    #intro start here..
    html.Div([
            dbc.Row([

              dbc.Col(
                html.Div([
                  html.Span('Created By:',className="panel-title",
                      style={'font-size':'25px','font-weight':'normal','color':'white'}),

                  
                    html.H2('Ramakant Shakya',style={'color':'white'}),
                    html.H2('(Data Science Enthusiast)',style={'color':'white'}),
                    


                  ],style=style_intro,className="panel-heading"),),


              dbc.Col(
                html.Div([
                  html.Span('Linkedin',className="panel-title",
                      style={'font-size':'25px','font-weight':'normal','color':'white'}),

                  

                    html.H2(html.A("Linkedin Profile", href='https://www.linkedin.com/in/ramakantshakya/', target="_blank",
                      style={'color':'white'})
                      ,),
                    html.H2(html.A("Github Profile", href='https://github.com/shakya2417', target="_blank",
                      style={'color':'white'})
                      ,),
                    


                  ],style=style_intro,className="panel-heading"),),

                  
            
              dbc.Col(
                html.Div([
                  html.Span('Any Suggestion',className="panel-title",
                      style={'font-size':'25px','font-weight':'normal','color':'white'}),

                  
                    html.H2('Mail at:',style={'color':'white'}),
                    html.H2('ramakantshakya@gmail.com',style={'color':'white'})
                    


                  ],style=style_intro,className="panel-heading"),),


                  
              dbc.Col(
                html.Div([
                  html.Span('Data Source:',className="panel-title",
                      style={'font-size':'25px','font-weight':'normal','color':'white'}),

                  
                    html.H2('https://www.mohfw.gov.in/ ',style={'color':'white','font-size':'20px'}),
                    html.H2('Johns Hopkins University',style={'color':'white','font-size':'20px'})
                    
                      

                    ],style=style_intro,className="panel-heading"),),
              ]),

              
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














































