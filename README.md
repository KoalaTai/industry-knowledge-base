# Industry Knowledge Base

## Overview
This project is designed to scrape industry-specific interview questions and create JSON files containing relevant industry keywords and jargon.

## Project Structure
- `main.py`: Entry point to run the scripts.
- `routes/`: Contains the main scripts:
  - `web_scraper.py`: A basic web scraper for interview questions.
  - `enhanced_scraper.py`: An optimized version of the web scraper with additional features.
  - `json_creator.py`: Script to create industry keywords JSON files.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/KoalaTai/industry-knowledge-base.git
   cd industry-knowledge-base
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- To scrape interview questions:
  ```bash
  python main.py
  ```
- To create industry keywords JSON:
  ```bash
  python main.py
  ```

## Future Enhancements
- Implement a more robust scraping method for complex websites.
- Add more industry-specific keywords.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
