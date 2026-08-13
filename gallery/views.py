from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib import messages
from .forms import PostForm
from django.db.models import Q


def product_list(request):
    query = request.GET.get('q')

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'myapp/index.html', {
        'posts': posts,
        'query': query
    })


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'myapp/detail.html', {'post': post})


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Post created successfully!")
            return redirect("product_list")
    else:
        form = PostForm()

    return render(request, "myapp/create.html", {"form": form})


def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        messages.success(request, "Post updated successfully!")
        return redirect('post_detail', id=post.id)

    return render(request, 'myapp/edit.html', {'form': form})


def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('product_list')

    return render(request, 'myapp/delete.html', {'post': post})