from django.urls import include, path

app_name = 'public'

urlpatterns = [
    path('images/', include('api.public.picture.urls', namespace='picture')),
]
