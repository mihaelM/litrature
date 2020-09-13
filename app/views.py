"""
Definition of views.
"""
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from datetime import datetime    
from .models import *
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
import simplejson
import json
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


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
            'app/login.html',
            {
                'title':'Login Page',
                'year':datetime.now().year,
            })

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password) #not solving none yet
        try:
            login(request, user)
        except:
            return HttpResponseNotFound('<h1>Login did not succeed.</h1>')
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
        print ("Attempt")
        profile_pic = UserDetails.objects.all().filter(user = username).defer("profile_pic")[0].profile_pic
    except:
        print("We did not made it")
        profile_pic = None
    
    # load songs of his, that's it basically

    songs = ArtPublish.objects.all().filter(author_id = username, genre = 'Poetry').defer("id", "title")

    #count posts first
    numOfPosts = ArtPublish.objects.all().filter(author_id = username).count()
    #print("broj {}".format(numOfPosts))
    numOfPosts += QuotePublish.objects.all().filter(author_id = username).count()

    #number of views of his art of course, what else

    numOfViews = x(ArtPublish.objects.all().filter(author_id = username).aggregate(Sum('views'))['views__sum'])

    numOfViews += x(QuotePublish.objects.all().filter(author_id = username).aggregate(Sum('views'))['views__sum'])

    # numer of upvotes of his art ofcourse

    numOfUpvotes = x(ArtPublish.objects.all().filter(author_id = username).aggregate(Sum('upvotes'))['upvotes__sum'])
    numOfUpvotes += x(QuotePublish.objects.all().filter(author_id = username).aggregate(Sum('upvotes'))['upvotes__sum'])
    

    return render(
        request,
        'app/profile.html', #add
        {
            'title':'Personal Page',
            'year':datetime.now().year,
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
        art = ArtPublish.objects.all().filter(author_id = username, genre = 'Poetry').defer("id", "title")  
    elif type == 'stories':
        art = ArtPublish.objects.all().filter(author_id = username, genre = 'Story').defer("id", "title")
    elif type =='quotes':
        art = QuotePublish.objects.all().filter(author_id = username, genre = 'Quote').defer("id", "title")
    
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
            'title':'Profile Page',
            'year':datetime.now().year,
            'username':request.user
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
              'title':'Write',
              'year':datetime.now().year,
            }
        )

    if request.method == 'POST':
        author_id = None #not got this yet
        if request.user.is_authenticated: #works, we will try with redirecting
            author_id = request.user
                
        date = datetime.now()
        views = 0
        upvotes = 0
        text = request.POST['text']
        genre = request.POST['art']
        title = request.POST['titleLit']
        

        #currently not used, maybe in future, but not for this project
        if 'draft' in request.POST:#i dalje ne radi meh...
            
            if genre == 'Quote': #big Q
                quoteEntry = QuoteDraft(author_id = author_id, date = date, text = text, genre = genre, title = title, originalauthor = request.POST['originalauthor']) #defined in myScript.js
                quoteEntry.save()
            else:
                entry = ArtDraft(author_id = author_id, date = date, text = text, genre = genre, title = title)
                entry.save()

                #note that it can be seen in drafts and redirect to profile
                print ("draft is not there, even tho")

            return HttpResponseRedirect(reverse('myprofile'))

        elif 'publish' in request.POST:
           
            originalauthor = None

            if genre == 'Quote': #big Q
                originalauthor = request.POST['originalauthor']
                quoteEntry = QuotePublish(author_id = author_id, date = date, views = views, upvotes = upvotes, text = text, genre = genre, title = title, originalauthor = originalauthor) #defined in myScript.js
                quoteEntry.save()
            else:
                entry = ArtPublish(author_id = author_id, date = date, views = views, upvotes = upvotes, text = text, genre = genre, title = title)
                entry.save()

            return publishLook(request, title, genre, date, request.user, originalauthor, text)

def publishLook (request, title, genre, date, user, originalauthor, text):
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
            'originalauthor':originalauthor,
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
            cnt = AuthorsUpvotes.objects.all().filter(author_id = request.user, type = type, art_id = id).count()

            ret = quote.upvotes
            # disabling multiple upvotes
            if not cnt > 0:
               
                ret += 1
                quote.upvotes = F('upvotes') + 1
                quote.save()
                upvote = AuthorsUpvotes(author_id = request.user, type = type, art_id = id)
                upvote.save()
           
        else:
            art = ArtPublish.objects.get(id = id)
            cnt = AuthorsUpvotes.objects.all().filter(author_id = request.user, type = type, art_id = id).count()

            ret = art.upvotes
            if not cnt > 0:
                ret += 1
                art.upvotes = F('upvotes') + 1
                art.save()
                upvote = AuthorsUpvotes(author_id = request.user, type = type, art_id = id)
                upvote.save()

        return HttpResponse(
            json.dumps({'upvotes':ret}),
            content_type="application/json"
         )


    return HttpResponse()


###look of publish art (poetry, quote, s. story)
def look(request, type, id):
    assert isinstance(request, HttpRequest)

    #look/type/id
    #works
    originalauthor = None
    hasIt = 0

    # should have used get, we'll try with that also..
    # allComments = []
    if type == 'quote':
        quote = QuotePublish.objects.get(id = id)

        title, genre, date, user, text, originalauthor, views, upvotes = quote.title, quote.genre, quote.date, quote.author_id, quote.text, quote.originalauthor, quote.views, quote.upvotes
        if request.method == 'GET':

            quote.views = F('views') + 1
            quote.save()

            # we should check if user has liked this particular quote in the beggining he surely did not
            hasIt = AuthorsUpvotes.objects.all().filter(author_id = quote.author_id, type = quote.genre, art_id = id).count()

        elif request.method == 'POST':
            comment = request.POST['comment']
           # print(comment)
            
            quotePublishComment = QuotePublishComment(author_id = request.user, quote_publish_id = quote, date = datetime.now(), text = comment)
            quotePublishComment.save()
        
        allComments = QuotePublishComment.objects.all().filter(quotepublish_id = quote).defer("author_id", "date", "text")[::-1]

        authorToPic = []

        for comment in allComments:
            rez = None
            try:
                rez = UserDetails.objects.all().filter(user = comment.author_id).defer("profile_pic")[0].profile_pic
            except:
                rez = None
            authorToPic.append(rez)

    else:
        art = ArtPublish.objects.get(id = id)

        title, genre, date, user, text, views, upvotes = art.title, art.genre, art.date, art.author_id, art.text, art.views, art.upvotes
        
        if request.method == 'GET':
            art.views = F('views') + 1
            art.save()

            hasIt = AuthorsUpvotes.objects.all().filter(author_id = art.author_id, type = art.genre, art_id = id).count()

            #gather all comments of this work

        elif request.method == 'POST':
            comment = request.POST['comment']

            artPublishComment = ArtPublishComment(author_id = request.user, artpublish_id = art, date = datetime.now(), text = comment)
            artPublishComment.save()
    

        allComments = ArtPublishComment.objects.all().filter(artpublish_id = art).defer("author_id", "date", "text")[::-1]

        authorToPic = []

        for comment in allComments:
            rez = None
            try:
                rez = UserDetails.objects.all().filter(user = comment.author_id).defer("profile_pic")[0].profile_pic
            except:
                rez = None
            authorToPic.append(rez)


       

    return render(
        request,
        'app/look.html', #add
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'id':id,
            'title':title,
            'genre':genre,
            'date':date,
            'author':user, #!author
            'text':text,
            'originalauthor':originalauthor,
            'views':views + 1,
            'upvotes':upvotes,
            'hasIt':hasIt,
            'zipped':zip(allComments, authorToPic)
        }
    )


def poetry(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)
  
    #ask for all poetry

    #link to author, hm, by name I guess, yeah that will have to be unique too .defer("pseudonime")

    #songs = ArtPublish.objects.all().prefetch_related("author_id").filter(genre = 'Poetry')
    #solution without joining tables ok :P

    # we can take only some rows
    songs = ArtPublish.objects.all().filter(genre = 'Poetry').defer("id", "title", "date", "author_id")[::-1]
    print(songs)

    return render(
        request,
        'app/poetry.html', #add
        {
           'title':'Home Page',
           'year':datetime.now().year,
           'songs':songs
        }
    )

def shortStories(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)
    stories = ArtPublish.objects.all().filter(genre = 'Story').defer("id", "title", "date", "author_id")[::-1]
    return render(
        request,
        'app/shortStories.html', #add
        {
           'title':'Home Page',
           'year':datetime.now().year,
           'stories':stories
        }
    )


def quotes(request):
    """Renders the quotes page."""
    assert isinstance(request, HttpRequest)

    allQuotes = QuotePublish.objects.all().defer("id", "title", "date", "author_id", "originalauthor")[::-1]
   
    return render(
        request,
        'app/quotes.html', #add
        {
           'title':'Home Page',
           'year':datetime.now().year,
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


    if request.method == 'POST' and request.FILES['pictureM']: #wohoho provjerio gore i proradilo
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            pseudonime = request.POST['pseudonime']
            favoriteBooks = request.POST['favoriteBooks']
            pic = request.FILES['pictureM']

            
            user = User.objects.create_user(username, email, password)
            user.save()
            print("Jos tu")
            userDetails = UserDetails(user = user, pseudonime = pseudonime, favorite_book = favoriteBooks, profile_pic = pic)
            userDetails.save()


            user = authenticate(username=username, password=password) #not solving none yet
            #print(username)
            #print(password)

            login(request, user)

            # we need to save it user details also
            return HttpResponseRedirect(reverse('myprofile'))
        except:
            return HttpResponseNotFound('<h1>Registering failed.</h1>')

    else:  

        return render(
            request,
            'app/register.html',
             {
                'title':'Home Page',
                'year':datetime.now().year,
             }
         )

        

#this is strange way to process database queryies we want to do (perheps get rid of some data), we just write them here, and call help route
def help(request):
        """Renders the home page."""
        assert isinstance(request, HttpRequest)


        QuotePublishComment.objects.all().delete()
        ArtPublishComment.objects.all().delete()

        return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )