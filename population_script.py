from django.contrib.auth.hashers import make_password
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'stock_exchange.settings')
import django
django.setup()
from baseapp.models import Game, Category, Offer, CustomUser, Profile, Subcategory
from django.core.files.images import ImageFile

def populate():
    users = [{"username":"nagibator777",
              "password":make_password("nagibator777"),
              "email": "nagibator777@gmail.com"},
             {"username":"lolka",
              "password":make_password("lolka123"),
              "email": "lolka123@gmail.com"}]
    chaos10 = {"title":"10 Chaos orb",
               "views":20,
               "price":10.55,
               "description":"",
               "user": "nagibator777",
               "type": "Custom",
               "quantity": 100,
               "rangestep": 10}
    exalt1 = {"title":"1 Exalt orb",
              "views":10,
              "price":30,
              "description":"",
              "user": "nagibator777"}
    kaomheart = {"title":"Kaom's heart",
                 "views":500,
                 "price":300,
                 "description":"",
                 "user": "nagibator777"}
    account1 = {"title":"Account with a lot",
                "views":100,
                "price":2000,
                "description":"Account with a lot of coins, skins and more..",
                "user": "lolka"}
    path_of_exile = [
        {"title":"Currency",
         "offers":[chaos10,exalt1]},
        {"title":"Items",
         "offers":[kaomheart]},
        {"title":"Accounts",
         "offers":[account1]}
    ]
    rotmg = [
        {"title":"Currency",
         "offers":[]},
        {"title":"Items",
         "offers":[]},
        {"title":"Accounts",
         "offers":[]}
    ]
    neverwinter = [
        {"title":"Currency",
         "offers":[]},
        {"title":"Items",
         "offers":[]},
        {"title":"Accounts",
         "offers":[]}
    ]
    games = {"Path of exile": {"categories": path_of_exile,
             "description": "Path of Exile is a free online-only action RPG under development by Grinding Gear Games in  2013",
             "logo": "poe_logo.png"},
             "Realm of the Mad God": {"categories": rotmg,
             "description": "Realm of the Mad God is a massively multiplayer online shooter video game co-created by Wild Shadow Studios and Spry Fox in 2011",
             "logo": "rotmg_logo.jpg"},
             "Neverwinter": {"categories": neverwinter,
             "description": "DescriptionNeverwinter is a free-to-play massively multiplayer online role-playing game developed by Cryptic Studios in 2013",
             "logo": "neverwinter_logo.png"}}
    for f in users:
        add_user(f["username"], f["password"], f["email"])
    u = CustomUser.objects.get_or_create(username="Peace", password=make_password("Peace"), email="iampeacemans@gmail.com", is_superuser=True, is_staff=True)
    u[0].save()
    p = Profile.objects.get_or_create(user=u[0], username=u[0].username)
    p[0].save()
    for p in users:
        add_profile(CustomUser.objects.get(username=p['username']), p['username'])

    for g, g_data in games.items():
        game = add_game(g, g_data["description"], g_data["logo"])
        print(game)
        for c in g_data["categories"]:
            category = add_category(c["title"], game)
            print(category)
            for o in c["offers"]:
                try:
                    add_offer(o["title"], o["views"], o["description"], o["price"], category, CustomUser.objects.get(username=o["user"]), o["type"], o["quantity"], o["rangestep"])
                except KeyError:
                    print(o["title"])
                    add_offer(o["title"], o["views"], o["description"], o["price"], category, CustomUser.objects.get(username=o["user"]))

def add_user(username, password, email):
    print(username)
    u = CustomUser.objects.get_or_create(username=username, password=password, email=email)[0]
    u.save()

def add_profile(user, username):
    p = Profile.objects.get_or_create(user=user, username=username)[0]
    p.save()

def add_game(name, description, logo):
    g = Game.objects.get_or_create(name=name, description=description, logo=ImageFile(open(logo, "rb")))[0]
    g.save()
    return g

def add_category(title, game):
    c = Category.objects.get_or_create(title=title, game=game)[0]
    c.save()
    return c

def add_offer(title, views, description, price, category, user, type=False, quantity=0, rangestep=0):
    if type:
        o = Offer.objects.get_or_create(title=title, views=views, description=description, price=price, category=category, user=user, type="Custom", quantity=quantity, rangestep=rangestep)[0]
    else:
        o = Offer.objects.get_or_create(title=title, views=views, description=description, price=price, category=category, user=user)[0]
    o.save()

if __name__ == '__main__':
    print("Starting population script...")
    populate()
