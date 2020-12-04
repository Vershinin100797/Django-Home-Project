from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView, DeleteView
from .exceptions import PermissionDenied
from bulletinboard import models
from .models import Post, Category, Profile
from .forms import AnnouncementPostForm, LoginForm, SignupForm, UpdateProfileForm, CommentForm


class HomePageView(ListView):
    model = Post
    template_name = 'bulletinboard/index.html'
    context_object_name = "latest_announcements"

    def get_queryset(self):
        return models.Post.objects.annotate()[:8]


class AnnouncementsPageView(View):
    template_name = 'bulletinboard/announcements.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {}
            posts = models.Post.objects.annotate()
            context['announcements'] = posts
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)


class AnnouncementView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    comment_form = CommentForm
    template_name = 'bulletinboard/announcement_detail.html'

    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['comments'] = models.Comment.objects.filter(in_post__pk=post_id).order_by('-date_publish')
        context['comment_form'] = None
        if request.user.is_authenticated:
            context['comment_form'] = self.comment_form
        return self.render_to_response(context)

    @method_decorator(login_required)
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        form = self.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.date_publish = timezone.now()
            comment.author = request.user
            comment.in_post = post
            comment.save()
            return render(request=request, template_name=self.template_name, context={'comment_form': self.comment_form,
                                                                                      'post': post,
                                                                                      'comments': post.comment_set.order_by(
                                                                                          '-date_publish')})
        else:
            return render(request=request, template_name=self.template_name, context={'comment_form': form,
                                                                                      'post': post,
                                                                                      'comments': post.comment_set.order_by(
                                                                                          '-date_publish')})


class CategoryView(View):
    template_name = 'bulletinboard/category.html'

    def get(self, request, *args, **kwargs):
        context = {}
        category = models.Category.objects.annotate()
        context['categories_list'] = category
        return render(request, self.template_name, context)


class AnnouncementCategoryView(View):
    pk_url_kwarg = 'category_id'
    template_name = 'bulletinboard/announcement_category.html'

    def get(self, request, category_id, *args, **kwargs):
        context = {}
        category = models.Post.objects.filter(category__pk=category_id)
        context['announcement_categories'] = category
        return render(request, self.template_name, context)


class CreateAnnouncementView(CreateView):
    form_class = AnnouncementPostForm
    template_name = 'bulletinboard/create_announcement.html'

    @method_decorator(login_required)
    def post(self, request,  *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.author = request.user
            post.save()
            context['post_was_created'] = True
            context['form'] = self.form_class
            return render(request=request, template_name=self.template_name, context=context)
        else:
            context['post_was_created'] = False
            context['form'] = form
            return render(request=request, template_name=self.template_name, context=context)


class EditAnnouncementView(UpdateView):
    model = models.Post
    pk_url_kwarg = 'post_id'
    template_name = 'bulletinboard/edit_announcement.html'
    form_class = AnnouncementPostForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("You are not author of this post")
        return super(EditAnnouncementView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('bulletinboard:announcement_detail', args=(post_id, ))


class DeleteAnnouncementView(DeleteView):
    model = models.Post
    pk_url_kwarg = 'post_id'
    template_name = 'bulletinboard/delete_announcement.html'

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('bulletinboard:delete_post_success', args=(post_id,))


from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.http import Http404


class LoginView(LoginView):
    template_name = 'my_auth/login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('bulletinboard:home'), request)
            else:
                context = {}
                context['form'] = form
                return render(request=request, template_name=self.template_name, context=context)
        else:
            context = {'form': form}
            return render(request=request, template_name=self.template_name, context=context)


class SignupView(View):
    template_name = 'my_auth/signup.html'
    registration_form = SignupForm

    def get(self, request, *args, **kwargs):
        context = {'form': self.registration_form}
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user_form = SignupForm(data=request.POST)
        registered = False
        if user_form.is_valid():
            user = user_form.save(commit=True)
            user.email = user_form.cleaned_data['email']
            user.save()
            registered = True
            return render(request, 'my_auth/signup.html',
                          {'registered': registered})
        else:
            return render(request, 'my_auth/signup.html',
                          {'form': user_form,
                           'registered': registered})


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("bulletinboard:home"))


class ProfileView(DetailView):
    model = Profile
    template_name = 'bulletinboard/profile.html'

    def get_object(self):
        return get_object_or_404(Profile, user__id=self.kwargs['user_id'])


class EditProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'bulletinboard/edit_profile.html'
    slug_field = "user_id"
    slug_url_kwarg = "user_id"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404("It is not your profile!")
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user_id = self.kwargs['user_id']
        return reverse('bulletinboard:profile', args=(user_id,))
