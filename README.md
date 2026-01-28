#Titanic Survival Analysis & Visualization

An interactive data visualization web application exploring survival patterns from the 1912 Titanic disaster. Built with Python, Plotly, and Gradio.

**[View Live Application](https://huggingface.co/spaces/SteveTheTurtl3/titanic-survival-visualization)**

#Features

- **Interactive Dashboard**: 4-panel statistical overview with bar charts, histograms, and box plots
- **Exploratory Scatter Plot**: Drill down into individual passengers with hover details
- **Real-time Interactivity**: Zoom, pan, and hover to explore data patterns
- **Professional Design**: Consistent color scheme, clear typography, accessible layout
- **Comprehensive Documentation**: Methodology, insights, and data processing steps included

#Key Insights Revealed

- **Gender Effect**: Women had 74% survival rate vs 19% for men ("women and children first" policy)
- **Class Disparity**: 1st class passengers were 2.5x more likely to survive than 3rd class
- **Age Patterns**: Children under 12 had 50% survival rate vs 36% for adults
- **Family Size**: Mid-sized families (2-4 members) had highest survival rates

#Technologies

- **Python 3.11+**: Core language
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualization library
- **Gradio**: Web application framework
- **Hugging Face Spaces**: Deployment platform

#Project Structure
titanic-survival-visualization/
├── app.py                 # Main application
├── train.csv              # Dataset (891 passengers)
├── requirements.txt       # Python dependencies
└── README.md             # Documentation

#Local Installation
```bash
# Clone repository
git clone https://github.com/SteveTheTurtl3/titanic-survival-visualization.git
cd titanic-survival-visualization

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Application will be available at `http://127.0.0.1:7860`

#Visualization Highlights

#Overview Dashboard
- **Bar Charts**: Survival rates by gender and passenger class
- **Histograms**: Age distribution comparison between survivors and non-survivors
- **Box Plots**: Fare distribution revealing economic disparities

#Interactive Scatter Plot
- Each point = one passenger
- Color = survival outcome
- Symbol = gender
- Size = family size
- Hover = detailed passenger information

#Design Principles

- **Color Consistency**: Teal (#4ECDC4) for survived, Coral (#FF6B6B) for died
- **Chart Selection**: Appropriate visualization types for each data relationship
- **Interactive Elements**: Hover, zoom, pan for user-driven exploration
- **Accessibility**: Clear labels, high contrast, colorblind-friendly palette

#Data Source

Dataset from [Kaggle Titanic Competition](https://www.kaggle.com/c/titanic)
- 891 passengers from RMS Titanic
- 12 features including demographics, ticket info, survival outcome
- Training set used for visualization

#Author

**Talia Kumar**
- B.S. Computational Applied Math & Statistics, Colorado School of Mines (Expected 2027)
- Email: tekk.education@gmail.com
- LinkedIn: [linkedin.com/in/talia-kumar](https://linkedin.com/in/talia-kumar)
- Location: Denver, CO

#License

MIT License - feel free to use this project for learning and portfolio purposes

#Acknowledgments

- Kaggle for providing the Titanic dataset
- Plotly for excellent visualization library
- Gradio for easy web deployment
- Hugging Face for free hosting
