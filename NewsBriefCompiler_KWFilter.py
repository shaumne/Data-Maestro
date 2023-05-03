import os
import requests
from bs4 import BeautifulSoup
import openai
import time

# Set the API key
openai.api_key = '<your-api-key-here>'

def chat_gpt(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].message['content'].strip()
    return message

def scrape_headlines(url, selector, keywords):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    if isinstance(selector, str):
        headlines = soup.select(selector)
    else:
        headlines = soup.find_all(*selector)

    filtered_headlines = [headline.text.strip() for headline in headlines if any(keyword.lower() in headline.text.lower() for keyword in keywords)]

    return filtered_headlines

sources = [
    {"name": "Reuters", "url": "https://www.reuters.com", "selector": 'a[data-testid="Heading"]'},
    {"name": "CBC", "url": "https://www.cbc.ca/news", "selector": "h3"},
    {"name": "BlogTO", "url": "https://www.blogto.com/", "selector": "p.article-thumbnail-title > span.article-thumbnail-title-text"},
    {"name": "Al Jazeera", "url": "https://www.aljazeera.com", "selector": "h3"},
    {"name": "BBC", "url": "https://www.bbc.com/", "selector": "h3"},
    {"name": "BNN", "url": "https://www.bnnbloomberg.ca", "selector": "h2"},
    {"name": "Financial Times", "url": "https://www.ft.com", "selector": "a[data-trackable='heading-link'] > span"},
    {"name": "The Star", "url": "https://www.thestar.com/", "selector": ".c-mediacard__heading > span[data-test-id='mediacard-headline']"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/", "selector": ".fc-item__title .js-headline-text"},
    {"name": "Washington Post", "url": "https://www.washingtonpost.com", "selector": "div.headline.relative.gray-darkest.pb-xs > h2 > a > span"},
    {"name": "The Hill", "url": "https://thehill.com", "selector": "h1.featured-cards__small__headline > a"},
    {"name": "BetaKit", "url": "https://betakit.com", "selector": "h2"},
    {"name": "Nikkei Asia", "url": "https://asia.nikkei.com/", "selector": "h2"},
    {"name": "Bloomberg", "url": "https://www.bloomberg.com/", "selector": "h3"},
    {"name": "Politico", "url": "https://www.politico.com", "selector": "h2"},
    {"name": "The Atlantic", "url": "https://www.theatlantic.com", "selector": "h2"},
    {"name": "Wired", "url": "http://wired.com", "selector": "h2"},
    {"name": "Wall Street Journal", "url": "https://www.wsj.com", "selector": "h3"},
    {"name": "Arab News", "url": "https://www.arabnews.com", "selector": "h2"},
    {"name": "Nature", "url": "https://www.nature.com/news", "selector": "h3"},
    {"name": "Science", "url": "https://www.science.org/news", "selector": "a.sc-8pb8t8-0.bmSGPg.sc-1tsrr2n-1.gJcTsX"},
    {"name": "National Post", "url": "https://nationalpost.com", "selector": "h3"},
    {"name": "Business Insider", "url": "https://www.businessinsider.com", "selector": "a[data-analytics-area='links']"},
    {"name": "The Globe and Mail", "url": "https://www.theglobeandmail.com", "selector": "h2.Headline__StyledHeadline-sc-1d2q0wc-0"},
    {"name": "TSN", "url": "https://www.tsn.ca", "selector": "h4"},
    {"name": "ESPN", "url": "https://www.espn.com", "selector": "h2"},
    {"name": "The Score", "url": "https://www.thescore.com", "selector": "span.Headlines__headlineText--2a4Hx"},
    {"name": "The Players' Tribune", "url": "https://www.theplayerstribune.com", "selector": "h3"},
    {"name": "Seeking Alpha", "url": "https://seekingalpha.com/market-news/", "selector": ('a', {'data-test-id': 'post-list-item-title'})},
]

def create_summary_prompt(sources, political_view, challenge_reinforce, tone, keywords, profession, favourite_artist, output_type):
    prompt = f"You are a genius information analyst who can easily read large amounts of data to concisely summarize key points and trends in any output style including songs. Your task is to: (1) read the news stories below and (2) concisely summarize the most relevant 3-5 topics about the following keywords: {', '.join(keywords)}. Your output style should be a: {output_type.capitalize()} with a {tone.capitalize()} tone. Personalize your point of view for a {profession} who is politically {political_view.capitalize()} that wants to {challenge_reinforce.replace('_', ' ').capitalize()}. Please include a relevant quote or lyric from {favourite_artist} at the end of your essay to reinforce a key theme of your analysis. News stories below are not in any particular order:\n\n"

    for source in sources:
        source_name = source["name"]
        headlines = source["headlines"]
        for headline in headlines[:5]:
            prompt += f"- {source_name}: {headline}\n"

    return prompt

def get_summary(keywords, political_view, challenge_reinforce, tone, profession, favourite_artist, output_type):
    for source in sources:
        source["headlines"] = scrape_headlines(source["url"], source["selector"], keywords)

    summary_prompt = create_summary_prompt(sources, political_view, challenge_reinforce, tone, keywords, profession, favourite_artist, output_type)

    summary_response = chat_gpt(summary_prompt)
    return summary_response

def get_user_keywords():
    user_input = input("Enter keywords separated by commas: ")
    user_keywords = [keyword.strip() for keyword in user_input.split(",")]
    return user_keywords