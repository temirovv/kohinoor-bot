import html2text


async def text_to_html(text):
    h = html2text.HTML2Text()
    h.ignore_links = True
    html_message = h.handle(text)
    return html_message
