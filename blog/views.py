from bson import ObjectId
from django.shortcuts import render, redirect
from django.utils import timezone

from .db import get_collection


def _serialize_blog(doc):
    if not doc:
        return None
    return {
        'id': str(doc.get('_id')),
        'title': doc.get('title', ''),
        'content': doc.get('content', ''),
        'created_at': doc.get('created_at'),
        'updated_at': doc.get('updated_at'),
    }


def home(request):
    if request.method == 'GET':
        cursor = get_collection('blogs').find().sort('created_at', -1)
        data = [_serialize_blog(doc) for doc in cursor]
        if data:
            return render(request, 'home.html', {'data': data})

    return render(request, 'home.html')


def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            now = timezone.now()
            get_collection('blogs').insert_one({
                'title': title,
                'content': content,
                'created_at': now,
                'updated_at': now,
            })
            return render(request, 'add.html', {'message': 'Blog added successfully!'})
    return render(request, 'add.html')


def _get_blog_or_none(blog_id: str):
    try:
        oid = ObjectId(blog_id)
    except Exception:
        return None
    doc = get_collection('blogs').find_one({'_id': oid})
    return _serialize_blog(doc)


def view_blog(request, blog_id):
    blog_post = _get_blog_or_none(blog_id)
    if blog_post:
        return render(request, 'details.html', {'blog': blog_post})
    return render(request, 'details.html', {'error': 'Blog not found.'})


def delete_blog(request, blog_id):
    blog_post = _get_blog_or_none(blog_id)
    if not blog_post:
        return render(request, 'delete.html', {'error': 'Blog not found.'})

    if request.method == 'POST':
        get_collection('blogs').delete_one({'_id': ObjectId(blog_id)})
        return render(request, 'delete.html', {'message': 'Blog deleted successfully!'})

    return render(request, 'delete.html')


def edit_blog(request, blog_id):
    blog_post = _get_blog_or_none(blog_id)
    if not blog_post:
        return render(request, 'edit.html', {'error': 'Blog not found.'})

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            get_collection('blogs').update_one(
                {'_id': ObjectId(blog_id)},
                {'$set': {'title': title, 'content': content, 'updated_at': timezone.now()}},
            )
            blog_post['title'] = title
            blog_post['content'] = content
            blog_post['updated_at'] = timezone.now()
            return render(request, 'edit.html', {'blog': blog_post, 'message': 'Blog updated successfully!'})

    return render(request, 'edit.html', {'blog': blog_post})


def show_blogs(request):
    cursor = get_collection('blogs').find().sort('created_at', -1)
    data = [_serialize_blog(doc) for doc in cursor]
    return render(request, 'homeuser.html', {'data': data})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and email and password:
            existing_user = get_collection('users').find_one({'$or': [{'username': username}, {'email': email}]})
            if existing_user:
                return render(request, 'signup.html', {'error': 'Username or email already exists.'})
            get_collection('users').insert_one({
                'username': username,
                'email': email,
                'password': password,
                'created_at': timezone.now(),
            })
            return render(request, 'signup.html', {'message': 'User registered successfully!'})
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = get_collection('users').find_one({'username': username, 'password': password})
            if user:
                request.session['user_id'] = str(user.get('_id'))
                request.session['username'] = user.get('username')
                next_url = request.GET.get('next') or 'show_blogs'
                return redirect(next_url)
            else:
                return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('login')