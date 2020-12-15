from django.shortcuts import render, redirect
from .models import Contact, Post, User, Comment
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from django.views.generic.list import ListView


# Create your views here.
def home(request):
	if 'user' in request.session:
		suggest_users = User.objects.all()
		current_user = request.session['user']
		session_user_obj = User.objects.get(username=current_user)
		fuser = Followers.objects.get(user=session_user_obj)
		following_users = fuser.another_user.all()
		user_posts = []
		for u in following_users:
			all_posts = u.post_set.all()
			for p in all_posts:
				user_posts.append(p)

		param = {'current_user': current_user, 'user_posts': user_posts,'sugg_users' :suggest_users}
		return render(request, 'blogs.html', param)
	else:
		feature_post = 	Post.objects.all().order_by('-id')[:3]
		param = {'feature_post': feature_post}
		return render(request, 'home.html', param)






def view_post(request, post_title):
	get_post = Post.objects.get(title=post_title)
	all_rel_posts = Post.objects.filter(user__username=get_post.user)
	post_comments = get_post.comment_set.all().order_by('-id')
	liked = False
	try:
		if get_post.likes.filter(username=request.session['user']).exists():
			liked = True
	except:
		return redirect('home')

	param = {'post_data': get_post, 'all_posts':all_rel_posts,'post_comments':post_comments, 'liked':liked}
	return render(request, 'post.html', param)



def like_post(request, post_title):
	user = User.objects.get(username=request.session['user'])
	post = Post.objects.get(title=post_title)
	liked = False
	if post.likes.filter(username=request.session['user']).exists():
		post.likes.remove(user)	
		liked = False
	else:
		post.likes.add(user)
		liked = True
	return HttpResponseRedirect(reverse('view_post', args=[str(post_title)]))


def delete_post(request, post_title):
	get_post = Post.objects.get(title=post_title)
	get_post.delete()
	messages.success(request, 'Post has been deleted succsfully.')
	return redirect(f'/profile/{get_post.user.first_name}')



def view_profile(request, user_name):
	try:
		user_obj = User.objects.get(username=user_name)
	except ObjectDoesNotExist:
		return HttpResponse('User does not exists.')
	session_user = User.objects.get(username=request.session['user'])
	session_following, create = Followers.objects.get_or_create(user=session_user)
	user_following, create = Followers.objects.get_or_create(user=user_obj)
	check_user_followers = Followers.objects.filter(another_user=user_obj)
	is_followed = False
	if session_following.another_user.filter(username=user_name).exists():
		is_followed=True
	else:
		is_followed=False

	user_posts = user_obj.post_set.all().order_by('-id')
	lis = []
	for post in user_posts:
		lis.append(post.likes.count())
	total_post_likes = sum(lis)
	param = {'user_posts': user_posts, 'user_data': user_obj, 'total_post_likes': total_post_likes, 'followers':check_user_followers,'session_following':session_following, 'user_following': user_following,'is_followed':is_followed}
	try:
		return render(request, 'profile.html', param)
	except:
		messages.warning(request, f"You have to login before access {user}'s profile.")
		return redirect('home')




def follow_user(request, user_name):
	if request.method == 'POST':
		other_user = User.objects.get(username=user_name)
		session_user = request.session['user']
		get_user = User.objects.get(username=session_user)
		check_follower = Followers.objects.get(user=get_user)
		is_followed = False

		if check_follower.another_user.filter(username=user_name).exists():
			check_follower.another_user.remove(other_user)
			is_followed = False
			return redirect(f'/profile/{user_name}')
		else:
			check_follower.another_user.add(other_user)
			is_followed = True
			return redirect(f'/profile/{user_name}')

	else:
		return redirect(f'/profile/{user_name}')





def update_profile(request, current_user):
	if request.method == 'POST':
		get_user = User.objects.get(username=current_user)

		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		mail = request.POST.get('mail')
		bio = request.POST.get('bio')
		
		
		get_user.first_name = fname
		get_user.last_name = lname
		get_user.email = mail
		get_user.bio = bio
		get_user.save()
		return redirect(f'/profile/{current_user}')
	else:
		return redirect('profile')


def change_image(request, user):
	get_user = User.objects.get(username=user)
	new_pic = request.FILES['image']

	get_user.profile_pic = new_pic
	get_user.save()
	messages.success(request, 'Profile Picture updated succsfully.')
	return redirect(f'/profile/{get_user.username}')


def settings(request, user):
	get_user = User.objects.get(username=user)


	if request.method == 'POST':
		pwd1 = request.POST['pwd1']
		pwd2 = request.POST['pwd2']
		email = request.POST['mail']


		if (pwd1 and pwd2) and not email:
			if pwd1==pwd2:
				get_user.password = pwd1
				get_user.save()
				messages.success(request, 'Password saved succesfully.')
			else:
				messages.warning(request, 'Password are not same.')
		elif email and not (pwd1 and pwd2):
			get_user.email = email
			get_user.save()
			messages.success(request, 'Email saved succesfully.')
		elif (pwd1 and pwd2) and email:
			if pwd1==pwd2:
				get_user.password = pwd1
				get_user.email = email
				get_user.save()
				messages.success(request, 'Password and Email saved succesfully.')
			else:
				messages.warning(request, 'Password are not same.')
		
	param = {'user_data': get_user}
	return render(request, 'profile_setting.html', param)



def delete_user(request, user):
	if request.method == 'POST':
		get_user = User.objects.get(username=user)

		first_name = request.POST.get('username')
		if first_name == get_user.first_name:
			get_user.delete()
			del request.session['user']
			return redirect('home')

	return HttpResponseRedirect(reverse('settings', args=[str(user)]))









class WritePostView(ListView):
	model = Post
	template_name = 'main/create_post.html'
	def get(self, request):
		form = WritePostForm()
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = WritePostForm(request.POST)
		if form.is_valid():
			user_obj = User.objects.get(username=request.session['user'])
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			add_post = self.model.objects.create(user=user_obj, title=title, content=content)
			add_post.save()
			form = WritePostForm()
			messages.success(request,'Post has been uploaded succsfully.')
			return render(request, self.template_name, {'form':form})

	

def search(request):
	query = request.GET.get('query')
	search_user = User.objects.filter(username=query)
	search_user_posts = Post.objects.filter(user__username__icontains=query)
	search_title = Post.objects.filter(title__icontains=query)
	search_content = Post.objects.filter(content__icontains=query)
	search_result = search_title.union(search_content,search_user_posts)
	
	param = {'search_result': search_result, 'search_term':query,'search_user':search_user}
	return render(request, 'search.html', param)



def signup(request):
	if request.method == 'POST':
		fname = request.POST.get('first_name')
		lname = request.POST.get('last_name')
		mail = request.POST.get('mail')
		userName = request.POST.get('username')
		pwd = request.POST.get('pwd')
		bio = request.POST.get('bio')

		check_username = User.objects.filter(username=userName)
		check_email = User.objects.filter(email=mail)
		if not check_username:
			create_user = User(first_name=fname, last_name=lname, email=mail,username=userName, password=pwd, bio=bio)
			create_user.save()
			messages.success(request, 'Your account has been created succsfully.')
			return redirect('home')
		else:
			messages.warning(request, 'This Username is already exists.')
			return redirect('home')
			

	else:
		return redirect('home')



def login(request):
	if request.method == 'POST':
		userName = request.POST.get('username')
		pwd = request.POST.get('pwd')

		check_user = User.objects.get(username=userName, password=pwd)
		if check_user:
			request.session['user'] = check_user.username
			return redirect('home')
		else:
			messages.warning(request, 'Invalid User')
			return redirect('home')
	else:
		return redirect('home')



def logout(request):
	try:
		del request.session['user']
		del request.session['email']
	except:
		return redirect('login')
	return redirect('login')









def contact(request):
	if request.method == 'POST':
		full_name = request.POST.get('full_name')
		mail = request.POST.get('mail')
		msg = request.POST.get('msg')

		
		create_contact = Contact(name=full_name, email=mail, message=msg)
		create_contact.save()
		messages.success(request, 'Your form has been submitted.')
		return redirect("contact")

	else:
		return render(request, 'contact.html')




#Create Comments
def add_comment(request, post_title):
    name = request.session['user']
    comment = request.POST.get('comment')
    post = Post.objects.get(title=post_title)
    if name!="" and comment!="":
        create_comment = Comment(post=post, name=name, comment=comment)
        create_comment.save()
        return HttpResponseRedirect(reverse('view_post', args=[str(post_title)]))
