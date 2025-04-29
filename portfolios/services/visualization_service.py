import plotly.graph_objects as go
from plotly.subplots import make_subplots
from portfolios.services.metrics_service import get_portfolio_metrics
from collections import defaultdict
from datetime import date
from portfolios.models import Portfolio
import logging

logger = logging.getLogger(__name__)

COLOR_PALETTE = [
    '#a8e6cf', '#dcedc1', '#ffd3b6', '#ffaaa5', '#ff8b94',
    '#d4a5a5', '#9c9c9c', '#b5ead7', '#c7ceea', '#e2f0cb',
    '#ffb7b2', '#ffdac1', '#b5ead7', '#c7ceea', '#e2f0cb',
    '#ffb7b2'
]

def format_metrics_for_plotting(metrics: list[dict]) -> dict:
    logger.debug("Formatting metrics for plotting")
    dates, total_values = [], []
    weights_by_asset = defaultdict(list)
    asset_names = set()

    for result in sorted(metrics, key=lambda x: x['date']):
        dates.append(result['date'].isoformat())
        total_values.append(float(result['total_value']))
        for asset_name, weight in result['weights'].items():
            weights_by_asset[asset_name].append(float(weight))
            asset_names.add(asset_name)

    formatted_data = {
        'dates': dates,
        'total_values': total_values,
        'weights': dict(weights_by_asset),
        'asset_names': sorted(list(asset_names))
    }
    logger.debug(f"Formatted data: {len(dates)} dates, {len(asset_names)} assets")
    return formatted_data

def create_metrics_plot(formatted_data: dict) -> go.Figure:
    logger.debug("Creating metrics plot")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    layout = {
        'title': {
            'text': 'Evolución del Portafolio',
            'x': 0.5,
            'y': 0.98,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'family': 'Inter, sans-serif', 'size': 24, 'color': '#2c3e50'}
        },
        'showlegend': True,
        'legend': {
            'orientation': "h",
            'yanchor': "top",
            'y': -0.25,
            'xanchor': "center",
            'x': 0.5,
            'font': {'family': 'Inter, sans-serif', 'size': 10, 'color': '#2c3e50'},
            'tracegroupgap': 0,
            'traceorder': 'normal',
            'itemwidth': 30,
            'itemsizing': 'constant',
            'bordercolor': 'rgba(128, 128, 128, 0.2)',
            'borderwidth': 1,
            'bgcolor': 'rgba(255, 255, 255, 0.8)',
            'entrywidth': 0.4,
            'entrywidthmode': 'fraction'
        },
        'height': 700,
        'margin': {'l': 50, 'r': 50, 't': 80, 'b': 150, 'pad': 0},
        'hovermode': 'x unified',
        'paper_bgcolor': 'rgba(245, 245, 245, 0.8)',
        'plot_bgcolor': 'rgba(255, 255, 255, 0.9)',
        'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': '#2c3e50'}
    }
    
    axis_config = {
        'showgrid': True,
        'zeroline': True,
        'automargin': True,
        'showline': True,
        'linewidth': 1,
        'linecolor': 'rgba(128, 128, 128, 0.2)',
        'gridcolor': 'rgba(128, 128, 128, 0.1)',
        'zerolinecolor': 'rgba(128, 128, 128, 0.2)'
    }
    
    for idx, asset_name in enumerate(formatted_data['asset_names']):
        fig.add_trace(
            go.Scatter(
                x=formatted_data['dates'],
                y=formatted_data['weights'][asset_name],
                name=asset_name,
                stackgroup='weights',
                mode='lines',
                line=dict(width=0),
                fillcolor=COLOR_PALETTE[idx % len(COLOR_PALETTE)],
                opacity=0.5,
                hovertemplate='Fecha: %{x}<br>Peso: %{y:.2%}<extra></extra>',
                zorder=1
            ),
            secondary_y=True
        )
    
    fig.add_trace(
        go.Scatter(
            x=formatted_data['dates'],
            y=formatted_data['total_values'],
            name='Valor Total',
            line=dict(color='#2c3e50', width=3),
            hovertemplate='Fecha: %{x}<br>Valor: $%{y:,.2f}<extra></extra>',
            mode='lines+markers',
            zorder=2
        ),
        secondary_y=False
    )
    
    fig.update_layout(**layout)
    
    fig.update_xaxes(
        **axis_config,
        title='Fecha',
        tickangle=45,
        range=[formatted_data['dates'][0], formatted_data['dates'][-1]],
        dtick="M1",
        tickformat="%b %Y"
    )
    
    fig.update_yaxes(
        **axis_config,
        title='Valor Total ($)',
        tickformat="$,.0f",
        secondary_y=False
    )
    
    fig.update_yaxes(
        **axis_config,
        title='Pesos (%)',
        tickformat=".0%",
        range=[0, 1],
        secondary_y=True
    )
    
    logger.info("Created metrics plot successfully")
    return fig

def get_portfolio_metrics_plot(portfolio_id: int, start_date: date, end_date: date) -> str:
    logger.debug(f"Getting portfolio metrics plot for portfolio {portfolio_id} from {start_date} to {end_date}")
    metrics = get_portfolio_metrics(portfolio_id, start_date, end_date)
    formatted_data = format_metrics_for_plotting(metrics)
    fig = create_metrics_plot(formatted_data)
    logger.info(f"Generated portfolio metrics plot for portfolio {portfolio_id}")
    return fig.to_html(full_html=False)
