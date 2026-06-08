from dash import Dash, html, dcc, Input, Output, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from mastery.bkt import BKTModel


app = Dash(__name__, title="Learner Model Simulation", external_stylesheets=[dbc.themes.BOOTSTRAP])

model = BKTModel()

def create_figure():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(len(model.p_history))),
            y=model.p_history,
            mode="lines+markers",
            name="Mastery"
        )
    )

    fig.update_layout(
        title="Mastery over time",
        xaxis_title="Step",
        yaxis_title="P(known)",
        yaxis_range=[0, 1],
        template="plotly_white",
        height=400,
    )

    return fig


@app.callback(
    Output("mastery-text", "children"),
    Output("mastery-graph", "figure"),

    Input("correct-btn", "n_clicks"),
    Input("incorrect-btn", "n_clicks"),
    Input("reset-btn", "n_clicks"),

    Input("p-init-slider", "value"),
    Input("t-slider", "value"),
    Input("g-slider", "value"),
    Input("s-slider", "value"),

    prevent_initial_call=False,
)
def update_dashboard(n_correct, n_incorrect, n_reset, p_init, T, G, S):
    model.p_init = p_init
    model.T = T
    model.G = G
    model.S = S

    trigger = ctx.triggered_id

    if trigger == "correct-btn":
        model.observe(True)
    elif trigger == "incorrect-btn":
        model.observe(False)
    elif trigger == "reset-btn":
        model.reset()

    mastery_text = html.H4(f"Current mastery: {model.p:.3f} (expected correct = {model.expected_correct():.2f})")

    fig = create_figure()

    return mastery_text, fig


if __name__ == "__main__":
    app.layout = dbc.Container([
        html.H1("Learner Model Simulation"),

        dbc.Card([
            dbc.CardHeader("Simulate Learner Event"),
            dbc.CardBody([
                dbc.Button("Correct", id="correct-btn", color="success", className="me-2"),
                dbc.Button("Incorrect", id="incorrect-btn", color="danger", className="me-2"),
                dbc.Button("Reset", id="reset-btn", color="secondary"),
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Bayesian Knowledge Tracing"),

                    dbc.CardBody([
                        html.Div(id="mastery-text"),

                        html.Label("Initial mastery"),
                        dcc.Slider(id="p-init-slider", min=0, max=1, step=0.01, value=model.p_init),

                        html.Label("Learning (T)"),
                        dcc.Slider(id="t-slider", min=0, max=1, step=0.01, value=model.T),

                        html.Label("Guess (G)"),
                        dcc.Slider(id="g-slider", min=0, max=1, step=0.01, value=model.G),

                        html.Label("Slip (S)"),
                        dcc.Slider(id="s-slider", min=0, max=1, step=0.01, value=model.S),

                        dcc.Graph(id="mastery-graph", figure=create_figure()),
                    ])
                ])
            ])
        ])
    ], fluid=True)

    app.run(debug=True)
