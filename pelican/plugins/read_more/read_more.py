"""
Read More
=========

This plugin inserts an inline "Read More" link into summary's last HTML element.
"""

import logging

from pelican import contents, signals
from pelican.generators import ArticlesGenerator
from pelican.utils import truncate_html_words

try:
    from lxml.etree import ParserError
    from lxml.html import fragment_fromstring, fragments_fromstring, tostring
except ImportError:
    raise Exception("Unable to find lxml. Read More requires lxml to be installed.")

logger = logging.getLogger(__name__)


def insert_into_last_element(html, element):
    """
    Function to insert an HTML element into another HTML fragment.
    example:
        html = '<p>paragraph1</p><p>paragraph2...</p>'
        element = '<a href="/read-more/">read more</a>'
        ---> '<p>paragraph1</p><p>paragraph2...<a href="/read-more/">read more</a></p>'
    """
    try:
        item = fragment_fromstring(element)
    except (ParserError, TypeError):
        item = fragment_fromstring("<span></span>")

    try:
        doc = fragments_fromstring(html)
        doc[-1].append(item)

        return b"".join(tostring(e) for e in doc).decode()
    except (ParserError, TypeError):
        return ""


def insert_read_more_link(instance):
    """
    Insert an inline "Read More" link into the last element of the summary
    :param instance:
    :return:
    """

    # only deals with Article type
    if type(instance) != contents.Article:
        logger.info("[read_more] Skipped: Content is not of type Article")
        return

    SUMMARY_END_SUFFIX = instance.settings.get("SUMMARY_END_SUFFIX", "...")
    SUMMARY_MAX_LENGTH = instance.settings.get("SUMMARY_MAX_LENGTH", 50)
    READ_MORE_LINK = instance.settings.get("READ_MORE_LINK", "<span>continue</span>")
    READ_MORE_LINK_FORMAT = instance.settings.get(
        "READ_MORE_LINK_FORMAT", '<a class="read-more" href="/{url}">{text}</a>'
    )

    logger.debug(f"[read_more] SUMMARY_MAX_LENGTH: {SUMMARY_MAX_LENGTH}")
    logger.debug(f"[read_more] READ_MORE_LINK: {READ_MORE_LINK}")
    logger.debug(f"[read_more] READ_MORE_LINK_FORMAT: {READ_MORE_LINK_FORMAT}")

    if not (SUMMARY_MAX_LENGTH and READ_MORE_LINK and READ_MORE_LINK_FORMAT):
        logger.error("[read_more] Abort: Settings not present")
        return

    summary = truncate_html_words(
        instance.content, SUMMARY_MAX_LENGTH, SUMMARY_END_SUFFIX
    )

    if not summary:
        logger.error(
            f"[read_more] Error: Summary truncation failed (None) -> \
            {instance.source_path}"
        )
        return

    if summary != instance.content:
        read_more_link = READ_MORE_LINK_FORMAT.format(
            url=instance.url, text=READ_MORE_LINK
        )
        logger.debug(f"[read_more] Format: {read_more_link}")
        logger.debug(f"[read_more] Summary (before inject): {summary}")
        result = insert_into_last_element(summary, read_more_link)
        if result:
            instance.metadata["summary"] = result
            logger.debug(
                f"[read_more] Summary (after inject): {instance.metadata['summary']}"
            )
        else:
            logger.error("[read_more] Error: Link not added to summary")


def run_plugin(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                insert_read_more_link(article)


def register():
    try:
        signals.all_generators_finalized.connect(run_plugin)
    except AttributeError:
        # NOTE: This may result in #314 so shouldn't really be relied on
        # https://github.com/getpelican/pelican-plugins/issues/314
        signals.content_object_init.connect(insert_read_more_link)
