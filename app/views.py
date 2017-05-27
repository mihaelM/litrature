"""
Definition of views.
"""
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime    
from models import *
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
import simplejson
import json

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )



def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def quotes(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html', #add
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )



def mylogin(request):

    if request.method == 'GET':
        return render (
             request,
            'app/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password) #not solving none yet
        login(request, user)

        return HttpResponseRedirect(reverse('myprofile'))

#httpredirect not so good

def x(input):
    return 0 if input is None else input

def myprofile(request):
    """Renders the my profile page."""
    assert isinstance(request, HttpRequest)
   # print (request.POST['username'])
    username = request.user
    
    try:
        profile_pic = UserDetails.objects.all().filter(user = username).defer("profile_pic")[0]
    except:
        profile_pic = None
    
    # load songs of his, that's it basically

    songs = ArtPublish.objects.all().filter(author_ID = username, genre = 'Poetry').defer("id", "title")

    #count posts first
    numOfPosts = ArtPublish.objects.all().filter(author_ID = username).count()
    #print("broj {}".format(numOfPosts))
    numOfPosts += QuotePublish.objects.all().filter(author_ID = username).count()

    #number of views of his art of course, what else

    numOfViews = x(ArtPublish.objects.all().filter(author_ID = username).aggregate(Sum('views'))['views__sum'])

    numOfViews += x(QuotePublish.objects.all().filter(author_ID = username).aggregate(Sum('views'))['views__sum'])

    # numer of upvotes of his art ofcourse

    numOfUpvotes = x(ArtPublish.objects.all().filter(author_ID = username).aggregate(Sum('upvotes'))['upvotes__sum'])
    numOfUpvotes += x(QuotePublish.objects.all().filter(author_ID = username).aggregate(Sum('upvotes'))['upvotes__sum'])
    

    return render(
        request,
        'app/profile.html', #add
        {
            'username':username,
            'songs' : songs,
            'numOfPosts' : numOfPosts,
            'numOfViews': numOfViews,
            'numOfUpvotes': numOfUpvotes,
            'profile_pic': profile_pic
        }
    )

#takes 2 argument 1, given...
@csrf_exempt
def loadData(request, type): ###we do not need 2 instances of type, but we can pretend for now
    """loads data for post object"""

    #some errors, we comment it for now, since no need for that
    """
    assert isinstance(request, HttpRequest)
    JSONdata = request.POST['data']
    dict = simplejson.JSONDecoder().decode( JSONdata ) 

    type = dict['type']
    """
    username = request.user

    returnList = None #this is stupid name

    if type == 'poetry':      
        art = ArtPublish.objects.all().filter(author_ID = username, genre = 'Poetry').defer("id", "title")  
    elif type == 'stories':
        art = ArtPublish.objects.all().filter(author_ID = username, genre = 'Story').defer("id", "title")
    elif type =='quotes':
        art = QuotePublish.objects.all().filter(author_ID = username, genre = 'Quote').defer("id", "title")
    
    dictArt = {}

    for i, art_instance in enumerate(art):
        dictArt[i] = {'id':art_instance.id, 'title': art_instance.title}

    print(dictArt)

    return HttpResponse(
            json.dumps(dictArt),
            content_type="application/json"
     )





def renderProfile(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/profile.html', #add
        {
            'username':username
        }
    )

def write(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)
    print("L1")
    if request.method == 'GET':
        return render(
            request,
            'app/write.html', #add
            {
            
            }
        )

    if request.method == 'POST':
        author_ID = None #not got this yet
        if request.user.is_authenticated: #works, we will try with redirecting
            author_ID = request.user
                
        date = datetime.now()
        views = 0
        upvotes = 0
        text = request.POST['text']
        genre = request.POST['art']
        title = request.POST['titleLit']
        

        if 'draft' in request.POST:#i dalje ne radi meh...
            
            if genre == 'Quote': #big Q
                quoteEntry = QuoteDraft(author_ID = author_ID, date = date, text = text, genre = genre, title = title, originalAuthor = request.POST['originalAuthor']) #defined in myScript.js
                quoteEntry.save()
            else:
                entry = ArtDraft(author_ID = author_ID, date = date, text = text, genre = genre, title = title)
                entry.save()

                #note that it can be seen in drafts and redirect to profile
                print ("draft is not there, even tho")

            return HttpResponseRedirect(reverse('myprofile'))

        elif 'publish' in request.POST:
           
            originalAuthor = None

            if genre == 'Quote': #big Q
                originalAuthor = request.POST['originalAuthor']
                quoteEntry = QuotePublish(author_ID = author_ID, date = date, views = views, upvotes = upvotes, text = text, genre = genre, title = title, originalAuthor = originalAuthor) #defined in myScript.js
                quoteEntry.save()
            else:
                entry = ArtPublish(author_ID = author_ID, date = date, views = views, upvotes = upvotes, text = text, genre = genre, title = title)
                entry.save()

            return publishLook(request, title, genre, date, request.user, originalAuthor, text)

def publishLook (request, title, genre, date, user, originalAuthor, text):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/look.html', #add
        {
            'title':title,
            'genre':genre,
            'date':date,
            'user':user,
            'text':text,
            'originalAuthor':originalAuthor,
            'views':0,
            'upvotes':0           
        }
    )

@csrf_exempt
def upvote(request, type, id):
    
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        #actually we will increase number just with javascript, and this is just for updating database..
        #hm i should know if it is art or quote, for now let's pretend....
        print('HERE WE ARE')
        if type == 'quote':
            quote = QuotePublish.objects.get(id = id)
            quote.upvotes = F('upvotes') + 1
            quote.save()
            upvote = AuthorsUpvotes(author_ID = request.user, type = type, art_ID = id)
            upvote.save()
           
        else:
            art = ArtPublish.objects.get(id = id)
            art.upvotes = F('upvotes') + 1
            art.save()
            upvote = AuthorsUpvotes(author_ID = request.user, type = type, art_ID = id)
            upvote.save()

        return HttpResponse()
    """   return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
    """

    return HttpResponse()



def look(request, type, id):
    assert isinstance(request, HttpRequest)

    #look/type/id
    #works
    originalAuthor = None
    hasIt = 0

    # should have used get, we'll try with that also..
    if type == 'quote':
        quote = QuotePublish.objects.get(id = id)

        title, genre, date, user, text, originalAuthor, views, upvotes = quote.title, quote.genre, quote.date, quote.author_ID, quote.text, quote.originalAuthor, quote.views, quote.upvotes
        
        quote.views = F('views') + 1
        quote.save()

        # we should check if user has liked this particular quote in the beggining he surely did not
        hasIt = AuthorsUpvotes.objects.all().filter(author_ID = quote.author_ID, type = quote.genre, art_ID = id).count()



    else:
        art = ArtPublish.objects.get(id = id)

        title, genre, date, user, text, views, upvotes = art.title, art.genre, art.date, art.author_ID, art.text, art.views, art.upvotes   
        
        art.views = F('views') + 1
        art.save()

        hasIt = AuthorsUpvotes.objects.all().filter(author_ID = art.author_ID, type = art.genre, art_ID = id).count()


    return render(
        request,
        'app/look.html', #add
        {
            'title':title,
            'genre':genre,
            'date':date,
            'author':user, #!author
            'text':text,
            'originalAuthor':originalAuthor,
            'views':views + 1,
            'upvotes':upvotes,
            'hasIt':hasIt
        }
    )


def poetry(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)
  
    #ask for all poetry

    #link to author, hm, by name I guess, yeah that will have to be unique too .defer("pseudonime")

    #songs = ArtPublish.objects.all().prefetch_related("author_ID").filter(genre = 'Poetry')
    #solution without joining tables ok :P

    # we can take only some rows
    songs = ArtPublish.objects.all().filter(genre = 'Poetry').defer("id", "title", "date", "author_ID")
    

    return render(
        request,
        'app/poetry.html', #add
        {
           'songs':songs 
           
        }
    )

def shortStories(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)
    stories = ArtPublish.objects.all().filter(genre = 'Story').defer("id", "title", "date", "author_ID")
    return render(
        request,
        'app/shortStories.html', #add
        {
            'stories':stories
        }
    )


def quotes(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)

    allQuotes = QuotePublish.objects.all().defer("id", "title", "date", "author_ID", "originalAuthor")
   
    return render(
        request,
        'app/quotes.html', #add
        {
            'quotes':allQuotes
        }
    )

def profileSearch(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/profileListing.html', #add
        {
            
        }
    )


def register(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)
    #print("ARE WE EVEN HERE")


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        pseudonime = request.POST['pseudonime']
        favoriteBooks = request.POST['favoriteBooks']
        pic = request.POST['pic']

        user = User.objects.create_user(username, email, password)
        user.save()

        userDetails = UserDetails(user = user, pseudonime = pseudonime, favorite_book = favoriteBooks, profile_pic = pic)
        userDetails.save()


        user = authenticate(username=username, password=password) #not solving none yet
        #print(username)
        #print(password)

        login(request, user)

        # we need to save it user details also
        return HttpResponseRedirect(reverse('myprofile'))
    else:  

        return render(
            request,
            'app/register.html'
        )
     
