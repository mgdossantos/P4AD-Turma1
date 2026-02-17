# -*- coding: utf-8 -*-
"""
Dashboard Interativo - Análise de Dados SLE
Visualizações e KPIs para análise de solicitações de coleta de lixo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output

# Carregar e preparar dados

# Limpeza e normalização


# Padronizar valores de 'bac'


# ==================== CALCULAR MÉTRICAS ====================
test=0


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
            html.Div(f"{test:,}", style={**styles['kpi_value'], **styles['kpi_value_primary']})
        ]),

        html.Div(style=styles['kpi_card'], children=[
            html.Div("Taxa de Reposição", style=styles['kpi_title']),
            html.Div(f"{test:.1f}%", style={**styles['kpi_value'], **styles['kpi_value_danger']})
        ]),

        html.Div(style=styles['kpi_card'], children=[
            html.Div("Solicitações (Reposição)", style=styles['kpi_title']),
            html.Div(f"{test:,}", style={**styles['kpi_value'], **styles['kpi_value_warning']})
        ]),

        html.Div(style=styles['kpi_card'], children=[
            html.Div("Solicitações (Entrega)", style=styles['kpi_title']),
            html.Div(f"{test:,}", style={**styles['kpi_value'], **styles['kpi_value_success']})
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


# ==================== EXECUTAR ====================
if __name__ == '__main__':
    app.run_server(debug=True)
