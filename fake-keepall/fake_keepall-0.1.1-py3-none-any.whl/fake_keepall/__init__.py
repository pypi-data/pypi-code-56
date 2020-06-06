from bs4 import BeautifulSoup, NavigableString
import click


def apply_fake_keep_all(element, custom_class=None):
    words = element.string.split(' ')
    if len(words) <= 1:
        return

    parent = element.parent
    parent.clear()
    tmp_soup = BeautifulSoup(features='html.parser')
    for word in words:
        if not word:
            continue
        span_tag = tmp_soup.new_tag('span')
        span_tag.append(word)
        # Use the custom CSS class instead of style property
        if custom_class is not None:
            span_tag['class'] = custom_class
        else:
            span_tag['style'] = 'white-space: nowrap;'
        parent.append(span_tag)
        parent.append(' ')


def conv(parent_element, whitelist_tags=['p', 'li'], custom_class=None):
    for child in parent_element.children:
        if isinstance(child, NavigableString):
            if not child.string.strip():
                continue
            # print(child.string, child.parent.name)  # for debug
            if not whitelist_tags or child.parent.name in whitelist_tags:
                apply_fake_keep_all(child, custom_class)
            continue
        conv(child, whitelist_tags, custom_class)


def convert_html(html: str, whitelist_tags=None, custom_class=None):
    soup = BeautifulSoup(html, 'html.parser')
    conv(soup.body, whitelist_tags, custom_class)
    return soup.prettify()


@click.command()
@click.option('-t', '--tags', type=str,
              help='Specifies whitelist tags separated by commas')
@click.option('-c', '--class', 'custom_class', type=str,
              help='Set a custom CSS class name to use instead of CSS style')
@click.argument('infile', type=click.File('r', encoding='utf-8'))
@click.argument('outfile', type=click.File('w', encoding='utf-8'))
def cli(infile, outfile, tags, custom_class):
    html = infile.read()
    whitelist_tags = None
    if tags:
        whitelist_tags = [t.strip() for t in tags.split(',')]
    outhtml = convert_html(html, whitelist_tags, custom_class)
    outfile.write(outhtml)


if __name__ == '__main__':
    cli()
