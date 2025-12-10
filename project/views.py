from datetime import date
from django.shortcuts import redirect, render
from .models import *
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateAccountForm, CreateBidForm, CreateProductForm, RateProductForm, UpdateAccountForm, UpdateProductForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Max
from django.db import transaction
from django.db.models import Q


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add sold products for this account
        context["sold_products"] = (
            Product.objects
            .filter(profile=self.object, status="sold")
            .prefetch_related("images")
            .annotate(highest_bid=Max("bid__bid_price"))
        )

        return context

class ProductListView(ListView):
    model = Product
    template_name = "project/show_products.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.filter(status="available")

        query = self.request.GET.get('query')
        category = self.request.GET.get('category')

        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

        if category:
            qs = qs.filter(category__icontains=category)
        
        qs = qs.annotate(highest_bid=Max("bid__bid_price"))

        return qs


class ProductDetailView(DetailView):
    model = Product
    template_name = "project/show_product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        bids = Bid.objects.filter(product=product)
        context['bids'] = bids

        context['highest_bid'] = bids.aggregate(Max("bid_price"))["bid_price__max"]

        if self.request.user.is_authenticated:
            profile = Account.objects.filter(user=self.request.user).first()
            is_seller = (profile == product.profile)
            context["is_seller"] = is_seller

            if is_seller:
                context["bids"] = (
                    Bid.objects
                    .filter(product=product)
                    .select_related("profile")
                    .order_by("-bid_price")
                )
            context['is_favorited'] = Favorite.objects.filter(
                profile=profile, product=product
            ).exists()
        else:
            context['is_favorited'] = False
            context["is_seller"] = False

        return context

# Views requiring account 
class ProjectLoginRequiredMixin(LoginRequiredMixin):
    """Require login and provide helper to get logged-in user's Account."""

    login_url = 'login'  # redirect here if not authenticated
    redirect_field_name = 'next'

    def get_logged_in_profile(self):
        """Return the Profile for the logged-in user."""

        return get_object_or_404(Account, user=self.request.user)


#----------------Account Views------------------------#
class CreateAccountView(CreateView):
    ''' View for managing the creation of a new account and user'''

    template_name = "project/create_account_form.html"
    form_class = CreateAccountForm
    model = Account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # If user_form is passed (e.g., from post), keep it; otherwise create a new one
        if 'user_form' in context:
            # already present via kwargs passed to get_context_data
            pass
        else:
            context['user_form'] = kwargs.get('user_form', UserCreationForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        account_form = self.get_form()
        user_form = UserCreationForm(request.POST)

        if account_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            self.object = account
            return redirect(self.get_success_url())

        # Re-render with bound forms and errors
        context = self.get_context_data(form=account_form, user_form=user_form)
        return self.render_to_response(context)
        
    def get_success_url(self):
        ''' After creating Account, got to Account detail page'''

        return reverse('show_account', kwargs={'pk': self.object.pk})

class LogoutConfirmationView(TemplateView):
    ''' A view for redirecting to the logout confirmation page.'''

    template_name = 'project/logged_out.html'

class UpdateAccountView(ProjectLoginRequiredMixin, UpdateView):
    '''The view class to handle profile updates based on its PK'''

    model = Account
    form_class = UpdateAccountForm
    template_name = "project/update_profile_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Account, user=self.request.user)

class DeleteAccountView(ProjectLoginRequiredMixin, DeleteView):
    model = Account
    template_name = "project/delete_account.html"

    def get_object(self):
        return get_object_or_404(Account, user=self.request.user)

    def get_success_url(self):
        return reverse('show_accounts')

class MyAccountDetailView(ProjectLoginRequiredMixin, DetailView):
    """Show the logged-in user's own account at /project/my_account/"""

    model = Account
    template_name = "project/show_account.html"
    context_object_name = "account"

    def get_object(self):
        return self.get_logged_in_profile()

    def get_context_data(self, **kwargs):
        """Add context to indicate this is the user's own account."""
        
        context = super().get_context_data(**kwargs)
        account = self.get_object()
        user = self.request.user
        profile = self.get_object()

        # Since this is always the logged-in user:
        context['is_own_account'] = True
        context["sold_products"] = (
            Product.objects
            .filter(profile=profile, status="sold")
            .prefetch_related("images")
            .annotate(highest_bid=Max("bid__bid_price"))
        )

        return context

class MyProductsListView(ProjectLoginRequiredMixin, ListView):
    template_name = "project/dashboard_list.html"
    context_object_name = "items"

    def get_queryset(self):
        profile = self.get_logged_in_profile()
        return (
            Product.objects
            .filter(profile=profile)
            .prefetch_related("bid_set", "bid_set__profile")
            .annotate(highest_bid=Max("bid__bid_price"))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Products"
        context["mode"] = "products"
        return context


class MyFavoritesListView(ProjectLoginRequiredMixin, ListView):
    template_name = "project/dashboard_list.html"
    context_object_name = "items"

    def get_queryset(self):
        profile = self.get_logged_in_profile()
        return (
            Favorite.objects
            .filter(profile=profile)
            .select_related("product")
            .annotate(highest_bid=Max("product__bid__bid_price"))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Favorites"
        context["mode"] = "favorites"
        return context

class MyBidsListView(ProjectLoginRequiredMixin, ListView):
    """Show all bids made by the logged-in user."""

    model = Bid
    template_name = "project/my_bids.html"
    context_object_name = "bids"

    def get_queryset(self):
        profile = self.get_logged_in_profile()
        return (
            Bid.objects
            .filter(profile=profile)
            .select_related('product')
            .annotate(highest_bid=Max('product__bid__bid_price'))
        )

class MyOrdersListView(ProjectLoginRequiredMixin, ListView):
    model = Order
    template_name = "project/my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        profile = self.get_logged_in_profile()
        return Order.objects.filter(profile=profile).prefetch_related("products")


#----------------Product Views------------------------#

class CreateProductView(ProjectLoginRequiredMixin, CreateView):
    form_class = CreateProductForm
    template_name = "project/create_product_form.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.profile = self.get_logged_in_profile()
        product.save()
        self.object = product

        image_files = self.request.FILES.getlist("image_file")
        for img in image_files:
            ProductImage.objects.create(
                product=product,
                image=img
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_product', kwargs={'pk': self.object.pk})


class UpdateProductView(ProjectLoginRequiredMixin, UpdateView):
    model = Product
    form_class = UpdateProductForm
    template_name = "project/update_product_form.html"

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        #  Do not allow editing sold items
        if product.status == "sold":
            return redirect("show_product", pk=product.pk)
        # Check to make sure seller is the only one that can edit
        if product.profile != self.get_logged_in_profile():
            return redirect("show_product", pk=product.pk)

        return super().dispatch(request, *args, **kwargs)

    
    def form_valid(self, form):
        response = super().form_valid(form)

        remove_ids = self.request.POST.getlist("remove_images")
        if remove_ids:
            ProductImage.objects.filter(
                id__in=remove_ids,
                product=self.object
            ).delete()

        for img in self.request.FILES.getlist("image_file"):
            ProductImage.objects.create(product=self.object, image=img)

        return response

    def get_success_url(self):
        return reverse('show_product', kwargs={'pk': self.object.pk})


class DeleteProductView(ProjectLoginRequiredMixin, DeleteView):
    model = Product
    template_name = "project/delete_product.html"

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        # Do not allow deleting sold items
        if product.status == "sold":
            return redirect("show_product", pk=product.pk)
        # Check if the seller is the one trying to delete
        if product.profile != self.get_logged_in_profile():
            return redirect("show_product", pk=product.pk)

        return super().dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return reverse('show_products')

#----------------Favorite Views------------------------#

class CreateFavoriteView(ProjectLoginRequiredMixin, CreateView):
    model = Favorite
    fields = []  # do not allow user input
    template_name = "project/create_favorite.html"

    def form_valid(self, form):
        form.instance.profile = self.get_logged_in_profile()
        form.instance.product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_product', kwargs={'pk': self.object.product.pk})

class DeleteFavoriteView(ProjectLoginRequiredMixin, DeleteView):
    model = Favorite
    template_name = "project/delete_favorite.html"

    def get_object(self):
        profile = self.get_logged_in_profile()
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return get_object_or_404(Favorite, profile=profile, product=product)

    def get_success_url(self):
        return reverse('show_product', kwargs={'pk': self.kwargs['pk']})



#----------------Bid Views------------------------#

class CreateBidView(ProjectLoginRequiredMixin, CreateView):
    form_class = CreateBidForm
    template_name = "project/create_bid_form.html"

    def dispatch(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])

        # Block new bids if deal is set, prevent user from wrapping around through http
        if product.status != "available":
            return redirect("show_product", pk=product.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        bid = form.save(commit=False)
        bid.profile = self.get_logged_in_profile()
        bid.product = get_object_or_404(Product, pk=self.kwargs['pk'])
        bid.save()
        self.object = bid
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_product', kwargs={'pk': self.object.product.pk})


class AcceptBidView(ProjectLoginRequiredMixin, TemplateView):

    def dispatch(self, request, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=self.kwargs['pk'])
        seller_profile = self.get_logged_in_profile()
        product = bid.product

        #  Only the seller can accept
        if product.profile != seller_profile:
            return redirect("show_product", pk=product.pk)

        # BLOCK if a bid was already accepted
        already_accepted = Bid.objects.filter(
            product=product,
            status="accepted"
        ).exists()

        if already_accepted:
            # Do nothing if one is already accepted
            return redirect("show_product", pk=product.pk)

        #  Accept bid
        bid.status = "accepted"
        bid.save()

        #  Auto-reject all other bids
        Bid.objects.filter(
            product=product
        ).exclude(pk=bid.pk).update(status="rejected")

        return redirect("show_product", pk=product.pk)
    

###----------------order abd rating----------------------###

class CheckoutAcceptedBidsView(ProjectLoginRequiredMixin, TemplateView):
    template_name = "project/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_logged_in_profile()

        accepted_bids = Bid.objects.filter(
            profile=profile,
            status="accepted",
            product__status="available"
        ).select_related("product")

        context["accepted_bids"] = accepted_bids
        context["total"] = sum(b.bid_price for b in accepted_bids)

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        profile = self.get_logged_in_profile()

        selected_ids = request.POST.getlist("selected_bids")

        if not selected_ids:
            return redirect("checkout")  # nothing selected

        selected_bids = Bid.objects.filter(
            pk__in=selected_ids,
            profile=profile,
            status="accepted",
            product__status="available"
        ).select_related("product")

        if not selected_bids.exists():
            return redirect("my_bids")

        total = sum(b.bid_price for b in selected_bids)

        order = Order.objects.create(
            profile=profile,
            date=date.today(),
            total=total
        )

        for bid in selected_bids:
            order.products.add(bid.product)

            # Mark product sold
            bid.product.status = "sold"
            bid.product.save()

        return redirect("my_orders")

class RateProductView(ProjectLoginRequiredMixin, FormView):
    form_class = RateProductForm
    template_name = "project/rate_product.html"

    def dispatch(self, request, *args, **kwargs):
        #  Correctly load product ONCE
        self.product = get_object_or_404(Product, pk=self.kwargs["pk"])
        profile = self.get_logged_in_profile()

        #  Only allow rating if user actually CHECKED OUT the product
        has_order = Order.objects.filter(
            profile=profile,
            products=self.product
        ).exists()

        if not has_order:
            return redirect("show_product", pk=self.product.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        #  Provide product to template
        context = super().get_context_data(**kwargs)
        context["product"] = self.product
        return context

    def form_valid(self, form):
        # Save the rating 
        rating_value = int(form.cleaned_data["rating"])
        self.product.rating = rating_value
        self.product.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect using self.product (NOT self.object)
        return reverse("show_product", kwargs={"pk": self.product.pk})

