from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from .models import Photo, Category
from .forms import PhotoForm


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


from django.contrib import messages

from django.views.decorators.http import require_POST

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from . import forms




#ユーザー情報関連
def users_detail(request, pk):
    user =get_object_or_404(User, pk=pk)
    photos = user.photo_set.all().order_by('-created_at')
    return render(request, 'app/users_detail.html', {'user': user, 'photos':photos,})
    

#def mypage(request, pk):
 #  user =get_object_or_404(User, pk=pk)
  #3  photos = user.photo_set.all().order_by('-created_at')
   # return render(request, 'app/mypage.html', {'user': user, 'photos':photos,})

@login_required
def mypage(request):
    user = request.user
    photos = user.photo_set.all().order_by('-created_at')
    return render(request, 'app/mypage.html',
                            {'user': user,
                             'photos':photos,})

@login_required
def mypage_edit(request):
    if request.method == 'POST':
        form = forms.ProfileEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('app:mypage')
    else:
        form = forms.ProfileEditForm(instance=request.user)
    return render(request, 'app/mypage_edit.html',
                            {'form': form})
                            

def index(request):
    photos = Photo.objects.all().order_by('-created_at')
    #return render(request, 'app/index.html', {'photos': photos})
    
    params = request.GET.copy()
    if 'page' in params:
        page = params['page']
        del params['page']
    else:
        page = 1
    search_params = params.urlencode()
    
    paginator = Paginator(photos, 4)
        
    try:
        photos = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        photos = paginator.page(1)
    
    return render(request, 'app/index.html',
                                {'photos': photos,
                                'search_params': search_params,})
                                

def posts_list(request):
    photos = Photo.objects.all().order_by('-created_at')
    #return render(request, 'app/index.html', {'photos': photos})
    
    params = request.GET.copy()
    if 'page' in params:
        page = params['page']
        del params['page']
    else:
        page = 1
    search_params = params.urlencode()
    
    paginator = Paginator(photos, 8)
        
    try:
        photos = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        photos = paginator.page(1)
    
    return render(request, 'app/posts_list.html',
                                {'photos': photos,
                                'search_params': search_params,})
                                
def posts_list_new(request):
    photos = Photo.objects.all().order_by('-created_at')
    #return render(request, 'app/index.html', {'photos': photos})
    
    paginator = Paginator(photos, 3)
        
    
    return render(request, 'app/posts_list.html',
                                {'photos': photos})
                                



                                
def shops_list(request):
    photos = Photo.objects.all().order_by('-created_at')
    #return render(request, 'app/index.html', {'photos': photos})
    
    params = request.GET.copy()
    if 'page' in params:
        page = params['page']
        del params['page']
    else:
        page = 1
    search_params = params.urlencode()
    
    paginator = Paginator(photos, 8)
        
    try:
        photos = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        photos = paginator.page(1)
    
    return render(request, 'app/shops_list.html',
                                {'photos': photos,
                                'search_params': search_params,})
                                
                                

    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) #入力した値からユーザーインスタンスを自動生成
        if form.is_valid():
            new_user = form.save() #ユーザーインスタンスの保存
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            # フォームの入力値で認証できればユーザーオブジェクト、できなければNoneを返す
            new_user = authenticate(username=input_username, password=input_password)
            if new_user is not None:
                # loginメソッドは、認証ができてなくてもログインさせることができる。→上のauthenticateで認証を実行する
                login(request, new_user)
                return redirect('app:users_detail', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form':form})

@login_required
def photos_new(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, "投稿が完了しました！") # 追加                     
        return redirect('app:users_detail', pk=request.user.pk)
    else:   
        form = PhotoForm()
    return render(request, 'app/photos_new.html', {'form': form},)


def photos_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'app/photos_detail.html', {'photo': photo})

    
@require_POST
def photos_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('app:users_detail', request.user.id)
    

def photos_category(request, category):
    # titleがURLの文字列と一致するcategoryインスタンスを取得
    category = Category.objects.get(title=category)
    #取得したcategoryに属するphoto一覧を取得
    photos = Photo.objects.filter(category=category).order_by('-created_at')
    return render(request, 'app/index.html', {'photos':photos, 'category':category})