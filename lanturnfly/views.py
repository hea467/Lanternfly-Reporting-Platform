from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

from lanturnfly.forms import LoginForm, RegisterForm, ReportForm

from lanturnfly.models import Profile, Spotting, Post, Comment
from json import dumps
import json
# Create your views here.

@login_required
def map(request):
    context = {}

    users_report = []
    fly_report = []
    usernames_report = []
    leaderboard = dict()

    for r in Spotting.objects.all():
        users_report.append((r.latitude, r.longitude))
        fly_report.append((r.see_num, r.kill_num, r.tree_num))
        usernames_report.append(r.user.username)

        
        leaderboard[r.user] = leaderboard.get(r.user, 0) + r.kill_num
    

    leaderboardList = []
    for key, value in leaderboard.items():
        leaderboardList.append((key, value))
    
    sortedLeaderList = sorted(leaderboardList,  key = lambda x: x[1], reverse=True)
    context['leaderList'] = sortedLeaderList

    
    report = dumps(users_report, cls=DjangoJSONEncoder)
    reporting_flys = dumps(fly_report, cls=DjangoJSONEncoder)
    # print(reporting_flys)

    context['username'] = usernames_report
    

    context['reports'] = report
    context['reporting_flys'] = reporting_flys
    return render(request, 'lanturnfly/map.html', context)



def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)

def add_report(request):
    if request.method == 'GET':
        context = {}
        context['form'] = ReportForm()
        return render(request, 'lanturnfly/addreport.html', context)
    print("HIIIIIII")
    form = ReportForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {}
        context['form'] = ReportForm()
        context['error'] = "YOU DID NOT CLICK MAP NOW I REAP UR SOULL MUhAhAhA?"
        return render(request, 'lanturnfly/addreport.html', context)
    if "latitude" not in request.POST or not request.POST["latitude"]: 
        return _my_json_error_response("CLICK DA MAPPP", status=400)
    if "longtitude" not in request.POST or not request.POST["longtitude"]: 
        return _my_json_error_response("did you hear me I said click ittt", status=400)
    print(request.POST["latitude"])
    pic = form.cleaned_data["image"]
    kill = form.cleaned_data["kill_num"]
    see = form.cleaned_data["see_num"]
    tree = form.cleaned_data["tree_num"]
    lat = form.cleaned_data["latitude"]
    lon = form.cleaned_data["longtitude"]
    if kill > see : 
        context = {}
        context['form'] = ReportForm()
        context['error'] = "Really....? You're lying. You can't kill more than you see. Lie better!!!"
        return render(request, 'lanturnfly/addreport.html', context)
    new_item = Spotting(latitude=lat, longitude=lon, user = request.user, kill_num = kill, see_num = see, tree_num = tree, picture = pic )
    new_item.save()
    return redirect("add_report")


def logout_action(request):
    logout(request)
    return redirect(reverse('home'))

# def all_report_debug(request):
#     context = {}
#     context['reports']= Spotting.objects.all()
#     return render(request, 'lanturnfly/debug.html', context)

def my_report(request):
    context = {}
    users_report = []
    for r in Spotting.objects.all():
        if (r.user.id == request.user.id) :
            users_report.append(r)
    context['reports'] = users_report
    context['first_name'] = request.user.first_name
    return render(request, 'lanturnfly/myreport.html', context )

def get_photo(request, id):
    report = get_object_or_404(Spotting, id=id)
    if not report.picture:
        raise Http404
    return HttpResponse(report.picture, content_type=report.content_type)


#Maggie try stupid things
#heatmap is now the new my_profile_actionlol
def heatmap(request):
    context = {}
    users_report = []
    try:
        user_profile = Profile.objects.get(id=request.user.id)
    except:
        new_profile = Profile(user=request.user)
        new_profile.save()
        user_profile = Profile.objects.get(id=request.user.id)

    print(user_profile.following.all())


    killed = 0
    reportNum = 0
    seen = 0
    trees = 0
    leaderboard = dict()

    flysKilled = []

    for r in Spotting.objects.all():
        if (r.user.id == request.user.id) :
            users_report.append((r.latitude, r.longitude))
            flysKilled.append(r.kill_num)

            killed += r.kill_num
            seen += r.see_num
            trees += r.tree_num
            reportNum += 1
        
        if (r.user in user_profile.following.all()):
            leaderboard[r.user] = leaderboard.get(r.user, 0) + r.kill_num
        
        

    leaderboard[request.user] = killed


    leaderboardList = []
    for key, value in leaderboard.items():
        leaderboardList.append((key, value))

    # leaderboardList = leaderboard.items()
    print("leaderboard", leaderboardList)


    sortedLeaderList = sorted(leaderboardList,  key = lambda x: x[1], reverse=True)
    
    report = dumps(users_report, cls=DjangoJSONEncoder)
    reporting_flys = dumps(flysKilled, cls=DjangoJSONEncoder)
    

    context['reports'] = report
    context['reporting_flys'] = reporting_flys

    context['first_name'] = request.user.first_name

    context['killNum'] = killed
    context['seeNum'] = seen
    context['treeNum'] = trees
    context['reportNum'] = reportNum

    context['leaderList'] = sortedLeaderList


    return render(request, 'lanturnfly/heatmap.html', context)


#Following ppl -> copy copy copy heh
@login_required
def other_profile_action(request, id):
    print("inside other_profile_actions")
    if(id == request.user.id):
        # return my_profile_action(request)
        return heatmap(request)
    
    user_profile = get_object_or_404(Profile, id=id)
    loggedin_profile = get_object_or_404(Profile, id=request.user.id)

    context = {}
    users_report = []

    killed = 0
    reportNum = 0
    seen = 0
    trees = 0

    flysKilled = []

    for r in Spotting.objects.all():
        if (r.user.id == id) :
            users_report.append((r.latitude, r.longitude))
            flysKilled.append(r.kill_num)
            killed += r.kill_num
            seen += r.see_num
            trees += r.tree_num
            reportNum += 1

    
    report = dumps(users_report, cls=DjangoJSONEncoder)
    reporting_flys = dumps(flysKilled, cls=DjangoJSONEncoder)
    

    context['reports'] = report
    context['reporting_flys'] = reporting_flys
    context['killNum'] = killed
    context['seeNum'] = seen
    context['treeNum'] = trees
    context['reportNum'] = reportNum
    context['profile'] = user_profile
    context['loggedin_profile'] = loggedin_profile.following.all()
    
    # context = {'profile' : user_profile, 'loggedin_profile' : loggedin_profile.following.all()}
    return render(request, 'lanturnfly/other_profile.html', context)

@login_required
def unfollow(request, id):
    print("inside unfollow button")
    user_to_unfollow = get_object_or_404(Profile, id=id)
    user_profile = Profile.objects.get(id=request.user.id)
    user_profile.following.remove(user_to_unfollow.user)
    user_profile.save()
    return render(request, 'lanturnfly/other_profile.html', {'profile' : user_to_unfollow, "loggedin_profile" : user_profile.following.all()})

@login_required
def follow(request, id):
    print("inside follow button")
    user_to_follow = get_object_or_404(Profile, id=id)
    user_profile = Profile.objects.get(id=request.user.id)
    user_profile.following.add(user_to_follow.user)
    user_profile.save()
    
    print(user_profile.following.all())
    return render(request, 'lanturnfly/other_profile.html', {'profile' : user_to_follow, "loggedin_profile" : user_profile.following.all()})




#Discussion post comment stuff -> copied from hw
@login_required
def global_action(request):
    if request.method == "GET":
        return render(request, 'lanturnfly/global_stream.html', {'posts': Post.objects.all()})
    
    if 'post' not in request.POST or not request.POST['post']:
        context = {'posts': Post.objects.all()}
        context['error'] = 'You must enter an item to add.'
        return render(request, 'lanturnfly/global_stream.html', context)
    
    new_post = Post(text=request.POST['post'], user=request.user, creation_time=timezone.now())
    new_post.save()

    # get_global(request)

    return render(request, 'lanturnfly/global_stream.html', {'posts': Post.objects.all()})


def get_global(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    
    response_data = []
    # posts_data = []
    for post in Post.objects.all():
        comments_data = []
        for comment in Comment.objects.all():
            if comment.posts.id == post.id:
                the_comment = {
                'id': comment.id,
                'post_id': comment.posts.id, #again, idk if this is right ha... 
                'user_id': comment.user.id,
                'user_first_name': comment.user.first_name,
                'user_last_name': comment.user.last_name,
                'text': comment.text,
                'creation_time': comment.creation_time.isoformat(),
                }
                comments_data.append(the_comment)
        
        # print(comments_data)
        the_post = {
            'id': post.id,
            'user_id': post.user.id,
            'user_first_name': post.user.first_name,
            'user_last_name': post.user.last_name,
            'text': post.text,
            'creation_time': post.creation_time.isoformat(),
            'comments' : comments_data,
        }
        response_data.append(the_post)
    
    # print(response_data)


    response_json = json.dumps(response_data)

    return HttpResponse(response_json, content_type='application/json')

    
def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)


def add_comment(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter an comment to add.", status=400)
    
    if not 'post_id' in request.POST or not request.POST['post_id']: #or not isinstance(request.POST['post_id'], int)
        return _my_json_error_response("Must have post to comment under", status=400)
    
    num_posts = []
    for post in Post.objects.all():
        num_posts.append(post)

    # print((request.POST['post_id']).isdigit())
    
    if not request.POST['post_id'].isdigit() or not (1 <= int(request.POST['post_id']) <= len(num_posts)):
        return _my_json_error_response("Not valid post_id", status=400)



    associated_post = get_object_or_404(Post, id=request.POST['post_id'])

    new_comment = Comment(text=request.POST['comment_text'], user=request.user, 
                          creation_time=timezone.now(), posts=associated_post)
    new_comment.save()

    
    return get_new_comments(request, new_comment)

 

def get_new_comments(request, new_comment):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    
    response_data = []
    for post in Post.objects.all():
        if post.id == new_comment.posts.id:                    #only looks at the post in which the new_comment is in. 
            comments_data = []
            for comment in Comment.objects.all():
                if comment.posts.id == post.id:
                    the_comment = {
                    'id': comment.id,
                    'post_id': comment.posts.id, #again, idk if this is right ha... 
                    'user_id': comment.user.id,
                    'user_first_name': comment.user.first_name,
                    'user_last_name': comment.user.last_name,
                    'text': comment.text,
                    'creation_time': comment.creation_time.isoformat(),
                    }
                    comments_data.append(the_comment)
            
            # print(comments_data)

            the_post = {
                'id': post.id,
                'user_id': post.user.id,
                'user_first_name': post.user.first_name,
                'user_last_name': post.user.last_name,
                'text': post.text,
                'creation_time': post.creation_time.isoformat(),
                'comments' : comments_data,
            }
            response_data.append(the_post)

    response_json = json.dumps(response_data)
    # print("response_json", response_json)

    return HttpResponse(response_json, content_type='application/json')