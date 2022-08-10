from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from core import views, urls

#router = routers.DefaultRouter()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
from core.views import *

urlpatterns = [
    path('help/', home),
    path('register/', RegisterView.as_view()),
    path('login/', MyObtainTokenPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('', UserOperationAPI.as_view()),   # POST -> update profile, PUT -> update pw, GET -> get_data, DELETE -> delete user
    path('', include(urls))
]



