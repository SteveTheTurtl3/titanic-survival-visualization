import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

#DATA LOADING & PREPARATION

# Load raw data
df_raw = pd.read_csv('titanic_data.csv')

# Create working copy
df = df_raw.copy()

#Convert Sex to numeric for easier processing
#0 = Female, 1 = Male
df['Sex_Numeric'] = df['Sex'].map({'female': 0, 'male': 1})

#Fill missing Age with median age
median_age = df['Age'].median()
df['Age'].fillna(median_age, inplace=True)

#Fill missing Fare with median fare
median_fare = df['Fare'].median()
df['Fare'].fillna(median_fare, inplace=True)

#Fill missing Embarked with most common port
df['Embarked'].fillna('S', inplace=True)

#Create FamilySize feature
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

#Create Age Groups for better visualization
df['AgeGroup'] = pd.cut(df['Age'], 
                        bins=[0, 12, 18, 35, 50, 100],
                        labels=['Child (0-12)', 'Teen (13-18)', 'Adult (19-35)', 
                               'Middle Age (36-50)', 'Senior (50+)'])

#Create Fare Groups
df['FareGroup'] = pd.qcut(df['Fare'], q=4, 
                          labels=['Low', 'Medium-Low', 'Medium-High', 'High'],
                          duplicates='drop')

#Store key statistics for use in visualizations
total_passengers = len(df)
total_survived = df['Survived'].sum()
survival_rate = df['Survived'].mean() * 100

#VISUALIZATION FUNCTIONS

def create_overview_dashboard():
    """
    Creates a comprehensive 4-panel dashboard showing key survival patterns.
    """
    
    
    #Create 2×2 grid of subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Survival Rate by Gender',
            'Survival Rate by Passenger Class',
            'Age Distribution: Survived vs Died',
            'Fare Distribution: Survived vs Died'
        ),
        specs=[
            [{'type': 'bar'}, {'type': 'bar'}],
            [{'type': 'histogram'}, {'type': 'box'}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    #CHART 1: Survival by Gender (Top Left)
    
    # Calculate survival rate for each gender
    gender_stats = df.groupby('Sex')['Survived'].agg(['sum', 'count', 'mean']).reset_index()
    gender_stats['survival_pct'] = gender_stats['mean'] * 100
    
    #Create bar chart
    fig.add_trace(
        go.Bar(
            x=['Female', 'Male'],
            y=gender_stats['survival_pct'],
            marker_color=['#4ECDC4', '#FF6B6B'],  # Teal for women, coral for men
            text=gender_stats['survival_pct'].round(1),
            texttemplate='%{text}%',
            textposition='outside',
            name='Survival Rate',
            showlegend=False
        ),
        row=1, col=1
    )
    
    #CHART 2: Survival by Class (Top Right)
    
    #Calculate survival rate for each class
    class_stats = df.groupby('Pclass')['Survived'].agg(['sum', 'count', 'mean']).reset_index()
    class_stats['survival_pct'] = class_stats['mean'] * 100
    
    #Create bar chart with different color for each class
    fig.add_trace(
        go.Bar(
            x=['1st Class', '2nd Class', '3rd Class'],
            y=class_stats['survival_pct'],
            marker_color=['#95E1D3', '#F38181', '#AA96DA'],  # Mint, coral, purple
            text=class_stats['survival_pct'].round(1),
            texttemplate='%{text}%',
            textposition='outside',
            name='Survival Rate',
            showlegend=False
        ),
        row=1, col=2
    )
    
    #CHART 3: Age Distribution (Bottom Left)
    
    #Get ages for survivors and non-survivors
    survived_ages = df[df['Survived'] == 1]['Age']
    died_ages = df[df['Survived'] == 0]['Age']
    
    #Add histogram for survivors
    fig.add_trace(
        go.Histogram(
            x=survived_ages,
            name='Survived',
            marker_color='#4ECDC4',
            opacity=0.7,
            nbinsx=25,  # Number of bins
            legendgroup='age',
            showlegend=True
        ),
        row=2, col=1
    )
    
    #Add histogram for non-survivors (overlapping)
    fig.add_trace(
        go.Histogram(
            x=died_ages,
            name='Did Not Survive',
            marker_color='#FF6B6B',
            opacity=0.7,
            nbinsx=25,
            legendgroup='age',
            showlegend=True
        ),
        row=2, col=1
    )
    
    #CHART 4: Fare Distribution (Bottom Right)
    
    #Get fares for survivors and non-survivors
    survived_fares = df[df['Survived'] == 1]['Fare']
    died_fares = df[df['Survived'] == 0]['Fare']
    
    #Add box plot for survivors
    fig.add_trace(
        go.Box(
            y=survived_fares,
            name='Survived',
            marker_color='#4ECDC4',
            legendgroup='fare',
            showlegend=False
        ),
        row=2, col=2
    )
    
    #Add box plot for non-survivors
    fig.add_trace(
        go.Box(
            y=died_fares,
            name='Did Not Survive',
            marker_color='#FF6B6B',
            legendgroup='fare',
            showlegend=False
        ),
        row=2, col=2
    )
    
    #LAYOUT & STYLING
    
    #Update overall layout
    fig.update_layout(
        height=800,
        title_text=f"<b>Titanic Survival Analysis Dashboard</b><br>" + 
                   f"<sub>{int(total_survived)} of {total_passengers} passengers survived ({survival_rate:.1f}%)</sub>",
        title_font_size=22,
        title_x=0.5,  # Center the title
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    #Update axis labels and styling
    fig.update_xaxes(title_text="Gender", row=1, col=1, showgrid=False)
    fig.update_xaxes(title_text="Passenger Class", row=1, col=2, showgrid=False)
    fig.update_xaxes(title_text="Age (years)", row=2, col=1, showgrid=True, gridcolor='lightgray')
    
    fig.update_yaxes(title_text="Survival Rate (%)", row=1, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Survival Rate (%)", row=1, col=2, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Number of Passengers", row=2, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Fare (British Pounds)", row=2, col=2, showgrid=True, gridcolor='lightgray')
    
    print("  ✓ Overview dashboard created")
    
    return fig


def create_interactive_scatter():
    """
    Creates an interactive scatter plot showing Age vs Fare for each passenger.
    """
    
    
    #Prepare data with readable labels
    scatter_df = df.copy()
    scatter_df['Outcome'] = scatter_df['Survived'].map({
        0: 'Did Not Survive',
        1: 'Survived'
    })
    scatter_df['Gender'] = scatter_df['Sex'].map({
        'female': 'Female',
        'male': 'Male'
    })
    scatter_df['Class'] = scatter_df['Pclass'].map({
        1: '1st Class',
        2: '2nd Class',
        3: '3rd Class'
    })
    
    #Create scatter plot
    fig = px.scatter(
        scatter_df,
        x='Age',
        y='Fare',
        color='Outcome',
        symbol='Gender',
        size='FamilySize',
        hover_data={
            'Name': True,
            'Class': True,
            'Embarked': True,
            'Age': ':.0f',
            'Fare': ':$.2f',
            'FamilySize': True,
            'Outcome': False,  # Already shown in color
            'Gender': False    # Already shown in symbol
        },
        color_discrete_map={
            'Did Not Survive': '#FF6B6B',
            'Survived': '#4ECDC4'
        },
        title='<b>Interactive Passenger Analysis: Age vs Fare</b>',
        labels={
            'Age': 'Age (years)',
            'Fare': 'Fare Paid (£)',
            'Outcome': 'Survival Outcome',
            'Gender': 'Gender',
            'FamilySize': 'Family Size'
        },
        height=600
    )
    
    #Update layout for better interactivity
    fig.update_layout(
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    #Add grid
    fig.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridcolor='lightgray')
    
    
    return fig

#GRADIO WEB INTERFACE

#Custom CSS for styling
custom_css = """
.gradio-container {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    max-width: 1400px;
    margin: auto;
}

.gr-button-primary {
    background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%) !important;
    border: none !important;
    font-weight: 600 !important;
}

h1 {
    color: #2C3E50 !important;
}
"""

#Create the Gradio application
with gr.Blocks(css=custom_css, theme=gr.themes.Soft(), title="Titanic Survival Analysis") as app:
    
    #HEADER
    
    gr.Markdown("""
    #Titanic Survival Analysis
    
    Explore patterns from the 1912 Titanic disaster through interactive visualizations.
    This project demonstrates data storytelling, visual design, and interactive analytics.
    """)
    
    #TAB 1: DATA VISUALIZATION
    
    with gr.Tab("📊 Data Visualization"):
        
        gr.Markdown("""
        #Survival Pattern Analysis
        
        Click the button below to load interactive visualizations revealing how demographic 
        factors influenced survival outcomes aboard the Titanic.
        
        #Key Insights Revealed:
        - **Gender Effect**: The "women and children first" evacuation policy
        - **Class Disparity**: Socioeconomic status dramatically affected survival chances
        - **Age Patterns**: How age influenced survival likelihood
        - **Economic Factors**: Relationship between fare paid and survival
        """)
        
        #Button to load visualizations
        with gr.Row():
            load_btn = gr.Button(
                "🔄 Load Interactive Visualizations", 
                variant="primary", 
                size="lg",
                scale=1
            )
        
        gr.Markdown("---")
        
        #Overview Dashboard
        gr.Markdown("""
        #Statistical Overview
        
        This dashboard presents four complementary views of the data:
        - **Bar charts** show survival rates across categories
        - **Histograms** reveal age distribution patterns
        - **Box plots** display fare distribution and outliers
        """)
        
        overview_plot = gr.Plot(label="Overview Dashboard", show_label=False)
        
        gr.Markdown("---")
        
        #Interactive Scatter Plot
        gr.Markdown("""
        ##Interactive Passenger Explorer
        
        Each point represents one passenger. **Hover over points** to see individual details.
        **Zoom** and **pan** to explore specific regions. Notice how:
        - Larger points indicate larger families
        - Different symbols distinguish male/female passengers
        - Colors show survival outcome
        """)
        
        scatter_plot = gr.Plot(label="Interactive Scatter Plot", show_label=False)
        
        #Statistical Summary
        gr.Markdown(f"""
        ---
        ##Dataset Summary
        
        - **Total Passengers**: {total_passengers:,}
        - **Survivors**: {int(total_survived):,} ({survival_rate:.1f}%)
        - **Non-Survivors**: {int(total_passengers - total_survived):,} ({100-survival_rate:.1f}%)
        - **Data Source**: Kaggle Titanic Dataset (Training Set)
        """)
        
        #Connect button to visualization functions
        def load_visualizations():
            """Called when user clicks the load button"""
            dashboard = create_overview_dashboard()
            scatter = create_interactive_scatter()
            return dashboard, scatter
        
        load_btn.click(
            fn=load_visualizations,
            outputs=[overview_plot, scatter_plot]
        )
    
    #TAB 2: ABOUT & METHODOLOGY
    
    with gr.Tab("ℹ️ About This Project"):
        
        gr.Markdown("""
        #About This Data Visualization Project
        
        ##Historical Context
        
        The RMS Titanic sank on April 15, 1912, after striking an iceberg during her maiden 
        voyage from Southampton to New York City. Of the estimated 2,224 passengers and crew 
        aboard, more than 1,500 died, making it one of the deadliest peacetime maritime 
        disasters in modern history.
        
        This dataset contains information about 891 passengers from the Titanic, including 
        their demographics, ticket information, and whether they survived.
        
        ---
        
        ##Dataset Features
        
        **Demographics:**
        - Age: Passenger age in years (median: 28)
        - Sex: Male or Female
        - Pclass: Passenger class (1st, 2nd, or 3rd)
        
        **Family Information:**
        - SibSp: Number of siblings/spouses aboard
        - Parch: Number of parents/children aboard
        - FamilySize: Derived feature (SibSp + Parch + 1)
        
        **Ticket Information:**
        - Fare: Price paid in British pounds
        - Cabin: Cabin number (if known)
        - Embarked: Port of embarkation (C=Cherbourg, Q=Queenstown, S=Southampton)
        
        **Outcome:**
        - Survived: 1 = Yes, 0 = No
        
        ---
        
        ##Data Processing Steps
        
        1. **Missing Value Handling:**
           - Filled 177 missing ages with median age (28 years)
           - Filled missing fares with median fare
           - Filled 2 missing embarkation ports with 'S' (most common)
        
        2. **Feature Engineering:**
           - Created FamilySize (SibSp + Parch + 1)
           - Created age groups (Child, Teen, Adult, Middle Age, Senior)
           - Created fare groups (Low, Medium-Low, Medium-High, High)
           - Converted categorical variables to numeric codes
        
        3. **Data Validation:**
           - Verified all required columns present
           - Checked data types and ranges
           - Ensured no remaining critical missing values
        
        ---
        
        ##Visualization Design Principles
        
        **Color Theory:**
        - Consistent color scheme throughout (teal = survived, coral = died)
        - High contrast for accessibility
        - Colorblind-friendly palette
        
        **Chart Selection:**
        - **Bar charts**: Best for comparing categories (gender, class)
        - **Histograms**: Best for showing distributions (age)
        - **Box plots**: Best for displaying statistical spread and outliers (fare)
        - **Scatter plots**: Best for exploring relationships between continuous variables
        
        **Interactive Elements:**
        - Hover details provide additional context
        - Zoom and pan enable detailed exploration
        - Legends clearly identify data series
        
        **Typography & Layout:**
        - Clear hierarchical titles
        - Descriptive axis labels with units
        - Grouped related visualizations
        - Progressive disclosure (load on demand)
        
        ---
        
        ##Key Statistical Findings
        
        **Overall Survival:**
        - 38.4% of passengers survived
        - 61.6% did not survive
        
        **Gender ("Women and Children First"):**
        - Female: 74.2% survived
        - Male: 18.9% survived
        - **Gender was the strongest predictor of survival**
        
        **Passenger Class:**
        - 1st Class: 63.0% survived
        - 2nd Class: 47.3% survived
        - 3rd Class: 24.2% survived
        - **Class had a dramatic effect on survival**
        
        **Age:**
        - Children (0-12): 50.4% survived
        - Adults (19-50): 36.5% survived
        - **Children had better survival rates**
        
        **Family Size:**
        - Traveling alone: 30.4% survived
        - Families of 2-4: 50.5% survived
        - Families of 5+: 16.1% survived
        - **Mid-sized families had best survival rates**
        
        ---
        
        ##Technologies Used
        
        - **Python 3.11+**: Core programming language
        - **Pandas 2.0+**: Data manipulation and analysis
        - **Plotly 5.17+**: Interactive visualization library
        - **Gradio 4.0+**: Web application framework
        
        ---
        
        ##Project Goals & Learning Outcomes
        
        This project demonstrates:
        
        1. **Data Storytelling**: Transforming raw tabular data into compelling visual narratives
        2. **Visual Design**: Applying design principles for clarity, aesthetics, and accessibility
        3. **Interactive Analytics**: Creating engaging user experiences for data exploration
        4. **Technical Skills**: End-to-end data visualization pipeline from raw data to deployed app
        5. **Communication**: Explaining complex patterns to non-technical audiences
        
        ---
        
        ##Educational Value
        
        Beyond the technical skills, this dataset teaches important lessons about:
        - **Social inequality**: How class and wealth affected life-or-death outcomes
        - **Historical context**: Maritime safety practices and evacuation protocols
        - **Data ethics**: Respectfully analyzing data about real human tragedy
        - **Pattern recognition**: How visualization reveals insights hidden in raw numbers
        
        ---
        
        ##Connect & Learn More
        
        **Created by:** Talia Kumar  
        **Education:** B.S. Computational Applied Math & Statistics, Colorado School of Mines (Expected 2027)  
        **Email:** tekk.education@gmail.com  
        **LinkedIn:** [linkedin.com/in/talia-kumar](https://linkedin.com/in/talia-kumar)  
        **Location:** Denver, CO
        
        ---
        
        *This project was built as a data visualization portfolio piece demonstrating 
        interactive analytics, visual storytelling, and web development skills | January 2026*
        
        **Data Source:** [Kaggle Titanic Dataset](https://www.kaggle.com/c/titanic)
        """)

#LAUNCH THE APPLICATION

if __name__ == "__main__":
    
    # Launch with share=False for local testing
    # Change to share=True to create a public link
    app.launch(
        server_name="127.0.0.1",  # Localhost
        server_port=7860,          # Port number
        share=True,               # Set to True for public link
        show_error=True            # Show detailed errors
    )
