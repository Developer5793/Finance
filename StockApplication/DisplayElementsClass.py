from dash import html
import dash_bootstrap_components as dbc


class RatioDisplayElements(object):
  def __init__(self, GraphORTableObject, YearlyButton, QuarterlyButton, TableButton, RatioName, RatioPercentage):      

      self.GraphORTableObject = GraphORTableObject
      self.YearlyButton = YearlyButton
      self.QuarterlyButton = QuarterlyButton
      self.TableButton = TableButton

      self.RatioName = RatioName
      self.RatioPercentage = RatioPercentage

  def CreateRatioElement(self):

       ElementName = html.Div([
                           dbc.Row([
                                dbc.Button("Yearly",id = self.YearlyButton,size="sm",outline="True", color="primary",style={"width":"80px", "marginLeft": "5px"},className="me-2"),
                                dbc.Button("Quarterly",id = self.QuarterlyButton,size="sm",outline="True", color="primary",style={"width":"80px"},className="me-2"),
                                dbc.Button("Table",id = self.TableButton,size="sm",outline="True", color="primary",style={"height": "100%","width":"80px"},className="me-2")                              
                                ],style={"marginTop": "5px"}, justify="center"),
                           dbc.Row(
                               html.Div(id = self.GraphORTableObject,
                                             style={'marginLeft': '5px',
                                                    'marginRight': '5px',                                                   
                                                    'width': '320px'}))
                            ],style={
                        'display': 'inline-block',
                        "height": "360px",
                        'background-color': '#191919' ,
                        'border': '1px solid grey',
                        'overflow': 'hidden',
                        'width': "360px"})       
       
       ElementHeader= html.Div([
                           dbc.Row(
                            html.P(self.RatioName,style={'family':'Courier',"font-weight": "bold","color": "white",'marginLeft': '5px',"fontSize":"15px"}),align="end"),
                           dbc.Row(
                            html.P(id=self.RatioPercentage,style={'family':'Courier',"font-weight": "bold","color": "white",'marginLeft': '5px', "fontSize":"25px"}),align="start")
                           ]
                             ,style={
                        'display': 'inline-block',
                        "height": "80px",
                        "marginTop": "20px",
                        'background-color': '#191919' ,
                        'border': '1px solid grey',
                        'overflow': 'hidden',
                        'width': "360px"})  
       
       return ElementName, ElementHeader

class MainDisplayElements:

  def Create_HeaderElement(Headername):
      ElementName = html.Div(html.H3(Headername),style={
                        'display': 'inline-block',
                        "height": "auto",
                        "marginTop": "20px",
                        'background-color': '#191919' ,
                        'border': '1px solid grey',
                        'overflow': 'hidden',
                        'width': "420px"})         
      return ElementName

  def Create_SideBar():

   sidebar = html.Div(
     [
        html.Div(
            [
                html.H2("Stocks", style={"color": "white"}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-grip me-2"), 
                        html.Span("Home", style={"color": "white"}),
                     ],
                    href="/",
                    active="exact",
                ),
               dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-scale-unbalanced-flip me-2"), 
                        html.Span("Economy", style={"color": "white"}),
                    ],
                    href="/",
                    active="exact"),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-chart-line me-2"),
                        html.Span("Fundamental Analysis",style={"color": "white"}),
                    ],
                    href="/searchscreen",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-gg me-2"),
                        html.Span("Compare Stocks", style={"color": "white"}),
                    ],
                    href="/page-2",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
        ],
    className="sidebar",
    )
   return sidebar

  def Create_MenuBar():
        
        PLOTLY_LOGO = ""
        nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))
        dropdown = dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("FundamentalAnalyse",
                            href="http://127.0.0.1:8050/searchscreen"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
            nav=True,
            in_navbar=True,
            label="Menu",
        )

        MenuBar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                                dbc.Col(dbc.NavbarBrand("Stock Analysis Tool", className="ms-2")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="https://plotly.com",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(
                            [nav_item, dropdown],
                            className="ms-auto",
                            navbar=True,
                        ),
                        id="navbar-collapse2",
                        navbar=True,
                    ),
                ],
            ),
            color="dark",
            dark=True,
            className="mb-3",)
        return MenuBar


  def Create_FundamentalTopBar(SearchBarID, SearchButtonID, QuarterlyID):
       TopMenu= html.Div(
                              dbc.Row(
                                   [
                                    dbc.Col(dbc.Input(id=SearchBarID, placeholder="Enter a Stocktag", type="text",debounce=True),width={"size": 1,"offset": 3}),
                                    dbc.Col(dbc.Button("Search", id=SearchButtonID, className="me-2", n_clicks=0, style={"marginLeft": "15px"}),width={"size": 1}),
                                    dbc.Col(dbc.Button("Quarterly", id=QuarterlyID, className="me-2",  n_clicks=0, style={"marginLeft": "15px"}),width={"size": 1}),
                                    dbc.Col(dbc.Nav([
                                        dbc.NavItem([dbc.NavLink("Statistics", href="/statistics", active="exact", style={"height": "50px"}),]),
                                        dbc.NavLink("Balance-Sheet-Ratios", href="/ratiopage", active="exact", style={"height": "50px"}),
                                        dbc.NavLink("Success Metrics", href="/ratiopage2", active="exact"),
                                        ], 
                                     horizontal=True,
                                     pills=True ),
                                     width={"size": 5})
                                    ],
                                    class_name="g-0"))
       return TopMenu
