from django.http import Http404, HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView
)

from .forms import EditProfileForm, PostForm, CommentForm
from .models import Post, Category, User, Comment


POSTS_ON_PAGE = 10


class CheckAccessMixin(UserPassesTestMixin):

    def test_func(self):
        instance = SingleObjectMixin.get_object(self)
        return self.request.user == instance.author

    def handle_no_permission(self):
        return HttpResponseForbidden('Недостаточно прав')


class ReverseToPageMixin():

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.kwargs['pk']})


class OneAndManyOjectsMixin(SingleObjectMixin):

    def get(self, request, *args, **kwargs):
        self.object = SingleObjectMixin.get_object(
            self, queryset=self.queryset)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset_to_view = self.object.blogs_posts.count_comment()
        if self.object != self.request.user:
            return queryset_to_view.published_post(
            ).published_category()
        return queryset_to_view


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'slug': self.request.user})


class PostUpdateView(
    CheckAccessMixin, ReverseToPageMixin, LoginRequiredMixin, UpdateView
):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = 'blog:post_detail'

    def handle_no_permission(self):
        return redirect(self.success_url, pk=self.kwargs['pk'])


class PostDeleteView(CheckAccessMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = context['post']
        form = {'instance': instance}
        context['form'] = form
        return context


class PostDetailView(UserPassesTestMixin, DetailView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'blog/detail.html'

    def test_func(self):
        self.object = SingleObjectMixin.get_object(self)
        if self.object not in Post.objects.published_post(
        ).published_category():
            return self.object.author == self.request.user
        return True

    def handle_no_permission(self):
        raise Http404('Страница не найдена')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostListView(ListView):
    model = Post
    paginate_by = POSTS_ON_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.select_related(
            'location'
        ).published_post(
        ).published_category(
        ).count_comment()


class ProfileDetailView(OneAndManyOjectsMixin, ListView):
    queryset = User.objects.all()
    slug_field = 'username'
    template_name = 'blog/profile.html'
    paginate_by = POSTS_ON_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context


class CategoryListView(OneAndManyOjectsMixin, ListView):
    queryset = Category.objects.filter(is_published=True)
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'category_slug'
    paginate_by = POSTS_ON_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'slug': self.request.user})


class CommentUpdateView(
        CheckAccessMixin, ReverseToPageMixin, LoginRequiredMixin, UpdateView
):
    queryset = Comment.objects.all()
    form_class = CommentForm
    pk_url_kwarg = 'comment_pk'
    template_name = 'blog/create.html'
    success_url = 'blog:post_detail'


class CommentDeleteView(CheckAccessMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, ReverseToPageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_url = 'blog:post_detail'

    def dispatch(self, request, *args, **kwargs):
        self.commented_post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.commented_post
        return super().form_valid(form)
