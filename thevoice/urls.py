"""thevoice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from team import views as team_views
from performance import views as performance_views
from score import views as score_views

# NOTE: We don't have to define django urls in each app
# as we can utilize django rest framework default router
router = routers.DefaultRouter()

router.register(r'teams',
                team_views.TeamViewSet,
                base_name='teams')

router.register(r'performances',
                performance_views.PerformanceViewSet,
                base_name='performances')

router.register(r'scores',
                score_views.ScoreViewSet,
                base_name='scores')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/', obtain_jwt_token, name='login'),

    # NOTE: The below urls are optional
    # They are used by django rest framework browsable api
    # and django admin panel
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
