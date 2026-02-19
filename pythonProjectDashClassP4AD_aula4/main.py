# -*- coding: utf-8 -*-
"""
Dashboard Interativo - Análise de Dados SLE
Visualizações e KPIs para análise de solicitações de coleta de lixo
"""

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Carregar e preparar dados
df = pd.read_csv('SLE.csv')

# Limpeza e normalização
df_normalized = df.copy()
df_normalized = df_normalized.dropna(axis=1, how='any')
df_normalized.columns = df_normalized.columns.str.lower().str.replace(" ", "_")


# Padronizar valores de 'bac'
for idx,elemento in enumerate(df_normalized['bac']):
  if (elemento == 'Compost-240'):
    df_normalized.loc[idx,'bac']= 'Compost - 240'
  if (elemento == 'Compost-132'):
    df_normalized.loc[idx,'bac']= 'Compost - 132'
  if (elemento == 'Compost- 132'):
    df_normalized.loc[idx,'bac']= 'Compost - 132'

# Converter data e criar períodos
df_normalized['date_fermeture'] = pd.to_datetime(df_normalized['date_fermeture'], errors='coerce')
df_normalized["month"] = df_normalized["date_fermeture"].dt.to_period("M")
df_normalized['week'] = df_normalized["date_fermeture"].dt.to_period("W")


# ==================== CALCULAR MÉTRICAS ====================
total_requests = len(df_normalized)
total_replacement = (df_normalized['requete'] == 'Remplacement').sum()
total_delivery = (df_normalized['requete'] == 'Livraison').sum()
replacement_rate = (total_replacement / total_requests) * 100 if total_requests > 0 else 0
delivery_rate = (total_delivery / total_requests) * 100 if total_requests > 0 else 0


# ==================== INICIALIZAR APP ====================
app = dash.Dash(__name__)

# ==================== ESTILOS CSS ====================
styles = {
    'container': {
        'maxWidth': '1400px',
        'margin': '0 auto',
        'padding': '30px 20px',
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f5f7fa',
        'minHeight': '100vh'
    },
    'title': {
        'textAlign': 'center',
        'color': '#2c3e50',
        'marginBottom': '40px',
        'fontSize': '32px',
        'fontWeight': 'bold'
    },
    'kpi_container': {
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '20px',
        'marginBottom': '40px'
    },
    'kpi_card': {
        'backgroundColor': 'white',
        'padding': '25px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'textAlign': 'center',
        'transition': 'transform 0.3s, boxShadow 0.3s',
        'cursor': 'pointer'
    },
    'kpi_card_hover': {
        'transform': 'translateY(-5px)',
        'boxShadow': '0 8px 16px rgba(0,0,0,0.15)'
    },
    'kpi_title': {
        'fontSize': '14px',
        'color': '#7f8c8d',
        'marginBottom': '10px',
        'textTransform': 'uppercase',
        'letterSpacing': '1px'
    },
    'kpi_value': {
        'fontSize': '36px',
        'fontWeight': 'bold',
        'marginTop': '10px'
    },
    'kpi_value_primary': {
        'color': '#3498db'
    },
    'kpi_value_danger': {
        'color': '#e74c3c'
    },
    'kpi_value_warning': {
        'color': '#f39c12'
    },
    'kpi_value_success': {
        'color': '#27ae60'
    },
    'charts_row': {
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))',
        'gap': '20px',
        'marginBottom': '30px'
    },
    'chart_container': {
        'backgroundColor': 'white',
        'borderRadius': '8px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'padding': '20px'
    },
    'full_width': {
        'gridColumn': '1 / -1'
    }
}

# ==================== LAYOUT ====================
app.layout = html.Div(style=styles['container'], children=[

    # Título
    html.H1("📊 Dashboard SLE - Análise de Dados", style=styles['title']),

    # KPIs
    html.Div(style=styles['kpi_container'], children=[
        html.Div(style=styles['kpi_card'], children=[
            html.Div("Total de Solicitações", style=styles['kpi_title']),
            html.Div(f"{total_requests:,}", style={**styles['kpi_value'], **styles['kpi_value_primary']})
        ]),

        html.Div(style=styles['kpi_card'], children=[
            html.Div("Taxa de Reposição", style=styles['kpi_title']),
            html.Div(f"{replacement_rate:.1f}%", style={**styles['kpi_value'], **styles['kpi_value_danger']})
        ]),

        html.Div(style=styles['kpi_card'], children=[
            html.Div("Solicitações (Reposição)", style=styles['kpi_title']),
            html.Div(f"{total_replacement:,}", style={**styles['kpi_value'], **styles['kpi_value_warning']})
        ]),

        html.Div(style=styles['kpi_card'], children=[
            html.Div("Solicitações (Entrega)", style=styles['kpi_title']),
            html.Div(f"{total_delivery:,}", style={**styles['kpi_value'], **styles['kpi_value_success']})
        ]),
    ]),

    # Gráficos - Linha 1
    html.Div(style=styles['charts_row'], children=[
        html.Div(style=styles['chart_container'], children=[
            dcc.Graph(id='pie-requete')
        ]),

        html.Div(style=styles['chart_container'], children=[
            dcc.Graph(id='bar-bac')
        ]),
    ]),

    # Gráfico - Top Ruas (Full Width)
    html.Div(style={**styles['chart_container'], **styles['full_width']}, children=[
        dcc.Graph(id='bar-top-ruas')
    ]),

    # Gráficos - Linha 2
    html.Div(style=styles['charts_row'], children=[

        html.Div(style=styles['chart_container'], children=[
            dcc.Graph(id='bar-bac-requete')
        ]),
    ]),

    # Gráfico - Timeline (Full Width)
    html.Div(style={**styles['chart_container'], **styles['full_width']}, children=[
        dcc.Graph(id='timeline-requete')
    ]),

])


# ==================== CALLBACKS ====================
@app.callback(Output('pie-requete','figure'),
               Input('pie-requete','id'))
def update_pie_requete(_):
    requete_counts = df_normalized['requete'].value_counts().reset_index()
    requete_counts.columns = ["requete", "count"]

    fig = px.pie(
        requete_counts,
        names="requete",
        values="count",
        title="Distribuição das Requêtes",
        hole=0  # coloque 0.35 se quiser donut
    )

    fig.update_layout(
        height=500,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig



# ==================== EXECUTAR ====================
if __name__ == '__main__':
    app.run_server(debug=True)
