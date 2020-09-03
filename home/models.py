from django.db import models

from wagtail.core.models import Page


class HomePage(Page):
    template = "home/home_page.html"
    subpage_types = [
        'news.NewsListingPage',
    ]
