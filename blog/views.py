from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Post,Comment
from users.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect
import xlwt
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
@staff_member_required
def export_post_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="post.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Post')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['author','title','content',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Post.objects.all().values_list('author','title','content')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def like(request,pk,*args, **kwargs):
        post = Post.objects.get(id=pk)
        post.likes=(post.likes)+1
        post.save()
        context = {
        'posts': Post.objects.all()
        }
        return redirect('blog-home')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by=5
    


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by=5
     
    def get_queryset(self):
        user=get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostCommentListView(ListView):
    model = Comment
    template_name = 'blog/post_comments.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'comments'
    def get_queryset(self):
        id1=get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(post_id=id1)
    

class PostDetailView(DetailView):
    model = Post


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk'] 
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
 
    def form_valid(self, form):
        form.instance.author = self.request.user
        profiles=Profile.objects.all()
        for profile in profiles:
              for following in profile.following.all():
                 if following.username==self.request.user.username:
                  send_mail(
                           'Chatter',
                           'New Post!!',
                           'f20212694@pilani.bits-pilani.ac.in',
                           [following.email],
                           fail_silently=False
                            )

        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

         


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@staff_member_required
def Import_csv(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
          
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_excel("."+excel_file)
            print(empexceldata)
            print(type(empexceldata))
            
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                print(dbframe)
                obj = Post.objects.create(author=request.user,title=dbframe.title, content=dbframe.content)
                print(type(obj))
                obj.save()
 
            return render(request, 'blog/Importexcel.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)
     
    return render(request, 'blog/Importexcel.html',{})