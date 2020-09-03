"""Stream fields live in here.
The reason to inherit standard Wagtail blocks is to customize templating of my blocks
"""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class SecondLevelTitleBlock(blocks.CharBlock):
    class Meta:  # noqa
        template = "streams/second_level_title_block.html"
        icon = "edit"
        label = "二级标题"


class ImageChooserBlock(ImageChooserBlock):
    class Meta:  # noqa
        template = "streams/image_chooser_block.html"
        # icon = "edit"
        label = "新闻图片"


class MainTextBlock(blocks.RichTextBlock):
    class Meta:  # noqa
        template = "streams/main_text_block.html"
        icon = "doc-full"
        label = "正文段落"
