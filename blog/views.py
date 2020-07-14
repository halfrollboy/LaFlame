from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #Отображенеи только по 3 элемента на стр
    page = request.GET.get('page')
    print('Стрианица',page)
    print('',object_list)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) #Если номер страницы не является целым числом, возвращаем первую страницу
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)#получаем список объектов на нужной странице с помощью метода page()
    return render(request,'blog/list.html',{'posts':posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',publish__year=year,publish__month=month,publish__day=day)
    print(' iam TUT')
    return render(request,'blog/detail.html',{'post': post})


def post_share(request, post_id):
 # Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id,status='published')
    sent = False
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # Отправка электронной почты.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'stikshel@gmail.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post': post, 'form': form, 'sent': sent})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'