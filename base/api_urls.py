from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('program/', include('program.api_urls')),
    path('user/', include('user.api_urls')),
]
