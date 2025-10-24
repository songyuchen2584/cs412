# File: mini_insta/models.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: Models for the mini_insta app. 
from datetime import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ''' Encapsulates the data of a mini_insta Profile.'''

    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(max_length=500, blank=True)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.username} ({self.display_name})"
    
    def get_absolute_url(self):
        '''return a string representation of the url'''

        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_all_posts(self):
        '''Return the query-set of posts for this profile.'''

        posts = Post.objects.filter(profile = self)
        return posts
    
    def get_followers(self):
        ''' Returns the query set of the profiles that are following this profile.'''

        follows = Follow.objects.filter(profile = self)
        followers = []
        for follow in follows:
            followers.append(follow.follower_profile)
        return followers

    def get_num_followers(self):
        '''Returns the count of profiles following this profile.'''
        
        num_followers = Follow.objects.filter(profile = self).count()
        return num_followers
    
    def get_following(self):
        ''' Returns the query set of the profiles that this profile is following.'''

        follows = Follow.objects.filter(follower_profile = self)
        following = []
        for follow in follows:
            following.append(follow.profile)
        return following

    def get_num_following(self):
        '''Returns the count of profiles this profile is following'''
        
        num_followers = Follow.objects.filter(follower_profile = self).count()
        return num_followers
    
    def get_post_feed(self):
        '''
        Return a queryset of Posts from all profiles this user follows,
        plus this user's own posts, ordered by most recent first.
        '''
        # get all profiles this profile follows
        followed_profiles = self.get_following()

        # include this profile itself
        profiles_to_include = list(followed_profiles) + [self]

        # filter Posts where the post.profile is one of these profiles
        return Post.objects.filter(profile__in=profiles_to_include).order_by('-timestamp')
    
    def get_liked_posts(self):
        """Return a queryset of Posts this profile has liked."""
        return Post.objects.filter(like__profile=self)

    class Meta:
        ordering = ['-join_date']

class Post(models.Model):
    ''' Encapsulates the data of a post.'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(max_length= 1000, blank=True)

    def __str__(self):
        ''' Return a string representation of this post'''
        return f"{self.caption}"
    
    def get_all_photos(self):
        '''Return the query-set of photos for this post.'''

        photos = Photo.objects.filter(post = self)
        return photos
    
    def get_all_comments(self):
        '''Return all comments associated with this post.'''

        return Comment.objects.filter(post=self)

    def get_likes(self):
        '''Return all likes associated with this post.'''

        return Like.objects.filter(post=self)

    def get_num_likes(self):
        '''Return the count of likes on this post.'''

        return Like.objects.filter(post=self).count()

    class Meta:
        ordering = ['-timestamp']


class Photo(models.Model):
    ''' Encapsulates the data of a photo for a post'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' Return a string representation of the URL of the photo'''

        return f"{self.get_image_url()}"       

    def get_image_url(self):
        ''' Returns the image_url if it exists, or else the image_file.url'''

        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url

    class Meta:
        ordering = ['-timestamp']

class Follow(models.Model):
    ''' Encapsulates the data of a follow relationship.'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Returns the string representation of the follow relationship'''

        return f"{self.follower_profile} is following {self.profile}"
    
    class Meta:
        ordering = ['-timestamp']

class Comment(models.Model):
    '''Encapsulates a comment made by a profile on a post.'''

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        '''Return a readable string for this comment.'''

        return f"{self.profile.display_name} commented on '{self.post.caption[:30]}': {self.text[:30]}"

    class Meta:
        ordering = ['-timestamp']


class Like(models.Model):
    '''Encapsulates a 'like' given by a profile on a post.'''

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a readable string for this like.'''

        return f"{self.profile.display_name} liked '{self.post.caption[:30]}'"

    class Meta:
        ordering = ['-timestamp']
