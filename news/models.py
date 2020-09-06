"""News listing and detail pages"""
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
# from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from streams import blocks


# class NewsListingListingPage(Page):
#     """Listing of listing page lists list of news"""
#     template = "news/news_listing_listing_page.html"
#     subpage_types = [
#         'news.NewsListingPage',
#         'news.NewsListingListingPage',  # 列表页的子页面也可以是列表页，即列表页可以嵌套
#     ]
#
#     class Meta:
#         verbose_name = "栏目页"
#         verbose_name_plural = "栏目页"
#

class NewsListingPage(Page):
    """Listing page lists News Detail Pages."""
    template = "news/news_listing_page.html"
    subpage_types = [
        'news.NewsListingPage',  # 列表页的子页面也可以是列表页，即列表页可以嵌套
        'news.NewsDetailPage',
    ]

    def get_child_pages(self):
        #  find all the NewsDetailPage that is descendants of current page
        return self.get_descendants().type(NewsDetailPage).public().live()
        # return self.get_children().public().live()

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)

        # Get urls and titles of all ancestors and Self
        ancestors = [(ancestor.url, ancestor.title) for ancestor in self.get_ancestors()[1:]]
        ancestors += [(self.url, self.title)]
        context['ancestors'] = ancestors

        # Get all posts
        all_posts = self.get_child_pages().order_by('-first_published_at')

        # Paginate all posts by 20 per page
        paginator = Paginator(all_posts, per_page=1)
        # Try to get the ?page=x value
        page = request.GET.get('page')
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int, show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts

        return context

    class Meta:
        verbose_name = "文章列表页"
        verbose_name_plural = "文章列表页"


class NewsDetailPage(Page):
    """Parental news detail page."""

    template = "news/news_detail_page.html"
    # parent_page_types = ['news.NewsListingPage']
    subpage_types = []
    news_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='新闻标题',
        verbose_name='新闻标题',
    )
    #  是否头条
    is_taotiao = models.BooleanField(verbose_name='是否头条', default=False)

    content = StreamField(
        [
            ("二级标题", blocks.SecondLevelTitleBlock(max_length=100, help_text='二级标题')),
            ("新闻图片", blocks.ImageChooserBlock(help_text='新闻图片')),
            ("正文段落", blocks.MainTextBlock(help_text='正文段落')),  # @todo, features=['bold','italic','link']
        ],
        null=True,
        blank=True,
        verbose_name="新闻内容"
    )

    # content can be displayed in Admin
    content_panels = Page.content_panels + [
        FieldPanel("news_title"),
        FieldPanel("is_taotiao"),
        StreamFieldPanel("content"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        first_published_date = self.first_published_at.strftime("%Y-%m-%d")
        context['first_published_date'] = first_published_date
        ancestors = [(ancestor.url, ancestor.title) for ancestor in self.get_ancestors()[1:]]
        context['ancestors'] = ancestors
        parent_title = self.get_parent().title
        context['parent_title'] = parent_title
        return context

    class Meta:
        verbose_name = "文章内容页"
        verbose_name_plural = "文章内容页"

