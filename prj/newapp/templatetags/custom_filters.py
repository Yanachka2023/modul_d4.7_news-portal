from django import template

# если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их искать и фильтры потеряются
register = template.Library()

bad_words = {
    'фигня':'ф****я',
    'олух': 'о**х',
}

@register.filter()

def censor(value, code='bad_words'):
   """
   value: значение, к которому нужно применить фильтр
   """
   postfix = code

   return f'{value} {postfix}'






