import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://www.theonion.com/latest"

    content = session.get(url, verify=True).content
    soup = BSoup(content, "html.parser")
    News = soup.find_all('div', class_='sc-cw4lnv-13 hHSpAQ')
    for article in News:
        # main = article.find_all('a')[0]
        # link = main['href']
        # image_src = str(main.find('img')['src']).split(" ")[-1]
        title = article.find('h2', class_='sc-759qgu-0 cvZkKd sc-cw4lnv-6 TLSoz').text.strip()
        link = article.find('div', class_='sc-cw4lnv-5 dYIPCV').a['href']
        image = article.find('img')['data-src']
        # title = main['title']
        if image:
            new_headline = Headline()
            new_headline.title = title
            new_headline.url = link
            new_headline.image = image
            new_headline.save()
    return redirect("../")

def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "news/home.html", context)
