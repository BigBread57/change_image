from django.urls import path

from api.public.picture.views import PictureListCreateApiView, PictureRetrieveDestroyApiView, PictureResizeApiView

app_name = 'picture'


urlpatterns = [
    path('', PictureListCreateApiView.as_view(), name='list_create_picture'),
    path('<int:pk>/', PictureRetrieveDestroyApiView.as_view(), name='list_create_picture'),
    path('<int:pk>/resize/', PictureResizeApiView.as_view(), name='resize_picture'),
]
