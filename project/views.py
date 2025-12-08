from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateAccountForm
from django.contrib.auth.forms import UserCreationForm, UpdateAccountForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your views here.

# Views without account
class AccountListView(ListView):
    ''' View for showing all accounts'''

    model = Account
    template_name = "project/show_accounts.html"
    context_object_name= "accounts"

class AccountDetailView(DetailView):
    ''' View for showing account detail'''

    model = Account
    template_name = "project/show_account.html"
    context_object_name = "account"


# Views requiring account 
class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    """Require login and provide helper to get logged-in user's Account."""

    login_url = 'login'  # redirect here if not authenticated
    redirect_field_name = 'next'

    def get_logged_in_profile(self):
        """Return the Profile for the logged-in user."""

        return Account.objects.get(user=self.request.user)
    
class CreateAccountView(CreateView):
    ''' View for managing the creation of a new account and user'''

    template_name = "project/create_account_form.html"
    form_class = CreateAccountForm
    model = User

    def get_context_data(self, **kwargs):
        ''' Create user form '''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid (self, form):
        ''' Creates the associated user and automatically login as the user'''

        # Construct the user creation form POST
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # Create and save the user
            user = user_form.save

            # login as the created user
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

            # connect the user to the Account
            form.instance.user = user

            # leave rest to superclass
            return super().form_valid(form)
        else:
            # render the forms with form errors
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
        
    def get_success_url(self):
        ''' After creating Account, got to Account detail page'''

        return reverse('show_account', kwargs={'pk': self.object.pk})

class LogoutConfirmationView(TemplateView):
    ''' A view for redirecting to the logout confirmation page.'''

    template_name = 'mini_insta/logged_out.html'

class UpdateAccountView(MiniInstaLoginRequiredMixin, UpdateView):
    '''The view class to handle profile updates based on its PK'''

    model = Account
    form_class = UpdateAccountForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Account, user=self.request.user)
