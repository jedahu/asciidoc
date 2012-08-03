from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from os import linesep

def filter(_, lines, encoding='utf-8', language='text', src_numbered=False, **attrs):
  return highlight(
      linesep.join(lines),
      get_lexer_by_name(language, encoding=encoding),
      HtmlFormatter(linenos=bool(src_numbered), encoding=encoding))
