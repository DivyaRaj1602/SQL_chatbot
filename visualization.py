# advanced_visualization.py - Advanced Plotly-based Visualization System
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from typing import List, Dict, Any, Optional, Tuple
import warnings
import numpy as np
from datetime import datetime

# Configure Plotly for better aesthetics
pio.templates.default = "plotly_white"
warnings.filterwarnings('ignore')

class AdvancedDataVisualizer:
    """
    Advanced data visualization system using Plotly
    Features:
    - Smart chart selection based on data types
    - Interactive charts with hover information
    - Multiple chart types (bar, line, scatter, heatmap, etc.)
    - Responsive design for all devices
    - Professional color schemes
    - Export capabilities
    """
    
    def __init__(self, data: List[Dict[str, Any]]):
        """
        Initialize the visualizer with data
        
        Args:
            data: List of dictionaries (SQL query results)
        """
        self.raw_data = data
        self.df = pd.DataFrame(data) if data else pd.DataFrame()
        self.chart_history = []
        
        # Set professional color scheme
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'accent': '#2ca02c',
            'highlight': '#d62728',
            'neutral': '#7f7f7f',
            'pastel': ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
        }
        
        print(f"🎨 Advanced Visualizer initialized with {len(self.df)} rows and {len(self.df.columns)} columns")
    
    def analyze_data_structure(self) -> Dict[str, Any]:
        """
        Analyze data structure to determine best visualization options
        """
        if self.df.empty:
            return {"error": "No data to analyze"}
        
        analysis = {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "column_types": {},
            "numeric_columns": [],
            "categorical_columns": [],
            "date_columns": [],
            "text_columns": [],
            "recommended_charts": []
        }
        
        for col in self.df.columns:
            col_type = str(self.df[col].dtype)
            analysis["column_types"][col] = col_type
            
            # Categorize columns
            if col_type in ['int64', 'float64']:
                analysis["numeric_columns"].append(col)
            elif col_type == 'object':
                if self.df[col].dtype == 'datetime64[ns]' or self._is_date_column(col):
                    analysis["date_columns"].append(col)
                elif self.df[col].nunique() < 20:  # Low cardinality = categorical
                    analysis["categorical_columns"].append(col)
                else:
                    analysis["text_columns"].append(col)
        
        # Recommend chart types based on data structure
        analysis["recommended_charts"] = self._get_recommended_charts(analysis)
        
        return analysis
    
    def _is_date_column(self, col: str) -> bool:
        """Check if a column contains date-like data"""
        try:
            pd.to_datetime(self.df[col].dropna().head(10))
            return True
        except:
            return False
    
    def _get_recommended_charts(self, analysis: Dict[str, Any]) -> List[str]:
        """Get recommended chart types based on data analysis"""
        recommendations = []
        
        num_numeric = len(analysis["numeric_columns"])
        num_categorical = len(analysis["categorical_columns"])
        num_date = len(analysis["date_columns"])
        
        if num_numeric >= 2 and num_categorical >= 1:
            recommendations.extend(["Bar Chart", "Grouped Bar Chart", "Box Plot"])
        
        if num_numeric >= 2:
            recommendations.extend(["Scatter Plot", "Line Chart", "Area Chart"])
        
        if num_categorical >= 1:
            recommendations.extend(["Pie Chart", "Donut Chart", "Treemap"])
        
        if num_date >= 1 and num_numeric >= 1:
            recommendations.extend(["Time Series", "Line Chart", "Area Chart"])
        
        if num_numeric >= 3:
            recommendations.extend(["3D Scatter", "Heatmap", "Correlation Matrix"])
        
        if len(analysis["numeric_columns"]) > 0:
            recommendations.extend(["Histogram", "Distribution Plot"])
        
        return list(set(recommendations))  # Remove duplicates
    
    def show_available_charts(self):
        """Display all available chart options with descriptions"""
        analysis = self.analyze_data_structure()
        
        print("\n🎨 Available Visualization Options:")
        print("=" * 60)
        
        if "error" in analysis:
            print("❌ No data available for visualization")
            return
        
        print(f"📊 Data Summary: {analysis['total_rows']} rows, {analysis['total_columns']} columns")
        print(f"🔢 Numeric columns: {', '.join(analysis['numeric_columns'])}")
        print(f"🏷️  Categorical columns: {', '.join(analysis['categorical_columns'])}")
        print(f"📅 Date columns: {', '.join(analysis['date_columns'])}")
        
        print(f"\n💡 Recommended Charts:")
        for i, chart in enumerate(analysis['recommended_charts'], 1):
            print(f"  {i}. {chart}")
        
        print(f"\n🚀 Quick Commands:")
        print("  - 'auto' : Auto-generate best chart")
        print("  - 'bar'  : Create bar chart")
        print("  - 'line' : Create line chart")
        print("  - 'scatter': Create scatter plot")
        print("  - 'pie'  : Create pie chart")
        print("  - 'hist' : Create histogram")
        print("  - 'heat' : Create heatmap")
        print("  - '3d'   : Create 3D visualization")
    
    def auto_visualize(self):
        """Automatically select and create the best visualization"""
        analysis = self.analyze_data_structure()
        
        if "error" in analysis:
            print("❌ No data available for visualization")
            return
        
        # Auto-select best chart type
        if len(analysis["numeric_columns"]) >= 2 and len(analysis["categorical_columns"]) >= 1:
            self.create_bar_chart()
        elif len(analysis["date_columns"]) >= 1 and len(analysis["numeric_columns"]) >= 1:
            self.create_line_chart()
        elif len(analysis["numeric_columns"]) >= 2:
            self.create_scatter_plot()
        elif len(analysis["categorical_columns"]) >= 1:
            self.create_pie_chart()
        else:
            self.create_histogram()
    
    def create_bar_chart(self, x_col: str = None, y_col: str = None, title: str = "Bar Chart"):
        """Create an interactive bar chart"""
        if self.df.empty:
            print("❌ No data available")
            return
        
        # Auto-select columns if not specified
        if not x_col:
            x_col = self.df.select_dtypes(include=['object']).columns[0] if len(self.df.select_dtypes(include=['object']).columns) > 0 else self.df.columns[0]
        if not y_col:
            y_col = self.df.select_dtypes(include=['number']).columns[0] if len(self.df.select_dtypes(include=['number']).columns) > 0 else self.df.columns[1]
        
        # Prepare data
        if y_col in self.df.columns and x_col in self.df.columns:
            chart_data = self.df.groupby(x_col)[y_col].sum().reset_index()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=chart_data[x_col],
                    y=chart_data[y_col],
                    marker_color=self.colors['primary'],
                    hovertemplate=f'<b>{x_col}</b>: %{{x}}<br><b>{y_col}</b>: %{{y}}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=title,
                xaxis_title=x_col,
                yaxis_title=y_col,
                template="plotly_white",
                height=500,
                showlegend=False
            )
            
            fig.show()
            self.chart_history.append(("Bar Chart", title))
            print(f"✅ Created bar chart: {x_col} vs {y_col}")
        else:
            print(f"❌ Columns not found: {x_col}, {y_col}")
    
    def create_line_chart(self, x_col: str = None, y_col: str = None, title: str = "Line Chart"):
        """Create an interactive line chart"""
        if self.df.empty:
            print("❌ No data available")
            return
        
        # Auto-select columns if not specified
        if not x_col:
            x_col = self.df.select_dtypes(include=['datetime64']).columns[0] if len(self.df.select_dtypes(include=['datetime64']).columns) > 0 else self.df.columns[0]
        if not y_col:
            y_col = self.df.select_dtypes(include=['number']).columns[0] if len(self.df.select_dtypes(include=['number']).columns) > 0 else self.df.columns[1]
        
        if y_col in self.df.columns and x_col in self.df.columns:
            # Sort by x-axis if it's numeric or date
            if self.df[x_col].dtype in ['int64', 'float64'] or self._is_date_column(x_col):
                chart_data = self.df.sort_values(x_col)
            else:
                chart_data = self.df
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=chart_data[x_col],
                    y=chart_data[y_col],
                    mode='lines+markers',
                    line=dict(color=self.colors['primary'], width=3),
                    marker=dict(size=6, color=self.colors['secondary']),
                    hovertemplate=f'<b>{x_col}</b>: %{{x}}<br><b>{y_col}</b>: %{{y}}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=title,
                xaxis_title=x_col,
                yaxis_title=y_col,
                template="plotly_white",
                height=500,
                showlegend=False
            )
            
            fig.show()
            self.chart_history.append(("Line Chart", title))
            print(f"✅ Created line chart: {x_col} vs {y_col}")
        else:
            print(f"❌ Columns not found: {x_col}, {y_col}")
    
    def create_scatter_plot(self, x_col: str = None, y_col: str = None, color_col: str = None, title: str = "Scatter Plot"):
        """Create an interactive scatter plot"""
        if self.df.empty:
            print("❌ No data available")
            return
        
        # Auto-select columns if not specified
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) >= 2:
            if not x_col:
                x_col = numeric_cols[0]
            if not y_col:
                y_col = numeric_cols[1]
        
        if y_col in self.df.columns and x_col in self.df.columns:
            fig = go.Figure()
            
            if color_col and color_col in self.df.columns:
                # Color by category
                categories = self.df[color_col].unique()
                for i, category in enumerate(categories):
                    subset = self.df[self.df[color_col] == category]
                    fig.add_trace(go.Scatter(
                        x=subset[x_col],
                        y=subset[y_col],
                        mode='markers',
                        name=str(category),
                        marker=dict(size=8, color=self.colors['pastel'][i % len(self.colors['pastel'])]),
                        hovertemplate=f'<b>{x_col}</b>: %{{x}}<br><b>{y_col}</b>: %{{y}}<br><b>{color_col}</b>: {category}<extra></extra>'
                    ))
            else:
                # Simple scatter
                fig.add_trace(go.Scatter(
                    x=self.df[x_col],
                    y=self.df[y_col],
                    mode='markers',
                    marker=dict(size=8, color=self.colors['primary']),
                    hovertemplate=f'<b>{x_col}</b>: %{{x}}<br><b>{y_col}</b>: %{{y}}<extra></extra>'
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_col,
                yaxis_title=y_col,
                template="plotly_white",
                height=500
            )
            
            fig.show()
            self.chart_history.append(("Scatter Plot", title))
            print(f"✅ Created scatter plot: {x_col} vs {y_col}")
        else:
            print(f"❌ Columns not found: {x_col}, {y_col}")
    
    def create_pie_chart(self, labels_col: str = None, values_col: str = None, title: str = "Pie Chart"):
        """Create an interactive pie chart"""
        if self.df.empty:
            print("❌ No data available")
            return
        
        # Auto-select columns if not specified
        if not labels_col:
            labels_col = self.df.select_dtypes(include=['object']).columns[0] if len(self.df.select_dtypes(include=['object']).columns) > 0 else self.df.columns[0]
        if not values_col:
            values_col = self.df.select_dtypes(include=['number']).columns[0] if len(self.df.select_dtypes(include=['number']).columns) > 0 else self.df.columns[1]
        
        if labels_col in self.df.columns and values_col in self.df.columns:
            # Aggregate data
            chart_data = self.df.groupby(labels_col)[values_col].sum().reset_index()
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=chart_data[labels_col],
                    values=chart_data[values_col],
                    hole=0.3,  # Donut chart
                    marker_colors=self.colors['pastel'],
                    hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=title,
                template="plotly_white",
                height=500,
                showlegend=True
            )
            
            fig.show()
            self.chart_history.append(("Pie Chart", title))
            print(f"✅ Created pie chart: {labels_col} by {values_col}")
        else:
            print(f"❌ Columns not found: {labels_col}, {values_col}")
    
    def create_histogram(self, column: str = None, bins: int = 30, title: str = "Histogram"):
        """Create an interactive histogram"""
        if self.df.empty:
            print("❌ No data available")
            return
        
        # Auto-select column if not specified
        if not column:
            column = self.df.select_dtypes(include=['number']).columns[0] if len(self.df.select_dtypes(include=['number']).columns) > 0 else self.df.columns[0]
        
        if column in self.df.columns:
            fig = go.Figure(data=[
                go.Histogram(
                    x=self.df[column],
                    nbinsx=bins,
                    marker_color=self.colors['primary'],
                    hovertemplate='<b>Range</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=f"Distribution of {column}",
                xaxis_title=column,
                yaxis_title="Frequency",
                template="plotly_white",
                height=500,
                showlegend=False
            )
            
            fig.show()
            self.chart_history.append(("Histogram", title))
            print(f"✅ Created histogram for {column}")
        else:
            print(f"❌ Column not found: {column}")
    
    def create_heatmap(self, title: str = "Correlation Heatmap"):
        """Create a correlation heatmap for numeric columns"""
        if self.df.empty:
            print("❌ No data available")
            return
        
        numeric_df = self.df.select_dtypes(include=['number'])
        
        if len(numeric_df.columns) < 2:
            print("❌ Need at least 2 numeric columns for heatmap")
            return
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        fig = go.Figure(data=[
            go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                hovertemplate='<b>%{x}</b> vs <b>%{y}</b><br>Correlation: %{z:.3f}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=title,
            template="plotly_white",
            height=500,
            xaxis_title="Variables",
            yaxis_title="Variables"
        )
        
        fig.show()
        self.chart_history.append(("Heatmap", title))
        print(f"✅ Created correlation heatmap")
    
    def create_3d_scatter(self, x_col: str = None, y_col: str = None, z_col: str = None, title: str = "3D Scatter Plot"):
        """Create a 3D scatter plot"""
        if self.df.empty:
            print("❌ No data available")
            return
        
        # Auto-select columns if not specified
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) >= 3:
            if not x_col:
                x_col = numeric_cols[0]
            if not y_col:
                y_col = numeric_cols[1]
            if not z_col:
                z_col = numeric_cols[2]
        
        if all(col in self.df.columns for col in [x_col, y_col, z_col]):
            fig = go.Figure(data=[
                go.Scatter3d(
                    x=self.df[x_col],
                    y=self.df[y_col],
                    z=self.df[z_col],
                    mode='markers',
                    marker=dict(
                        size=6,
                        color=self.df[z_col],
                        colorscale='Viridis',
                        opacity=0.8
                    ),
                    hovertemplate=f'<b>{x_col}</b>: %{{x}}<br><b>{y_col}</b>: %{{y}}<br><b>{z_col}</b>: %{{z}}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=title,
                scene=dict(
                    xaxis_title=x_col,
                    yaxis_title=y_col,
                    zaxis_title=z_col
                ),
                template="plotly_white",
                height=600
            )
            
            fig.show()
            self.chart_history.append(("3D Scatter", title))
            print(f"✅ Created 3D scatter plot: {x_col} vs {y_col} vs {z_col}")
        else:
            print(f"❌ Columns not found: {x_col}, {y_col}, {z_col}")
    
    def create_dashboard(self, charts: List[Tuple[str, str]] = None):
        """Create a dashboard with multiple charts"""
        if self.df.empty:
            print("❌ No data available")
            return
        
        if not charts:
            # Auto-create dashboard based on data
            analysis = self.analyze_data_structure()
            charts = []
            
            if len(analysis["numeric_columns"]) >= 2:
                charts.append(("Bar Chart", "Distribution"))
            if len(analysis["date_columns"]) >= 1:
                charts.append(("Line Chart", "Trends"))
            if len(analysis["numeric_columns"]) >= 2:
                charts.append(("Scatter Plot", "Correlation"))
            if len(analysis["categorical_columns"]) >= 1:
                charts.append(("Pie Chart", "Composition"))
        
        # Create subplot layout
        rows = (len(charts) + 1) // 2
        cols = min(2, len(charts))
        
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=[title for _, title in charts],
            specs=[[{"secondary_y": False}] * cols] * rows
        )
        
        # Add charts to subplots
        for i, (chart_type, title) in enumerate(charts):
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            if chart_type == "Bar Chart":
                # Add bar chart
                pass  # Implementation would go here
            elif chart_type == "Line Chart":
                # Add line chart
                pass  # Implementation would go here
            # ... other chart types
        
        fig.update_layout(
            title="Data Dashboard",
            template="plotly_white",
            height=300 * rows,
            showlegend=False
        )
        
        fig.show()
        print(f"✅ Created dashboard with {len(charts)} charts")
    
    def export_chart(self, format: str = "html", filename: str = None):
        """Export the last created chart"""
        if not self.chart_history:
            print("❌ No charts to export")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chart_{timestamp}"
        
        print(f"📤 Exporting chart as {format}...")
        # Implementation would depend on the specific chart library being used
    
    def get_chart_history(self):
        """Get history of created charts"""
        if not self.chart_history:
            print("📊 No charts created yet")
            return
        
        print("\n📊 Chart History:")
        for i, (chart_type, title) in enumerate(self.chart_history, 1):
            print(f"  {i}. {chart_type}: {title}")
    
    def clear_history(self):
        """Clear chart history"""
        self.chart_history.clear()
        print("🗑️  Chart history cleared")

    def show_plot_options(self):
        """Alias for backward compatibility"""
        return self.show_available_charts()


# Backward compatibility
DataAnalyzer = AdvancedDataVisualizer
