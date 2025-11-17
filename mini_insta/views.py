# File: mini_insta/views.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: Views for the mini_insta app. 
import random
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Follow, Like, Photo, Profile,Post
from .forms import CreatePostForm, CreateProfileForm, UpdatePostForm, UpdateProfileForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    """Require login and provide helper to get logged-in user's Profile."""

    login_url = 'login'  # redirect here if not authenticated
    redirect_field_name = 'next'

    def get_logged_in_profile(self):
        """Return the Profile for the logged-in user."""

        return Profile.objects.get(user=self.request.user)

# Create your views here.

# -------------------------------------------------------------
#  Views that anyone can access
# -------------------------------------------------------------
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

    def get_context_data(self, **kwargs):
        ''' Adds content data to ensure follow/unfollow status and prevent user from following self.'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            user_profile = Profile.objects.filter(user=user).first()
            
            # Add flag to check if viewing own profile
            context['is_own_profile'] = (user_profile == profile)
            
            # Check if logged-in user is following this profile
            if user_profile and user_profile != profile:
                context['is_following'] = Follow.objects.filter(
                    profile=profile, follower_profile=user_profile
                ).exists()
            else:
                context['is_following'] = False
        else:
            context['is_following'] = False
            context['is_own_profile'] = False
        return context

class PostDetailView(DetailView):
    '''displays a single post'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ''' Add contenxt data to ensure like/unlike status and disable user from following itself.'''
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            # Safely get the associated Profile
            profile = Profile.objects.filter(user=user).first()
            
            if profile:
                # Check if this is the user's own post
                context['is_own_post'] = (profile == post.profile)
                
                # Check if user has liked this post
                context['user_liked'] = Like.objects.filter(post=post, profile=profile).exists()
            else:
                context['is_own_post'] = False
                context['user_liked'] = False
        else:
            context['is_own_post'] = False
            context['user_liked'] = False

        return context

    
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

class ShowFollowersDetailView(DetailView):
    ''' The view class to handle the display of the followers of a profile.'''

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    ''' The view class to handle the display the profiles followed by a profile'''

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

# -------------------------------------------------------------
#  Views that require login
# -------------------------------------------------------------

class CreatePostView(MiniInstaLoginRequiredMixin, CreateView):
    ''' a view to handle the creation of a new post'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        '''After creating a new Post, go back to the logged-in user's profile page'''
        profile = get_object_or_404(Profile, user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    def get_context_data(self, **kwargs):
        '''Add the logged-in user's profile to the context'''
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context

    def form_valid(self, form):
        '''Handle form submission and save new Post + images'''
        profile = get_object_or_404(Profile, user=self.request.user)

        # Save the Post instance and link it to the user's profile
        post = form.save(commit=False)
        post.profile = profile
        post.save()

        # Handle multiple uploaded images
        files = self.request.FILES.getlist('image_file')
        print('Number of uploaded files:', len(files))

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

class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView):
    '''The view class to handle profile updates based on its PK'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

class DeletePostView(MiniInstaLoginRequiredMixin, DeleteView):
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
    
class UpdatePostView(MiniInstaLoginRequiredMixin, UpdateView):
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

class PostFeedListView(MiniInstaLoginRequiredMixin, ListView):
    '''Displays the feed of posts for a given Profile.'''

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "feed_posts"

    def get_queryset(self):
        ''''Return posts for the feed of the given profile.'''

        profile = Profile.objects.get(user=self.request.user)
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Add the profile to the context.'''

        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
    
class SearchView(MiniInstaLoginRequiredMixin, ListView):
    ''' View for handling the search feature of the mini_insta app.'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'  # default object list name

    def dispatch(self, request, *args, **kwargs):
        '''If there's no query, show the search form.Otherwise, continue normal dispatch (to run get_queryset)'''

        self.profile = self.request.user
        query = self.request.GET.get('query', None)

        if not query:
            return render(request, 'mini_insta/search.html', {'profile': self.profile})
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Obtain Posts that contain the query. Return the QuerySet of matching Posts'''

        query = self.request.GET.get('query', '')
        # Search Posts that contain the query in caption
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')

        # Matching Profiles
        matching_profiles = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )

        context['profile'] = self.profile
        context['query'] = query
        context['matching_profiles'] = matching_profiles
        context['matching_posts'] = self.get_queryset()
        return context
    
class MyProfileDetailView(MiniInstaLoginRequiredMixin, DetailView):
    """Show the logged-in user's own profile at /mini_insta/profile."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return self.get_logged_in_profile()
    
    def get_context_data(self, **kwargs):
        ''' Adds content data to ensure follow/unfollow status and ensure a user cannot follow itself.'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            user_profile = Profile.objects.filter(user=user).first()
            
            # Add flag to check if viewing own profile
            context['is_own_profile'] = (user_profile == profile)
            
            # Check if logged-in user is following this profile
            if user_profile and user_profile != profile:
                context['is_following'] = Follow.objects.filter(
                    profile=profile, follower_profile=user_profile
                ).exists()
            else:
                context['is_following'] = False
        else:
            context['is_following'] = False
            context['is_own_profile'] = False
        return context
    
class LogoutConfirmationView(TemplateView):
    ''' A view for redirecting to the logout confirmation page.'''

    template_name = 'mini_insta/logged_out.html'

class CreateProfileView(CreateView):
    '''A view to process the registratiom form to create a new user.'''

    template_name="mini_insta/create_profile_form.html"
    form_class= CreateProfileForm
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        ''' Creates the user associated with the profile and automatically login as the created user.'''
        # Reconstruct the user creation form from POST data
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # Create and save the User
            user = user_form.save()

            # Log the user in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Attach the User to the Profile instance
            form.instance.user = user

            # Delegate the rest to the superclass
            return super().form_valid(form)
        else:
            # Re-render the form with both form errors
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self):
        ''' After creating profile, go to their profile page'''

        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class FollowProfileView(LoginRequiredMixin, TemplateView):
    '''View to handle the following of a profile.'''

    def dispatch(self, request, *args, **kwargs):
        other_profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        follower_profile = Profile.objects.filter(user=request.user).first()

        # Only allow follow if not self
        if follower_profile and follower_profile != other_profile:
            Follow.objects.get_or_create(profile=other_profile, follower_profile=follower_profile)

        # Redirect back to the profile page
        return redirect(other_profile.get_absolute_url())


class UnfollowProfileView(LoginRequiredMixin, TemplateView):
    '''View to handle the unfollowing of a profile.'''

    def dispatch(self, request, *args, **kwargs):
        other_profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        follower_profile = Profile.objects.filter(user=request.user).first()

        if follower_profile:
            Follow.objects.filter(profile=other_profile, follower_profile=follower_profile).delete()

        return redirect(other_profile.get_absolute_url())


class LikePostView(LoginRequiredMixin, TemplateView):
    ''' View to handle the liking of a post.'''

    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        post = get_object_or_404(Post, pk=kwargs['pk'])

        # prevent liking own post
        if post.profile != profile:
            Like.objects.get_or_create(profile=profile, post=post)

        return redirect(reverse('show_post', kwargs={'pk':post.pk}))


class UnlikePostView(LoginRequiredMixin, TemplateView):
    ''' View to handle the unliking of a post.'''

    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        post = get_object_or_404(Post, pk=kwargs['pk'])

        Like.objects.filter(profile=profile, post=post).delete()
        return redirect(reverse('show_post', kwargs={'pk':post.pk}))
    

#######################################################################################
# enable REST API for app

from rest_framework import generics
from .serializers import *

class PostListAPIView(generics.ListCreateAPIView):
    '''
    This view will expose the API for Articles with List and Create
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, validated_data):
        '''handle object creattion'''

        print(f'PostSerializer.create(), validated_data = {validated_data}.')

        # create an Object
        post = Post.objects.create(user=User.objects.first(),**validated_data)

        # save to db
        post.user = User.objects.first()

        post.save()

        return post

