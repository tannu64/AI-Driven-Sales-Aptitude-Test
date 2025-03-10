# AI-Driven Psychometric Sales Aptitude Test

An interactive, AI-powered assessment tool designed to evaluate sales aptitude through psychometric principles.

## Overview

This application provides organizations with a sophisticated tool to identify top sales talent based on psychological insights. The test combines traditional psychometric assessment methods with modern AI algorithms to deliver real-time scoring and personalized feedback.

## Features

- **Interactive Assessment**: Engaging question formats that adapt based on previous responses
- **AI-Powered Analysis**: Advanced algorithms that evaluate responses beyond simple scoring
- **Real-time Feedback**: Immediate insights for both test-takers and administrators
- **Comprehensive Reporting**: Detailed analysis of strengths, weaknesses, and potential
- **Scientific Foundation**: Based on established psychometric principles and sales performance research

## Results Visualization

The application provides comprehensive visual results after completing the assessment:

- **Overall Score**: A summary score reflecting overall sales aptitude
- **Category Breakdown**: Detailed scores across different sales competency areas
- **Strengths & Areas for Development**: Personalized feedback on strong points and improvement areas
- **Recommendations**: AI-generated suggestions for career development

Sample result screens can be found in the `Results` folder (images 1-6).

## Technical Architecture

- **Frontend**: Responsive web interface built with HTML, CSS, JavaScript
- **Backend**: Python Flask API server
- **AI Models**: TensorFlow and scikit-learn for response analysis and scoring
- **Database**: SQL database for storing assessment data and results
- **Authentication**: Secure login system for administrators and test-takers

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sales-aptitude-test.git
   cd sales-aptitude-test
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

## Project Structure

```
sales-aptitude-test/
├── src/
│   ├── models/        # AI models and algorithms
│   ├── data/          # Data processing and management
│   ├── utils/         # Utility functions
│   └── frontend/      # Frontend controllers
├── templates/         # HTML templates
├── static/            # Static assets (CSS, JS, images)
├── tests/             # Test suite
├── migrations/        # Database migrations
├── .env               # Environment variables
├── config.py          # Configuration settings
├── app.py             # Application entry point
└── README.md          # Project documentation
```

## Development Roadmap

- [x] Project setup and architecture design
- [x] Question bank development
- [x] AI model training for response analysis
- [x] Frontend interface implementation
- [x] Scoring algorithm refinement
- [x] User testing and feedback collection
- [ ] Performance optimization
- [x] Documentation and deployment

## Developer Contact

This project was developed by Tanveer Hussain.

- **Email**: agapaitanveermou@gmail.com
- **Upwork**: [Tanveer Hussain on Upwork](https://www.upwork.com/freelancers/~01a14d825a9bd8689d)
- **LinkedIn**: [Tanveer Hussain on LinkedIn](https://www.linkedin.com/in/tanveer-hussain-277119196/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Research in sales psychology and performance metrics
- Open-source AI and psychometric assessment tools
- Contributors and testers who provided valuable feedback 