# File: mini_insta/views.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: Views for the mini_insta app. 
import random
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Photo, Profile,Post
from .forms import CreatePostForm, UpdatePostForm, UpdateProfileForm

# Create your views here.
class ProfileListView(ListView):
    ''' A view class to show all blog profiles'''
    
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''displays a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    '''displays a single post'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    
class RandomProfileDetailView(DetailView):
    '''displays a single random profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        ''' return one instance of the profile object at random'''

        all_profiles = Profile.objects.all()
        profile = random.choice(all_profiles)
        return profile


class CreatePostView(CreateView):
    ''' a view to handle the creation of a new post'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        ''' Provide a URL to navigate to after creating a new Comment'''

        # create and return url
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk':pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the profile from URL parameter
        profile_pk = self.kwargs.get('pk')
        context['profile'] = get_object_or_404(Profile, pk=profile_pk)
        return context


    def form_valid(self, form):
        ''' Handles the form submission and saves new objects to the database'''

        pk=self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # Save the Post instance with the profile
        post = form.save(commit=False)  # create a Post object but don't save to DB yet
        post.profile = profile
        post.save()  

        # Get list of uploaded files
        files = self.request.FILES.getlist('image_file')
        print('Number of uploaded files:', len(files))

        # Create Photo for each file
        for file in files:
            Photo.objects.create(post=post, image_file=file)

        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form invalid errors:", form.errors)
        print("FILES received:", self.request.FILES)
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        print("FILES at post:", request.FILES)
        return super().post(request, *args, **kwargs)

class UpdateProfileView(UpdateView):
    '''The view class to handle profile updates based on its PK'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

class DeletePostView(DeleteView):
    '''The view class to handle the deletion of a post'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object is the Post being deleted
        profile = self.object.profile  # get the related profile
        context['profile'] = profile
        return context

    def get_success_url(self):
        '''Return to the profile of the deleted post.'''
        
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = post.profile
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context

    def get_success_url(self):
        # Redirect to the show_post page for this post after update
        return reverse('show_post', kwargs={'pk': self.object.pk})

