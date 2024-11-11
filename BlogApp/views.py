from django.shortcuts import render,get_object_or_404
from BlogApp.models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from BlogApp.forms import EmailSendForm
from BlogApp.forms import CommentForm
# Create your views here.
def post_list_view(request):
    post_list=Post.objects.all();
    return render(request,'BlogApp/post_list.html',{"post_list":post_list})

def post_detail_view(request, year,month,day,post):
    post=get_object_or_404(Post,slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day);
    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()
    return render(request, 'BlogApp/post_detail.html',
                  {"post": post, 'form': form, 'comments': comments, 'csubmit': csubmit})

def post_list_view(request):
    post_list=Post.objects.all()
    paginator=Paginator(post_list,1)
    page_number=request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'BlogApp/post_list.html', {"post_list": post_list})

class PostListView(ListView):
    model=Postpaginate_by=3

send_mail('Hello', 'Have a nice Day..!! ....', 'yaraprathima13@gmail.com',['akkiakhila420@gmail.com'])#,'billanasaraiah808@gmail.com','yamapoojitha2002@gmail.com'])

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id, status='published')
    sent=False
    form=EmailSendForm()
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],	post.title)
            message="Read Post At: \n{}\n\n{} 'Comments:\n{}".format(post_url,cd['name'],cd['comments'])
            send_mail(subject, message, 'yaraprathima13@gmail.com', [cd['to']]) #use[] or ()tuple
            sent=True;
    else:
        form=EmailSendForm()
    return render(request,'BlogApp/sharebymail.html', {'post':post,'form':form,'sent':sent})

#bootstarp-sample.html-view
def bs_sample_view(request):
    return render(request,"BlogApp/Sample.html")







