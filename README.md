# AI Agent Information Retrieval Project

## Project Overview

This AI agent is designed to automatically retrieve and extract specific information from web sources based on user-defined queries. Users can upload a CSV or connect a Google Sheet, specify search parameters, and obtain structured data about entities in their dataset.

## Features

- CSV and Google Sheets file upload
- Dynamic web search for each entity
- Custom prompt-based information retrieval
- LLM-powered data extraction
- Results display and CSV download

## Prerequisites

- Python 3.8+
- API Keys:
  - Search API (SerpAPI/ScraperAPI)
  - LLM API (Groq/OpenAI)
  - Google Sheets API (optional)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-agent-project.git
cd ai-agent-project
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
- Create a `.env` file with:
  ```
  SEARCH_API_KEY=your_search_api_key
  LLM_API_KEY=your_llm_api_key
  ```

## Usage

1. Run the dashboard
```bash
streamlit run app.py
```

2. Upload your data file
3. Select the primary column
4. Enter your custom search query
5. Retrieve and download results

## Optional Advanced Features

- Multiple field extraction
- Direct Google Sheets output
- Robust error handling

## Technologies Used

- Dashboard: Streamlit
- Data Handling: pandas
- Search API: SerpAPI/ScraperAPI
- LLM: Groq/OpenAI GPT
- Backend: Python
- Agents: Langchain

## Limitations

- Respects web scraping terms of service
- Subject to API rate limits
- Dependent on web data availability

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.