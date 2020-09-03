"""News listing and detail pages"""
from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
# from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from streams import blocks


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
        # @todo add Pagination
        return context


class NewsDetailPage(Page):
    """Parental news detail page."""

    template = "news/news_detail_page.html"
    parent_page_types = ['news.NewsListingPage']
    news_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='新闻标题'
    )

    content = StreamField(
        [
            ("二级标题", blocks.SecondLevelTitleBlock(max_length=100, help_text='二级标题')),
            ("新闻图片", blocks.ImageChooserBlock(help_text='新闻图片')),
            ("正文段落", blocks.MainTextBlock(help_text='正文段落')),  # @todo, features=['bold','italic','link']
        ],
        null=True,
        blank=True,
    )

    # content can be displayed in Admin
    content_panels = Page.content_panels + [
        FieldPanel("news_title"),
        StreamFieldPanel("content"),
    ]