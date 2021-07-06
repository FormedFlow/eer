menu = [
    {'title': 'Уроки', 'url_name': 'lessons'},
    {'title': 'Контакты', 'url_name': 'contacts'},
    {'title': 'О сайте', 'url_name': 'about'}
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context

