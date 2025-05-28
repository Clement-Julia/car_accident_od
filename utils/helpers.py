from dash import html
import dash_bootstrap_components as dbc

def accordion_stats(title, df_stats, is_percent=True):
    ordre_gravite = ["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"]
    colonnes_ordonnees = [col for col in ordre_gravite if col in df_stats.columns]
    autres_colonnes = [col for col in df_stats.columns if col not in colonnes_ordonnees]
    colonnes_finales = autres_colonnes + colonnes_ordonnees
    df_stats = df_stats[colonnes_finales]

    header = html.Tr([html.Th(col) for col in df_stats.columns])
    body_rows = [
        html.Tr([
            html.Td(
                f"{val:.1f}%" if isinstance(val, float) and is_percent and col != "annee"
                else f"{int(val)}" if col == "annee" and isinstance(val, (int, float))
                else f"{val:.1f}" if isinstance(val, float)
                else val
            ) for col, val in zip(df_stats.columns, row)
        ]) for _, row in df_stats.iterrows()
    ]

    table = html.Table(
        [html.Thead(header), html.Tbody(body_rows)],
        className="table-dark-custom"
    )

    return dbc.Accordion(
        children=[
            dbc.AccordionItem(table, title=title)
        ],
        className="accordion-dark",
        start_collapsed=True,
        flush=True
    )
