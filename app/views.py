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
from django.http import HttpResponseRedirect

from . import forms




from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
from django.urls import reverse_lazy
from .forms import (
    MyPasswordChangeForm
)



class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('app:password_change_done')
    template_name = 'app/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'app/password_change_done.html'



#ユーザー情報関連
def users_detail(request, pk):
    user =get_object_or_404(User, pk=pk)
    photos = user.photo_set.all().filter(pk__gte=40).order_by('-created_at')
    return render(request, 'app/users_detail.html', {'user': user, 'photos':photos,})
    

#def mypage(request, pk):
 #  user =get_object_or_404(User, pk=pk)
  #3  photos = user.photo_set.all().order_by('-created_at')
   # return render(request, 'app/mypage.html', {'user': user, 'photos':photos,})

@login_required
def mypage(request):
    user = request.user
    photos = user.photo_set.all().filter(pk__gte=40).order_by('-created_at')
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
    photos = Photo.objects.all().filter(pk__gte=40).order_by('-created_at')
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
    photos = Photo.objects.all().filter(pk__gte=40).order_by('-created_at')
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

                                
def shops_list(request):
    photos = Photo.objects.all().filter(pk__lt=40).order_by('created_at')
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
    
    return render(request, 'app/shops_list.html',
                                {'photos': photos,
                                'search_params': search_params,})
                                
           

                                
def shops_detail(request):
    photos = Photo.objects.all().filter(pk__gte=40).order_by('-created_at')
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
    
    return render(request, 'app/shops_detail.html',
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
    category = Category.objects.get(title=category)
    photos = Photo.objects.filter(category=category).filter(pk__gte=40).order_by('-created_at')
    return render(request, 'app/shops_detail.html', {'photos':photos, 'category':category})

'''
@login_required
def like(request, *args, **kwargs):
    photo = Photo.objects.get(id=kwargs['photo_id'])
    is_like = Like.objects.filter(user=request.user).filter(photo=photo).count()
    # unlike
    if is_like > 0:
        liking = Like.objects.get(post__id=kwargs['post_id'], user=request.user)
        liking.delete()
        photo.like_num -= 1
        photo.save()
        messages.warning(request, 'いいねを取り消しました')
        return redirect(reverse_lazy('app:photos_detail', kwargs={'photo_id': kwargs['photo_id']}))
    # like
    photo.like_num += 1
    photo.save()
    like = Like()
    like.user = request.user
    like.photo = photo
    like.save()
    messages.success(request, 'いいね！しました')
    return HttpResponseRedirect(reverse_lazy('app:photos_detail', kwargs={'photo_id': kwargs['photo_id']}))
'''