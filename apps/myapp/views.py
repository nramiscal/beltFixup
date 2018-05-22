from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(req):
    # User.objects.all().delete()
    # Trip.objects.all().delete()
    return render(req, 'myapp/index.html')


def register(req):

    result = User.objects.regValidator(req.POST)
    print(result)

    if result[0]:
        req.session['id'] = result[1].id
        req.session['name'] = result[1].name
        return redirect('/my_page')
    else:
        for error in result[1]:
            messages.add_message(req, messages.ERROR, error, extra_tags='register')
        return redirect('/')

def login(req):

    result = User.objects.loginValidator(req.POST)
    print(result)

    if result[0]:
        req.session['id'] = result[1].id
        req.session['name'] = result[1].name
        return redirect('/my_page')
    else:
        for error in result[1]:
            messages.add_message(req, messages.ERROR, error, extra_tags='login')
        return redirect('/')

def logout(req):
    req.session.clear()
    return redirect('/')


def add_trip(req):
    return render(req, 'myapp/add_trip.html')

def create_trip(req):
    result = Trip.objects.tripValidator(req.POST, req.session['id'])
    # print(result)
    if result[0]:
        return redirect('/my_page')
    else:
        for error in result[1]:
            messages.add_message(req, messages.ERROR, error)
        return redirect('/add_trip')



def my_page(req):

    my_trips = User.objects.get(id=req.session['id']).joins.all()
    others_trips = Trip.objects.exclude(joiners = req.session['id'])


    context = {
        'my_trips' : my_trips,
        'others_trips' : others_trips
    }
    return render(req, 'myapp/my_page.html', context)



def join(req, trip_id):
    user = User.objects.get(id=req.session['id'])
    trip = Trip.objects.get(id=trip_id)

    user.joins.add(trip)
    return redirect('/my_page')




def show_trip(req, trip_id):
    trip = Trip.objects.get(id=trip_id)
    # other users joining this trip (except planner!)
    other_users = trip.joiners.exclude(id=trip.planner_id)

    context = {
        'trip' : trip,
        'other_users' : other_users
    }
    return render(req, 'myapp/show_trip.html', context)
