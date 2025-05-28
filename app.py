import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True,pages_folder="front/pages", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

header = dbc.Navbar(
    dbc.Container([
        html.Div("Accidents de la route en France (2019–2023)", style={
            "fontWeight": "bold",
            "fontSize": "1.5rem",
            "marginRight": "2rem"
        }),
        dbc.Nav([
            dbc.NavItem(
                dcc.Link(
                    page["name"],
                    href=page["relative_path"],
                    className="header_btn",  # ✅ c’est ici que tu ajoutes ta classe CSS
                    style={"padding": "8px 16px", "textDecoration": "none", "color": "black"}
                )
            )
            for page in dash.page_registry.values()
        ])
    ]),
    color="light",
    dark=False,
    style={
        "borderRadius": "12px",
        "marginTop": "20px",
        "boxShadow": "0px 4px 12px rgba(0,0,0,0.1)",
        "background": "linear-gradient(to right, #f8f9fa, #e9ecef)",
    }
)



app.layout = dbc.Container([
    header,
    html.Br(),
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)