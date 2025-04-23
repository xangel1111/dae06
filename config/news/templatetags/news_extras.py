from django import template
import re

register = template.Library()


@register.filter(name="truncate_words_html")
def truncate_words_html(value, arg):
    """
    Truncates HTML to a certain number of words.
    Preserves HTML tags.
    
    Usage: {{ text|truncate_words_html:50 }}
    """
    try:
        length = int(arg)
    except ValueError:
        return value
    
    if not value:
        return ""
    
    # Count words while preserving HTML tags
    words_to_return = length
    
    # Split by spaces but preserve HTML tags
    tag_pattern = r'(<[^>]+>|[^<>\s]+)'
    splitted = re.findall(tag_pattern, value)
    
    # Loop through and count
    result = []
    word_count = 0
    
    for part in splitted:
        if not part.startswith('<'):
            word_count += 1
            if word_count > words_to_return:
                result.append('...')
                break
        result.append(part)
    
    return ''.join(result)


@register.filter(name="reading_time")
def reading_time(value):
    """
    Estimates reading time for an article.
    
    Usage: {{ article.content|reading_time }}
    """
    if not value:
        return "0 min read"
    
    # Count words (roughly)
    word_count = len(value.split())
    
    # Average reading speed: 200 words per minute
    minutes = max(1, word_count // 200)
    
    if minutes == 1:
        return "1 min read"
    else:
        return f"{minutes} min read"