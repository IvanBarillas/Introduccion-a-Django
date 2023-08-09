from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView, DeleteView
from .models import Post
from .forms import PostCreateForm
from django.urls import reverse_lazy


# Create your views here.
class BlogListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()


        context = {
            'posts': posts
        
        }
        return render(request,'blog_list.html', context)
    
class BlogCreateView(View):
    def get(self, request, *args, **kwargs):
        form = PostCreateForm()

        context = {
            'form':form
        
        }
        return render(request,'blog_create.html',context)
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = PostCreateForm(request.POST)
            if form.is_valid():

                #Queremos obtener la informacion de nuestro formulario
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')

                #Creamos el Post
                #p hace referencia al post
                p, created = Post.objects.get_or_create(title=title, content=content) # el primer title y content hacen referencia al objeto Post
                p.save()
                return redirect('blog:home')



            context = {
               
        }
        return render(request,'blog_create.html',context)

#Class para ver los detalles de cada blog    
class BlogDetailView(View):
    def get(self, request,pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        context= {
            'post':post

        }
        return render(request, 'blog_detail.html',context)

class BlogUpdateView(UpdateView):
    model = Post
    fields=['title','content']
    template_name = "blog_update.html"

    #para redirigir 
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('blog:detail', kwargs={'pk':pk})

class BlogDeleteView(DeleteView):
    model = Post
    template_name = "blog_delete.html"
    success_url = reverse_lazy('blog:home')
        
