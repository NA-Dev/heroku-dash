#!/usr/bin/env python
# coding: utf-8

# # Lab Assignment 12: Interactive Visualizations
# ## DS 6001: Practice and Application of Data Science
# 
# ### Instructions
# Please answer the following questions as completely as possible using text, code, and the results of code as needed. Format your answers in a Jupyter notebook. To receive full credit, make sure you address every part of the problem, and make sure your document is formatted in a clean and professional way.

# ## Problem 0
# Import the following libraries:

# In[1]:


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# external_stylesheets = ['./style.css']


# For this lab, we will be working with the 2019 General Social Survey one last time.

# In[2]:


gss = pd.read_csv("gss.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])



# The `gss` dataframe contains the following features:
# 
# * `id` - a numeric unique ID for each person who responded to the survey
# * `weight` - survey sample weights
# * `sex` - male or female
# * `education` - years of formal education
# * `region` - region of the country where the respondent lives
# * `age` - age
# * `income` - the respondent's personal annual income
# * `job_prestige` - the respondent's occupational prestige score, as measured by the GSS using the methodology described above
# * `mother_job_prestige` - the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above
# * `father_job_prestige` -the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above
# * `socioeconomic_index` - an index measuring the respondent's socioeconomic status
# * `satjob` - responses to "On the whole, how satisfied are you with the work you do?"
# * `relationship` - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."
# * `male_breadwinner` - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
# * `men_bettersuited` - agree or disagree with: "Most men are better suited emotionally for politics than are most women."
# * `child_suffer` - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."
# * `men_overwork` - agree or disagree with: "Family life often suffers because men concentrate too much on their work."

# ## Problem 1
# Our goal in this lab is to build a dashboard that presents our findings from the GSS. A dashboard is meant to be shared with an audience, whether that audience is a manager, a client, a potential employer, or the general public. So we need to provide context for our results. One way to provide context is to write text using markdown code.
# 
# Find one or two websites that discuss the gender wage gap, and write a short paragraph in markdown code summarizing what these sources tell us. Include hyperlinks to these websites. Then write another short paragraph describing what the GSS is, what the data contain, how it was collected, and/or other information that you think your audience ought to know. A good starting point for information about the GSS is here: http://www.gss.norc.org/About-The-GSS
# 
# Then save the text as a Python string so that you can use the markdown code in your dashboard later.
# 
# It should go without saying, but no plagiarization! If you summarize a website, make sure you put the summary in your own words. Anything that is copied and pasted from the GSS webpage, Wikipedia, or another website without attribution will receive no credit.
# 
# (Don't spend too much time on this, and you might want to skip it during the Zoom session and return to it later so that you can focus on working on code with your classmates.) [1 point]

# In[4]:


markdown_text = '''
    A disparity exists between men's and women's salaries for the same work. This "gender wage gap" has been narrowing, but still has not been closed. In 1963 the federal Equal Pay Act called for equal pay for equal work, but as of 1979 our best estimates for the wage gap showed women makine 62 cents for every dollar a man made on average. Currently, the gap is estimated by the U.S Bureau and Labor Statistics to be 82 cents on the dollar. Narrowing the gap is very challenging when in some cases, women are fired for voicing their frustration with the inequality they experience. Source: [Closing the Gender Pay Gap](https://www.shrm.org/hr-today/news/hr-magazine/summer2019/pages/closing-the-gender-pay-gap.aspx)

    What is even more staggering is a similar gap in promotions. If we only consider wage gaps for the same positions, we underestimate the inequality experienced by women in the work force by not also including that their pay is limited by lack of promotions. Researchers found that by midcareer men are 85% more likely to hold executive level positions than women, and later in their careers this gap increases to 171%. Source: [Gender Pay Gap Pegged to Lack of Promotions](https://www.shrm.org/resourcesandtools/hr-topics/compensation/pages/gender-pay-gap-pegged-to-promotions.aspx)

    The General Social Survey (GSS) has gathered data relating to US employment that can be used to study this pay gap. Below we analyze data they collected in 2018 containing information on gender, education, pay, and socioeconomic background for respondants. It also includes responses to several statements regarding traditional gender roles so we can look for trends in agreement or disagreement with these statements. Data Source: [https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv](https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv)
'''


# ## Problem 2
# Generate a table that shows the mean income, occupational prestige, socioeconomic index, and years of education for men and for women. Use a function from a `plotly` module to display a web-enabled version of this table. This table is for presentation purposes, so round every column to two decimal places and use more presentable column names. [3 points]

# In[5]:


gss_grouped = gss.groupby("sex").agg({"income": "mean", 
"job_prestige": "mean", 
"socioeconomic_index": "mean", 
"education": "mean"}).round(2) 

gss_grouped = gss_grouped.reset_index()
gss_grouped = pd.melt(gss_grouped, id_vars='sex', 
                    value_vars = ['income', 'job_prestige', 'socioeconomic_index', 'education'])
gss_grouped = gss_grouped.rename({'variable':'Index', 'value':'Average', 'sex': 'Gender'}, axis=1)
gss_grouped['Index'] = gss_grouped['Index'].map({'income': 'Income',
                                                 'job_prestige':'Occupational Prestige',
                                                 'socioeconomic_index':'Socioeconomic Status',
                                                 'education': 'Education'})
gss_grouped['Gender'] = gss_grouped['Gender'].map({'female': 'Female',
                                                 'male':'Male'})

fig2 = ff.create_table(gss_grouped)


# ## Problem 4
# Create an interactive scatterplot with `job_prestige` on the x-axis and `income` on the y-axis. Color code the points by `sex` and make sure that the figure includes a legend for these colors. Also include two best-fit lines, one for men and one for women. Finally, include hover data that shows us the values of `education` and `socioeconomic_index` for any point the mouse hovers over. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# In[8]:


gss_data = gss.copy()
gss_data['sex'] = gss_data['sex'].map({'female': 'Female',
                                       'male':'Male'})
fig4 = px.scatter(gss_data, x='job_prestige', y='income', 
                 color = 'sex', 
                 trendline='ols',
                 height=700,
                 labels={'job_prestige':'Job Prestige', 
                        'income':'Income',
                        'sex': 'Gender'},
                 hover_data=['education', 'socioeconomic_index'])
fig4.update(layout=dict(title=dict(x=0.5)))


# ## Problem 5
# Create two interactive box plots: one that shows the distribution of `income` for men and for women, and one that shows the distribution of `job_prestige` for men and for women. Write presentable labels for the axis that contains `income` or `job_prestige` and remove the label for `sex`. Also, turn off the legend. Don't bother with titles because we will be using subtitles on the dashboard for these graphics. [3 points]

# In[9]:


fig5a = px.box(gss_data, x='income', y = 'sex', color = 'sex',
                   labels={'income':'Income', 'sex':''})
fig5a.update_layout(showlegend=False)


# In[10]:


fig5b = px.box(gss_data, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'job_prestige':'Job Prestige', 'sex':''})
fig5b.update_layout(showlegend=False)


# ## Problem 6
# Create a new dataframe that contains only `income`, `sex`, and `job_prestige`. Then create a new feature in this dataframe that breaks `job_prestige` into six categories with equally sized ranges. Finally, drop all rows with any missing values in this dataframe.
# 
# Then create a facet grid with three rows and two columns in which each cell contains an interactive box plot comparing the income distributions of men and women for each of these new categories. 
# 
# (If you want men to be represented by blue and women by red, you can include `color_discrete_map = {'male':'blue', 'female':'red'}` in your plotting function. Or use different colors if you want!) [3 points]

# In[11]:


gss_sub = gss_data[['income', 'sex', 'job_prestige']]
gss_sub['job_prestige_groups'] = pd.cut(gss_sub['job_prestige'], bins=6, labels=['Lowest', 'Low', 'Low-Mid', 'Mid-High', 'High', 'Highest'])
gss_sub = gss_sub.dropna()


# In[12]:


fig6 = px.box(gss_sub, x='sex', y='income', color='sex',
             facet_col='job_prestige_groups', facet_col_wrap=2,
            labels={'sex':'Gender', 'income':'Income'},
            color_discrete_map = {'Male':'blue', 'Female':'red'},
            height=900
             )

fig6.update(layout=dict(title=dict(x=0.5)))
fig6.update_layout(showlegend=True)
fig6.for_each_annotation(lambda a: a.update(text=a.text.replace("job_prestige_groups=", "")))

  
# ## Extra Credit (up to 10 bonus points)
# Dashboards are all about good design, functionality, and accessability. For this extra credit problem, create another version of the dashboard you built for problem 7, but take extra steps to improve the appearance of the dashboard, add user-inputs, and host it on the internet with its own URL.
# 
# **Challenge 1**: Be creative and use a layout that significantly departs from the one used for the ANES data in the module 12 notebook. A good place to look for inspiration is the [Dash gallery](https://dash-gallery.plotly.host/Portal/). We will award up to 3 bonus points for creativity, novelty, and style.
# 
# **Challenge 2**: Alter the barplot from problem 3 to include user inputs. Create two dropdown menus on the dashboard. The first one should allow a user to display bars for the categories of `satjob`, `relationship`, `male_breadwinner`, `men_bettersuited`, `child_suffer`, or `men_overwork`. The second one should allow a user to group the bars by `sex`, `region`, or `education`. After choosing a feature for the bars and one for the grouping, program the barplot to update automatically to display the user-inputted features. One bonus point will be awarded for a good effort, and 3 bonus points will be awarded for a working user-input barplot in the dashboard.
# 
# **Challenge 3**: Follow the steps listed in the module notebook to deploy your dashboard on Heroku. 1 bonus point will be awarded for a Heroku link to an app that isn't working. 4 bonus points will be awarded for a working Heroku link.

# In[57]:

graphstyle = {
            'margin-bottom':'50px', 
            'margin-left':'auto',
            'margin-right':'auto', 
            'text-align':'center',
            'max-width': '1000px'
            }

questions = {
    'satjob': 'On the whole, how satisfied are you with the work you do?',
    'relationship': 'A working mother can establish just as warm and secure a relationship with her children as a mother who does not work.',
    'male_breadwinner': 'It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family.',
    'men_bettersuited': 'Most men are better suited emotionally for politics than are most women.',
    'child_suffer': 'A preschool child is likely to suffer if his or her mother works.',
    'men_overwork': 'Family life often suffers because men concentrate too much on their work.'
}

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    [
        html.H1('Understanding the Gender Wage Gap'),
        dcc.Markdown(children = markdown_text),
        html.H3('Comparing mean income, occupational prestige, and socioeconomic index by gender'),
        html.Div([
            dcc.Graph(figure=fig2)
        ], style=graphstyle),
        html.H3('Degree of agreement with gender role statements'),
        
        # user inputs
        html.Div([
            
            html.H4('Choose a feature to group by:'),
            
            dcc.Dropdown(id='y-axis',
                         options=[{'label': i, 'value': i} for i in ['sex', 'region', 'education']],
                         value='sex'),
            
            html.H4('Choose a statement:'),
            
            dcc.Dropdown(id='x-axis',
                         options=[{'label': questions[i], 'value': i} for i in questions.keys()],
                         value='male_breadwinner',
                         optionHeight=120)
        
        ], id='main', style={'width': '30%', 'float': 'left'}),
        
        html.Div([
            html.H5(id='fig3title'),
            html.Div([
                dcc.Graph(id='fig3')
            ], style=graphstyle),
        ], style={'width': '65%', 'float': 'right'}),
        
        html.Br(style={'clear':'both'}),
        
        html.H3('Trends in Income versus Job Prestige by gender'),
        html.Div([
            dcc.Graph(figure=fig4)
        ], style=graphstyle),
        
        html.Div([
            html.H3('Job Prestige distribution by gender'),
            html.Div([
                dcc.Graph(figure=fig5a)
            ], style=graphstyle)
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            html.H3('Income distribution by gender'),
            html.Div([
                dcc.Graph(figure=fig5b)
            ], style=graphstyle)
        ], style = {'width':'48%', 'float':'right'}),
        
        html.Br(style={'clear':'both'}),
        
        html.H3('Income distributions by job prestige and gender'),
        html.Div([
            dcc.Graph(figure=fig6)
        ], style=graphstyle),
    ]
)
@app.callback(
    Output(component_id='fig3title', component_property='children'),
    [Input(component_id='x-axis',component_property='value')]
)
def update_output_title(input_value):
    return 'Statement: {}'.format(questions[input_value])

@app.callback(Output(component_id='fig3',component_property='figure'),
                  [Input(component_id='x-axis',component_property='value'),
                   Input(component_id='y-axis',component_property='value')])

def make_figure(x, y):    
    data = gss.dropna()
    xtab = pd.crosstab(data[y], data[x]).reset_index()
    xtab = pd.melt(xtab, id_vars = y, value_vars = data[x].unique())
    
    fig3 = px.bar(xtab, x=x, y='value', color=y,
            labels={x:'Response', 'value':'Count'},
            text='value',
            barmode = 'group')
    fig3.update_layout(showlegend=True)
    fig3.update(layout=dict(title=dict(x=0.5)))
    return fig3

if __name__ == '__main__':
    app.run_server(debug=True)
