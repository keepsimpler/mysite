"""News listing and detail pages"""
from django.db import models
from wagtail.core.models import Page


class NewsListingPage(Page):
    """Listing page lists all the News Detail Pages."""
    template = "news/news_listing_page.html"
    subpage_types = ['news.NewsDetailPage']

    def get_child_pages(self):
        return self.get_children().public().live()

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = self.get_child_pages().order_by('-first_published_at')


class NewsDetailPage(Page):
    """Parental news detail page."""

    subpage_types = []
    parent_page_types = ['news.NewsListingPage']
    news_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='新闻标题'
    )