from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView
)

from .forms import EditProfileForm, PostForm, CommentForm
from .models import Post, Category, User, Comment
from .cbv_mixins import (
    CheckAccessMixin, OneAndManyOjectsMixin, ReverseToPageMixin
)


POSTS_ON_PAGE = 10


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    slug_url_kwarg = 'user'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'slug': self.request.user})


class PostUpdateView(
    CheckAccessMixin, ReverseToPageMixin, UpdateView,
):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def handle_no_permission(self):
        return redirect(self.success_url, pk=self.kwargs['pk'])


class PostDeleteView(CheckAccessMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        print('печать объекта', self.object)
        print('печать form', context['form'])
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.author != self.request.user:
            self.object = super().get_object(Post.objects.published_post(
            ).published_category())
            return self.object
        return self.object

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
        return reverse_lazy('blog:profile', kwargs={'slug': self.request.user})


class CommentUpdateView(
        CheckAccessMixin, ReverseToPageMixin, UpdateView
):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_pk'
    template_name = 'blog/create.html'


class CommentDeleteView(CheckAccessMixin, DeleteView):
    queryset = Comment.objects.all()
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, ReverseToPageMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        commented_post = super().get_object(Post.objects.all())
        if commented_post.author != self.request.user:
            commented_post = super().get_object(
                Post.objects.published_post().published_category())
        form.instance.post = commented_post
        return super().form_valid(form)
