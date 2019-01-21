from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect, reverse
from django.template.context import RequestContext
from baseapp.models import Game, Category, Offer, Profile, CustomUser, Purchases
from baseapp.forms import UserForm, ProfileForm, BaseOfferForm, CustomOfferForm, NewGameForm, NewCategoryForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from django.http import JsonResponse
from django.utils import timezone
from djmoney.money import Money
from django.contrib import messages

def index(request):
    context_dict = {'games': Game.objects.order_by('-purchases')}
    return render(request, 'baseapp/index.html', context=context_dict)

def games(request, game_name_url):
    context_dict = {}
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

    return render(request, 'baseapp/game.html', context=context_dict)

def categories(request, game_name_url, category_name_url):
    context_dict = {}
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
    return render(request, 'baseapp/Category.html', context=context_dict)

def offer(request, offer_id):
    context_dict = {}
    try:
        offer = Offer.objects.get(id=offer_id)
        context_dict['offer'] = offer
        price = float(offer.price)
        context_dict['price'] = price
    except Offer.DoesNotExist:
        pass
    return  render(request, 'baseapp/offer.html', context=context_dict)

def profile(request, username):
    context_dict = {}
    try:
        user = CustomUser.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        context_dict['user_profile'] = profile
        offers = Offer.objects.filter(user=user)
        context_dict['offers'] = offers
        if request.user.username == profile.username:
            purchases = Purchases.objects.filter(customer=profile)
            context_dict['purchases'] = purchases
    except CustomUser.DoesNotExist:
        pass
    return render(request, 'baseapp/profile.html', context=context_dict)

def signup(request):
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
                login(request, user)
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

def signin(request):
    context_dict = {}
    try:
        next_page = request.GET['next']
    except MultiValueDictKeyError:
        next_page = False
    if request.user.is_authenticated:
        return HttpResponseRedirect(next_page)
    if request.user.is_authenticated:
        return HttpResponse('Your already logged in. <br><a href="/">Index</a>')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if next_page:
                        return HttpResponseRedirect(next_page)
                    else:
                        return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('Your account is disabled')
            else:
                print('Invalid {0}, {1}'.format(username, password))
                return HttpResponse('Invalid login details supplied')
        else:
            return render(request, 'registration/login.html', context=context_dict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def add_offer(request, game_name_url, category_name_url):
    baseoffer_form = BaseOfferForm(data=request.POST)
    customoffer_form = CustomOfferForm(data=request.POST)
    game = False
    category = False
    offer_added = False
    try:
        game = Game.objects.get(slug=game_name_url)
        try:
            category = Category.objects.get(game=game, slug=category_name_url)
        except:
            pass
    except:
        pass
    if request.method == 'POST':
        if baseoffer_form.is_valid() and customoffer_form.is_valid():
            if baseoffer_form.cleaned_data['type'] == 'Base':
                offer = baseoffer_form.save(commit=False)
                offer.category = category
                offer.user = request.user
                offer.save()
            else:
                title = baseoffer_form.cleaned_data['title']
                description = baseoffer_form.cleaned_data['description']
                price = baseoffer_form.cleaned_data['price']
                type = baseoffer_form.cleaned_data['type']
                quantity = customoffer_form.cleaned_data['quantity']
                rangestep = customoffer_form.cleaned_data['rangestep']
                user = request.user
                offer = Offer.objects.create(title=title,
                                             description=description,
                                             price=price, type=type,
                                             quantity=quantity,
                                             rangestep=rangestep, user=user,
                                             category=category)
            offer_added = True
        else:
            print(baseoffer_form.errors)
    else:
        baseoffer_form = BaseOfferForm()
        customoffer_form = CustomOfferForm()
    return render(request,
                  'baseapp/add_offer.html',
                  {'baseoffer_form': baseoffer_form,
                   'customoffer_form': customoffer_form,
                   'game': game,
                   'category': category,
                   'offer_added': offer_added})

def offer_status_change(request):
    username = request.user.username
    offer = Offer.objects.get(id=request.GET.get('offer'))
    data = {
        'success': False,
        'pause': False,
        'delete': False
    }
    if offer.user.username == username:
        if request.GET.get('button') in ("active-btn play-btn",
                                         "active-btn pause-btn"):
            if (timezone.now()-offer.datetimemodified).total_seconds() > 5:
                offer.active = not offer.active
                offer.datetimemodified = datetime.datetime.now()
                offer.save()
                data['success'] = True
                data['pause'] = True
        elif request.GET.get('button') in ("active-btn delete-btn"):
            offer.delete()
            data['success'] = True
            data['delete'] = True
    return JsonResponse(data)

def add_money(request, username):
    if request.user.username == username:
        profile = Profile.objects.get(username=username)
        profile.money += Money(1000, 'USD')
        profile.save()
    return HttpResponseRedirect(reverse('profile', args=[username]))

def zero_money(request, username):
    if request.user.username == username:
        profile = Profile.objects.get(username=username)
        profile.money = Money(0, 'USD')
        profile.save()
    return HttpResponseRedirect(reverse('profile', args=[username]))

def purchase(request, offer_id, quantity=0):
    try:
        offer = Offer.objects.get(id=offer_id)
    except Offer.DoesNotExist:
        messages.error(request, 'Offer does not exist!')
        return HttpResponseRedirect(reverse('index'))
    try:
        profile = Profile.objects.get(username=request.user.username)
    except Profile.DoesNotExist:
        messages.warning(request, 'You must be logged in!')
        return HttpResponseRedirect(reverse('offer', args=[offer.id]))
    if request.user.username == offer.user.username:
        messages.warning(request, 'You cannot buy from yourself!')
        return HttpResponseRedirect(reverse('offer', args=[offer.id]))
    if offer.type == 'base':
        if profile.money < offer.price:
            messages.warning(request, 'Not enough money!')
            return HttpResponseRedirect(reverse('offer', args=[offer.id]))
        else:
            seller = Profile.objects.get(username=offer.user.username)
            profile.money -= offer.price
            seller.money += offer.price
            Purchases.objects.create(customer=profile,offer_title=offer.title,
                        offer_seller=seller.username,
                        offer_price=offer.price)
            profile.save()
            seller.save()
            offer.delete()
            messages.success(request, 'Purchase is success!')
            return HttpResponseRedirect(reverse('index'))
    else:
        if quantity == 0:
            messages.warning(request, 'You have to choose something to buy.')
            return HttpResponseRedirect(reverse('offer', args=[offer.id]))
        if offer.quantity < quantity:
            messages.warning(request, 'Not enough product!')
            return HttpResponseRedirect(reverse('offer', args=[offer.id]))
        else:
            if profile.money < offer.price*quantity:
                messages.warning(request, 'Not enough money!')
                return HttpResponseRedirect(reverse('offer', args=[offer.id]))
            else:
                seller = Profile.objects.get(username=offer.user.username)
                total_price = offer.price*quantity
                profile.money -= total_price
                seller.money += total_price
                Purchases.objects.create(customer=profile,
                            offer_title=offer.title,
                            offer_seller=seller.username, offer_type='Custom',
                            offer_price=total_price,
                            purchase_quantity=quantity)
                if offer.quantity == quantity:
                    offer.delete()
                else:
                    offer.quantity -= quantity
                    offer.save()
                profile.save()
                seller.save()
                messages.success(request, 'Purchase is success!')
                return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('offer', args=[offer.id]))

def add_game(request):
    if request.user.is_staff:
        if request.method == 'POST':
            new_game_form = NewGameForm(data=request.POST)
            if new_game_form.is_valid():
                game = new_game_form.save(commit=False)
                if 'logo' in request.FILES:
                    game.logo = request.FILES['logo']
                game.save()
                messages.success(request, 'Creating new game was success!')
                return HttpResponseRedirect(reverse('index'))
            else:
                print(new_game_form.errors)
        else:
            new_game_form = NewGameForm()
        return render(request, 'baseapp/add_game.html', {'new_game_form': new_game_form})
    else:
        messages.warning(request, 'Staff only!')
        return HttpResponseRedirect(reverse('index'))

def add_category(request):
    if request.user.is_staff:
        if request.method == 'POST':
            new_category_form = NewCategoryForm(data=request.POST)
            if new_category_form.is_valid():
                category = new_category_form.save()
                messages.success(request, 'Creating new category was success!')
                return HttpResponseRedirect(reverse('games', args=[category.game.slug]))
            else:
                print(new_category_form.errors)
        else:
            new_category_form = NewCategoryForm()
        return render(request, 'baseapp/add_category.html', {'new_category_form': new_category_form})
    else:
        messages.warning(request, 'Staff only!')
        return HttpResponseRedirect(reverse('index'))

def get_offer_list(max_results=0, query=''):
    offers_list = []
    if query:
        offers_list = Offer.objects.filter(title__icontains=query)
    if max_results > 0:
        if len(offers_list) > max_results:
            offers_list = offers_list[:max_results]
    return offers_list

def search(request):

    offers = []
    contains = ''
    if request.method == 'GET':
        contains = request.GET['suggestion']
        print(contains)
    offers = get_offer_list(8, contains)
    return render(request, 'baseapp/offers.html',
                  {'offers': offers})
