from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from os import linesep

def filter(lines, encoding='utf-8', language='text', src_numbered=False, **attrs):
  lexer = get_lexer_by_name('text', encoding=encoding)
  try:
    lexer = get_lexer_by_name(language, encoding=encoding)
  except Exception:
    pass
  return highlight(
      linesep.join(lines),
      lexer,
      HtmlFormatter(linenos=bool(src_numbered), encoding=encoding))
