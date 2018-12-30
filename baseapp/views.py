from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from baseapp.models import Game, Category, Offer


def index(request):
    context_dict = {'games': Game.objects.order_by('-purchases')}
    return render_to_response('baseapp/index.html', context=context_dict)

def games(request, game_name_url):
    context_dict = {}
    try:
        game = Game.objects.get(slug=game_name_url)
        context_dict["game"] = game
        try:
            categories = Category.objects.filter(game=game)
            context_dict["categories"] = categories
        except Category.DoesNotExist:
            pass
    except Game.DoesNotExist:
        pass

    return render_to_response('baseapp/game.html', context=context_dict)

def categories(request, game_name_url, category_name_url):
    context_dict = {}
    try:
        game = Game.objects.get(slug=game_name_url)
        context_dict["game"] = game
        try:
            category = Category.objects.get(game=game, slug=category_name_url)
            context_dict["category"] = category
            try:
                offers = Offer.objects.filter(category=category)
                context_dict["offers"] = offers
            except Offer.DoesNotExist:
                pass
        except Category.DoesNotExist:
            pass
    except Game.DoesNotExist:
        pass
    return render_to_response('baseapp/Category.html', context=context_dict)
