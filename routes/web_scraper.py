import requests
from bs4 import BeautifulSoup
import json

def scrape_interview_questions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    questions = []
    answers = []

    # Assuming questions are in <h2> tags and answers in <p> tags
    for question in soup.find_all('h2'):
        questions.append(question.text.strip())

    for answer in soup.find_all('p'):
        answers.append(answer.text.strip())

    return questions, answers

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def scrape_and_save_interview_questions():
    # Example URL, replace with actual interview question URLs
    url = 'https://example.com/interview-questions'
    questions, answers = scrape_interview_questions(url)
    interview_data = {'questions': questions, 'answers': answers}
    
    save_to_json(interview_data, 'interview_questions.json')
