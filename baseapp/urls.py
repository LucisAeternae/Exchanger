"""stock_exchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from baseapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('marketplace/<game_name_url>/', views.games, name='games'),
    path('marketplace/<game_name_url>/<category_name_url>/', views.categories, name='categories'),
    path('offer/<offer_id>/', views.offer, name='offer'),
    path('members/<username>/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('marketplace/<game_name_url>/<category_name_url>/add_offer/', views.add_offer, name='add_offer'),
    path('ajax/offer_status_change/', views.offer_status_change, name='offer_status_change'),
    path('member/<username>/add_money/', views.add_money, name='add_money'),
    path('member/<username>/zero_money/', views.zero_money, name='zero_money'),
    path('offer/<offer_id>/purchase/', views.purchase, name='purchase'),
    path('offer/<offer_id>/purchase/<int:quantity>/', views.purchase, name='purchase'),
    path('add_game/', views.add_game, name='add_game'),
    path('add_category/', views.add_category, name='add_category'),
    path('search/', views.search, name='search')

]
