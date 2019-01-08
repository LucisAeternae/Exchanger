from django.shortcuts import render, render_to_response, HttpResponse
from django.template.context import RequestContext
from baseapp.models import Game, Category, Offer, Profile
from baseapp.forms import UserForm, ProfileForm


def render_response(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)

def index(request):
    context_dict = {'games': Game.objects.order_by('-purchases')}
    context_dict['context_instance'] = RequestContext(request)
    return render_to_response('baseapp/index.html', context=context_dict)

def games(request, game_name_url):
    context_dict = {}
    context_dict['context_instance'] = RequestContext(request)
    try:
        game = Game.objects.get(slug=game_name_url)
        context_dict['game'] = game
        try:
            categories = Category.objects.filter(game=game)
            context_dict['categories'] = categories
        except Category.DoesNotExist:
            pass
    except Game.DoesNotExist:
        pass

    return render_to_response('baseapp/game.html', context=context_dict)

def categories(request, game_name_url, category_name_url):
    context_dict = {}
    context_dict['context_instance'] = RequestContext(request)
    try:
        game = Game.objects.get(slug=game_name_url)
        context_dict['game'] = game
        try:
            category = Category.objects.get(game=game, slug=category_name_url)
            context_dict['category'] = category
            try:
                offers = Offer.objects.filter(category=category)
                context_dict['offers'] = offers
            except Offer.DoesNotExist:
                pass
        except Category.DoesNotExist:
            pass
    except Game.DoesNotExist:
        pass
    return render_to_response('baseapp/Category.html', context=context_dict)

def offer(request, offer_id):
    context_dict = {}
    context_dict['context_instance'] = RequestContext(request)
    try:
        offer = Offer.objects.get(id=offer_id)
        context_dict['offer'] = offer
        price = float(offer.price)
        context_dict['price'] = price
    except Offer.DoesNotExist:
        pass
    return  render_to_response('baseapp/offer.html', context=context_dict)

def profile(request, username):
    context_dict = {}
    context_dict['context_instance'] = RequestContext(request)
    try:
        user = Profile.objects.get(username=username)
        context_dict['user'] = user
        offers = Offer.objects.filter(user=user)
        context_dict['offers'] = offers
    except Profile.DoesNotExist:
        pass
    return render_to_response('baseapp/profile.html', context=context_dict)

def singup(request):
    if request.user.is_authenticated:
        return HttpResponse('Your already logged in. <br><a href="/">Index</a>')
    else:
        registered = False
        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            profile_form = ProfileForm(data=request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                if 'avatar' in request.FILES:
                    profile.avatar = request.FILES['avatar']
                profile.save()
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
        else:
            user_form = UserForm()
            profile_form = ProfileForm()
        return render(request,
                      'registration/registration_form.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'registered': registered})
