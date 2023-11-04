from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.urls import reverse


class CheckAccessMixin(UserPassesTestMixin, SingleObjectMixin,
                       LoginRequiredMixin):

    def test_func(self):
        instance = self.get_object()
        return self.request.user == instance.author

    def handle_no_permission(self):
        return HttpResponseForbidden('Недостаточно прав')


class ReverseToPageMixin(object):
    success_url = 'blog:post_detail'
    slug_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse(self.success_url,
                       kwargs={self.slug_url_kwarg:
                               self.kwargs[self.slug_url_kwarg]})


class OneAndManyOjectsMixin(SingleObjectMixin):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset_to_view = self.object.blogs_posts.count_comment()
        if self.object != self.request.user:
            return queryset_to_view.published_post(
            ).published_category()
        return queryset_to_view
