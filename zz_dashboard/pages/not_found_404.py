from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__
)


def layout():
    layout = html.Div(
        dbc.Container(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname was not recognized..."),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-light rounded-3",
    )
    return layout
