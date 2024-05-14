from django.urls import path
from . import views

urlpatterns = [
    path("images/", views.upload_image, name='upload_image'),  
]

# urlpatterns = [
#     path("images/", TemplateView.as_view(template_name='upload_image.html'), name='upload_image'),
# ]