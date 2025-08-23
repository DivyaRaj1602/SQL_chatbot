# simple_main.py - Enhanced version with history and interactive visualization

from advanced_pipeline import AdvancedSQLPipeline
from visualization import AdvancedDataVisualizer as DataAnalyzer
from history import ChatHistory

def display_results(result):
    """Display results in a nice format"""
    print("\n" + "="*60)

    if result['success']:
        print("✅ SUCCESS")
        print(f"Question: {result['user_question']}")
        print(f"Table: {result['target_table']}")
        print(f"SQL: {result['sql_query']}")
        print(f"Found: {result['result_count']} rows")

        # Show first few results
        if result['results']:
            print("\n📊 Results:")
            print("-" * 40)

            # Show headers
            headers = list(result['results'][0].keys())
            print(" | ".join(headers))
            print("-" * 40)

            # Show first 5 rows
            for i, row in enumerate(result['results'][:5]):
                values = [str(row[col]) for col in headers]
                print(" | ".join(values))

            if len(result['results']) > 5:
                print(f"... and {len(result['results']) - 5} more rows")
        else:
            print("No data found")

    else:
        print("❌ FAILED")
        print(f"Error: {result['error']}")

    print("="*60)

def handle_visualization_command(command, analyzer):
    """Handle user visualization commands"""
    command = command.lower().strip()
    parts = command.split()
    
    if not parts:
        return False
    
    action = parts[0]
    
    try:
        if action == "histogram":
            if len(parts) >= 2:
                column = parts[1]
            else:
                # Pick first numeric column
                numeric_cols = analyzer.df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    column = numeric_cols[0]
                    print(f"📊 Creating histogram for {column} (auto-selected)...")
                else:
                    print("❌ No numeric column available for histogram")
                    return True
            analyzer.create_histogram(column)
            return True
            
        elif action == "pie":
            if len(parts) >= 2:
                labels_col = parts[1]
                values_col = analyzer.df.select_dtypes(include=['number']).columns[0] \
                    if len(analyzer.df.select_dtypes(include=['number']).columns) > 0 else None
            else:
                # Auto-pick first categorical + numeric
                cat_cols = analyzer.df.select_dtypes(include=['object']).columns
                num_cols = analyzer.df.select_dtypes(include=['number']).columns
                if len(cat_cols) > 0 and len(num_cols) > 0:
                    labels_col, values_col = cat_cols[0], num_cols[0]
                    print(f"🥧 Creating pie chart for {labels_col} by {values_col} (auto-selected)...")
                else:
                    print("❌ Need at least one categorical and one numeric column for pie chart")
                    return True
            analyzer.create_pie_chart(labels_col, values_col)
            return True
            
        elif action == "scatter":
            if len(parts) >= 3:
                x_col, y_col = parts[1], parts[2]
            else:
                # Auto-pick first two numeric columns
                num_cols = analyzer.df.select_dtypes(include=['number']).columns
                if len(num_cols) >= 2:
                    x_col, y_col = num_cols[0], num_cols[1]
                    print(f"🔍 Creating scatter plot: {x_col} vs {y_col} (auto-selected)...")
                else:
                    print("❌ Need at least two numeric columns for scatter plot")
                    return True
            analyzer.create_scatter_plot(x_col, y_col)
            return True
            
        elif action == "line":
            if len(parts) >= 3:
                x_col, y_col = parts[1], parts[2]
            else:
                # Auto-pick first date/numeric combination
                date_cols = analyzer.df.select_dtypes(include=['datetime64']).columns
                num_cols = analyzer.df.select_dtypes(include=['number']).columns
                if len(date_cols) > 0 and len(num_cols) > 0:
                    x_col, y_col = date_cols[0], num_cols[0]
                    print(f"📈 Creating line chart: {y_col} over {x_col} (auto-selected)...")
                else:
                    print("❌ Need a date (or sequential) and a numeric column for line chart")
                    return True
            analyzer.create_line_chart(x_col, y_col)
            return True
            
        elif action == "bar":
            if len(parts) >= 2:
                column = parts[1]
            else:
                # Auto-pick first categorical column
                cat_cols = analyzer.df.select_dtypes(include=['object']).columns
                if len(cat_cols) > 0:
                    column = cat_cols[0]
                    print(f"📊 Creating bar chart for {column} (auto-selected)...")
                else:
                    print("❌ No categorical column available for bar chart")
                    return True
            analyzer.create_bar_chart(x_col=column)
            return True
            
        elif action == "box":
            if len(parts) >= 2:
                column = parts[1]
            else:
                # Auto-pick first numeric column
                num_cols = analyzer.df.select_dtypes(include=['number']).columns
                if len(num_cols) > 0:
                    column = num_cols[0]
                    print(f"📦 Creating box plot for {column} (auto-selected)...")
                else:
                    print("❌ No numeric column available for box plot")
                    return True
            analyzer.plot_box(column)
            return True
            
        elif action == "heatmap":
            print(f"🔥 Creating correlation heatmap...")
            analyzer.plot_corr_heatmap()
            return True
            
        elif action == "options":
            analyzer.show_plot_options()
            return True
            
        elif action == "summary":
            analyzer.safe_analyze()
            return True
            
        elif action == "auto":
            print("🚀 Auto-generating the best visualization...")
            analyzer.auto_visualize()
            return True
            
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error creating plot: {e}")
        return True

def show_help():
    """Display help information"""
    print("\n💡 Available Commands:")
    print("=" * 40)
    print("📊 Data Analysis:")
    print("   • summary - Show data summary and statistics")
    print("   • options - Show available plotting options")
    print("\n🎨 Visualization Commands:")
    print("   • auto - Let AI choose the best chart automatically")
    print("   • options - See all available chart types")
    print("   • histogram <column> - Create histogram")
    print("   • pie <column> - Create pie chart")
    print("   • bar <column> - Create bar chart")
    print("   • box <column> - Create box plot")
    print("   • scatter <x_col> <y_col> - Create scatter plot")
    print("   • line <x_col> <y_col> - Create line chart")
    print("   • heatmap - Create correlation heatmap")
    print("   • 3d - Create 3D visualization")
    print("\n📚 History & Navigation:")
    print("   • history - Show chat history")
    print("   • clear - Clear chat history")
    print("   • schema - Show database schema")
    print("   • help - Show this help message")
    print("   • exit - Quit the application")
    print("\n🚀 Advanced SQL Features:")
    print("   • JOINs (INNER, LEFT, RIGHT, FULL)")
    print("   • CTEs (Common Table Expressions)")
    print("   • Window Functions")
    print("   • Subqueries and UNIONs")
    print("   • Complex aggregations")
    print("\n💬 Example Queries:")
    print("   • 'Show me all employees'")
    print("   • 'Get orders with customer and employee names'")
    print("   • 'Show product sales by category with rankings'")
    print("   • 'Find customers who ordered more than 5 products'")

def main():
    """Enhanced main function with history and interactive visualization"""
    print("🚀 Welcome to Advanced SQL Pipeline with Visualization!")
    print("This version supports JOINs, CTEs, Window Functions, and all advanced SQL features!")
    print("Type 'help' for available commands, 'exit' to quit.\n")

    # Initialize pipeline and history
    try:
        pipeline = AdvancedSQLPipeline()
        chat_history = ChatHistory()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return

    current_analyzer = None

    while True:
        user_input = input("\n💬 Ask me about your data: ").strip()

        if user_input.lower() == 'exit':
            print("👋 Goodbye!")
            break

        if user_input.lower() == 'help':
            show_help()
            continue

        if user_input.lower() == 'history':
            chat_history.show_history()
            continue

        if user_input.lower() == 'clear':
            chat_history.clear()
            current_analyzer = None
            print("🗑️  Chat history cleared.")
            continue

        if user_input.lower() == 'schema':
            pipeline.show_schema()
            continue

        if not user_input:
            continue

        # Check if this is a visualization command for existing data
        if current_analyzer and user_input.lower().startswith(('histogram', 'pie', 'scatter', 'line', 'bar', 'box', 'heatmap', 'options', 'summary', 'auto')):
            if handle_visualization_command(user_input, current_analyzer):
                continue
            else:
                print("❌ Invalid visualization command. Type 'options' to see available plots.")

        # Process as a new SQL query
        print(f"\n🔍 Processing: {user_input}")
        result = pipeline.process_query(user_input)
        
        # Add to history
        chat_history.add(user_input, result)
        
        # Display results
        display_results(result)
        
        # Set up visualization if successful
        if result['success'] and result['results']:
            try:
                current_analyzer = DataAnalyzer(result['results'])
                chat_history.add_analyzer(current_analyzer)
                
                # Show data summary
                print(f"\n📊 Data loaded successfully! {len(result['results'])} rows available for analysis.")
                print(f"🎯 Tables involved: {result['target_table']}")
                print("\n🎨 VISUALIZATION COMMANDS:")
                print("   • 'auto' - Let AI choose the best chart automatically")
                print("   • 'options' - See all available chart types")
                print("   • 'pie category' - Create pie chart of categories")
                print("   • 'histogram list_price' - Show price distribution")
                print("   • 'scatter standard_cost list_price' - Cost vs Price correlation")
                print("   • 'bar category' - Bar chart by category")
                print("   • 'line id list_price' - Price trends")
                print("   • 'heatmap' - Correlation matrix")
                print("\n💡 Quick Start: Type 'auto' to see the best visualization!")
                
            except Exception as e:
                print(f"❌ Error setting up data analysis: {e}")
                current_analyzer = None
        else:
            current_analyzer = None

if __name__ == "__main__":
    main()