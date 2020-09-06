import re

from django.db import models

from wagtail.core.models import Page

from news.models import NewsDetailPage, NewsListingPage


class HomePage(Page):
    template = "home/home_page.html"
    subpage_types = [
        'news.NewsListingPage',
        'news.NewsDetailPage',
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # find the most important news
        most_important_news = NewsDetailPage.objects.filter(is_taotiao=True)[0]

        rich_text = most_important_news.content[0].value.source  # @todo non rich text field may happen
        clean = re.compile('<.*?>')
        most_important_news_description = re.sub(clean, '', rich_text)[:75] + '...'

        context['most_important_news'] = most_important_news
        context['most_important_news_description'] = most_important_news_description

        # first list: 统战要闻
        news_list = NewsListingPage.objects.filter(title='统战要闻')[0]
        first_list_title = news_list.title
        first_list_url = news_list.url
        first_list = NewsDetailPage.objects.descendant_of(news_list).order_by('-first_published_at')[:5]
        context['first_list'] = first_list
        context['first_list_title'] = first_list_title
        context['first_list_url'] = first_list_url

        # second list: 通知公告
        news_list = NewsListingPage.objects.filter(title='通知公告')[0]
        second_list_title = news_list.title
        second_list_url = news_list.url
        second_list = NewsDetailPage.objects.descendant_of(news_list).order_by('-first_published_at')[:4]
        context['second_list'] = second_list
        context['second_list_title'] = second_list_title
        context['second_list_url'] = second_list_url

        # third list: 党外代表人士风采
        news_list = NewsListingPage.objects.filter(title='党外代表人士风采')[0]
        third_list_title = news_list.title
        third_list_url = news_list.url
        third_list = NewsDetailPage.objects.descendant_of(news_list).order_by('-first_published_at')[:5]
        context['third_list'] = third_list
        context['third_list_title'] = third_list_title
        context['third_list_url'] = third_list_url


        return context


