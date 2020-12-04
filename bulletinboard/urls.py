from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from .views import *

app_name = 'bulletinboard'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('announcement/', AnnouncementsPageView.as_view(), name='announcements'),
    path('announcement/<int:post_id>', AnnouncementView.as_view(), name='announcement_detail'),
    path('categories/<int:category_id>', AnnouncementCategoryView.as_view(), name='announcements_categories'),
    path('create/', CreateAnnouncementView.as_view(), name='create_announcement'),
    path('announcement/<int:post_id>/edit/', EditAnnouncementView.as_view(), name='edit_announcement'),
    path('announcement/<int:post_id>/delete/', login_required(DeleteAnnouncementView.as_view()),
         name='delete_announcement'),
    path('announcement/<int:post_id>/delete_success', TemplateView.as_view(
         template_name='bulletinboard/delete_success.html'), name='delete_post_success'),
]

from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetCompleteView

PasswordResetConfirmView.success_url = reverse_lazy('bulletinboard:password_reset_complete')

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('<int:user_id>/profile/', ProfileView.as_view(), name='profile'),
    path('<int:user_id>/profile/edit', login_required(EditProfileView.as_view()), name='edit_profile'),
    path('password-reset/', PasswordResetView.as_view(success_url=reverse_lazy('bulletinboard:password_reset_done'),
                                                      template_name='my_auth/password_reset.html',
                                                      email_template_name="my_auth/password_reset_email.html"),
         name='password_reset'),

    path('password-reset/done', PasswordResetDoneView.as_view(template_name='my_auth/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset/<str:uidb64>/<slug:token>', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('password_reset_complete'), template_name='my_auth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset/complete', PasswordResetCompleteView.as_view(
        template_name='my_auth/password_reset_complete.html'),
         name='password_reset_complete'
        ),

]
