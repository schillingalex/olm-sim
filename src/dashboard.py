from copy import copy
import solara
import matplotlib.pyplot as plt

from learner.bkt import BKTModel


plt.style.use("seaborn-v0_8-pastel")


models = []


def process_response(correct: bool):
    for model in models:
        current_model = model.value
        current_model.observe(correct)
        model.set(copy(current_model))


def reset_models():
    for model in models:
        current_model = model.value
        current_model.reset()
        model.set(copy(current_model))


@solara.component
def Controls():
    with solara.Card("Simulate Learner Event"):
        with solara.Row():
            solara.Button("Correct", on_click=lambda: process_response(True))
            solara.Button("Incorrect", on_click=lambda: process_response(False))
            solara.Button("Reset", on_click=lambda: reset_models())


@solara.component
def BKTParameterControls(model_reactive):
    model = model_reactive.value
    p_init = solara.reactive(model.p_init)
    T = solara.reactive(model.T)
    G = solara.reactive(model.G)
    S = solara.reactive(model.S)

    def apply_params(_=None):
        model.p_init = float(p_init.value)
        model.p_trans = float(T.value)
        model.p_guess = float(G.value)
        model.p_slip = float(S.value)
        model_reactive.set(model)

    with solara.Card("BKT Parameters"):
        solara.SliderFloat(value=p_init, max=1.0, step=0.01, label="Initial mastery", on_value=apply_params)
        solara.SliderFloat(value=T, max=1.0, step=0.01, label="Learning (T)", on_value=apply_params)
        solara.SliderFloat(value=G, max=1.0, step=0.01, label="Guess (G)", on_value=apply_params)
        solara.SliderFloat(value=S, max=1.0, step=0.01, label="Slip (S)", on_value=apply_params)


@solara.component
def BKTMasteryText(model_reactive):
    model = model_reactive.value
    return solara.Markdown(f"### Current mastery: **{model.p:.3f}** (expected correct = {model.expected_correct():.2f})")


@solara.component
def BKTMasteryPlot(model_reactive):
    model = model_reactive.value
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(model.p_history, marker="o")
    ax.set_ylim(0, 1)
    ax.set_title("Mastery over time")
    ax.set_xlabel("Step")
    ax.set_ylabel("P(known)")
    ax.grid(True)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    fig.tight_layout()
    plt.close(fig)
    return solara.FigureMatplotlib(fig)


@solara.component
def BKTPanel():
    bkt_model = solara.reactive(BKTModel())
    models.append(bkt_model)
    with solara.Card("Bayesian Knowledge Tracing"):
        BKTParameterControls(bkt_model)
        BKTMasteryText(bkt_model)
        BKTMasteryPlot(bkt_model)


@solara.component
def Page():
    solara.Title("Learner Model Simulation")
    with solara.Card(elevation=0):
        Controls()
        with solara.Row():
            BKTPanel()
