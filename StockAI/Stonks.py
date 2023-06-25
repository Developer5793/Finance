from dash import html, dcc
from dash import Dash
import dash_bootstrap_components as dbc
import dash
from DisplayElementsClass import MainDisplayElements


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])

Menubar = MainDisplayElements.Create_MenuBar()


app.layout = html.Div([Menubar, dash.page_container,


							dcc.Store(id="CompanyOverview", storage_type='session'),
							dcc.Store(id="BalanceSheet",storage_type='session'),
						    dcc.Store(id="IncomeStatement",storage_type='session'),
							dcc.Store(id="CashflowStatement",storage_type='session'),
							dcc.Store(id="MonthlyPriceInformation", storage_type="session"),
							dcc.Store(id="FundamentalDataFrame",storage_type='session'),
							dcc.Store(id="EquityToAssetStateButton",storage_type='session'),
							dcc.Store(id="DebtEquityStateButton",storage_type='session'),
							dcc.Store(id="LongTermDebtEquityStateButton",storage_type='session'),
							dcc.Store(id="ShortTermDebtEquityStateButton",storage_type='session'),
							dcc.Store(id="FixedAssetRatioStateButton",storage_type='session'),
							dcc.Store(id="CoverageRatioIStateButton",storage_type='session'),
							dcc.Store(id="CoverageRatioIIStateButton",storage_type='session'),
							dcc.Store(id="CashRatioStateButton",storage_type='session'),
							dcc.Store(id="CurrentRatioStateButton",storage_type='session'),
							dcc.Store(id="QuickRatioStateButton",storage_type='session'),
							dcc.Store(id="RetunOnEquityStateButton",storage_type='session'),
							dcc.Store(id="ReturnOnAssetsStateButton",storage_type='session'),
							dcc.Store(id="ReturnOnSalesStateButton",storage_type='session'),
							dcc.Store(id="OperatingProfitMarginStateButton",storage_type='session'),
							dcc.Store(id="ProfitMarginStateButton",storage_type='session'),
							dcc.Store(id="CashFlowToRevenuesStateButton",storage_type='session'),
							dcc.Store(id="InterestCoverageRatioStateButton",storage_type='session'),
						    dcc.Store(id="PriceEarningsStateButton",storage_type='session'),
							dcc.Store(id="EPSStateButton",storage_type='session'),						
					] ,           
					  className="content",
)


if __name__ == '__main__':
	app.run_server(debug=True)

