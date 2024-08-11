from routes.web_scraper import scrape_and_save_interview_questions
from routes.json_creator import create_and_save_industry_keywords

def main():
    # Choose the task you want to run

    # To scrape interview questions and save to a JSON file
    scrape_and_save_interview_questions()

    # To create industry keywords JSON file
    create_and_save_industry_keywords()

if __name__ == '__main__':
    main()
