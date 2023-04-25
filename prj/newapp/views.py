# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .filters import PostFilter, C, F, X
from .forms import PostForm
from .models import Post, Comment
from django.urls import reverse

from datetime import datetime

def multiply(request):
   number = request.GET.get('number')
   multiplier = request.GET.get('multiplier')

   try:
       result = int(number) * int(multiplier)
       html = f"<html><body>{number}*{multiplier}={result}</body></html>"
   except (ValueError, TypeError):
       html = f"<html><body>Invalid input.</body></html>"

   return HttpResponse(html)

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2



    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_publication'] = "Чуть позже сообщим о предстоящих публикациях!"
        context['filterset'] = self.filterset
        return context

    def user_list(request):
        f = F(request.GET, queryset=User.objects.all())
        return render(request, 'user_t.html', {'filter': f})

    def posts_list(request):
        c = C(request.GET, queryset=Post.objects.all())
        return render(request, 'post_t.html', {'filter': c})

    def comment_list(request):
        x = X(request.GET, queryset=Comment.objects.all())
        return render(request, 'comment_t.html', {'filter': x})




class PostDetail(DetailView):
        # Модель всё та же, но мы хотим получать информацию по отдельному товару
        model = Post
        # Используем другой шаблон — post.html
        template_name = 'post.html'
        # Название объекта, в котором будет выбранный пользователем продукт
        context_object_name = 'post'

class PostCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_create.html'



    def create_post(request):

        form = PostForm()

        if request.method == 'POST':
            form = PostForm(request.POST)
            form.save()
            return HttpResponseRedirect('/posts/')
        form = PostForm()
        return render(request, 'post_create.html', {'form': form})




class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts')

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class PostDelete(DeleteView):
        model = Post
        template_name = 'post_delete.html'
        queryset = Post.objects.all()
        success_url = reverse_lazy('post_delete')

        def get_success_url(self):
            return reverse('post_delete', kwargs={'pk': self.object.pk})

class PostSearch(ListView):
        model = Post
        template_name = 'post_search.html'
        context_object_name = 'post_search'
        ordering = ['-time_of_creation']

        def get_queryset(self):
            queryset = super().get_queryset()
            self.filterset = PostFilter(self.request.GET, queryset)

            if not self.request.GET:
                return queryset.none()

            return self.filterset.qs

        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
                return context