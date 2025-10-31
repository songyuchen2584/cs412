from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from . models import Voter
from django.db.models import Q, Count
from datetime import datetime
import plotly.graph_objects as go
from plotly.offline import plot

class VoterListView(ListView):
    ''' View to display the Voter information'''

    template_name="voter_analytics/voters.html"
    model = Voter
    context_object_name="voters"

    paginate_by = 100

    def get_queryset(self):
        ''' Filter results based on form parameters '''
        
        queryset = super().get_queryset()
        
        # Get filter parameters from GET request
        party = self.request.GET.get('party')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')
        
        # Apply filters
        if party:
            queryset = queryset.filter(party=party)
        
        if min_birth_year:
            queryset = queryset.filter(DOB__year__gte=int(min_birth_year))
        
        if max_birth_year:
            queryset = queryset.filter(DOB__year__lte=int(max_birth_year))
        
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        
        # Filter by election participation (checkbox is checked)
        if v20state:
            queryset = queryset.filter(v20state='TRUE')
        
        if v21town:
            queryset = queryset.filter(v21town='TRUE')
        
        if v21primary:
            queryset = queryset.filter(v21primary='TRUE')
        
        if v22general:
            queryset = queryset.filter(v22general='TRUE')
        
        if v23town:
            queryset = queryset.filter(v23town='TRUE')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        ''' Add additional context for the filter form '''
        
        context = super().get_context_data(**kwargs)
        
        # Get unique party affiliations
        parties = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['parties'] = parties
        
        # Generate year ranges for birth dates
        context['years'] = range(1920, 2010)
        
        # Voter scores (typically 0-5)
        context['voter_scores'] = range(0, 6)
        
        # Preserve filter parameters in context
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_year'] = self.request.GET.get('min_birth_year', '')
        context['selected_max_year'] = self.request.GET.get('max_birth_year', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['checked_v20state'] = self.request.GET.get('v20state', '')
        context['checked_v21town'] = self.request.GET.get('v21town', '')
        context['checked_v21primary'] = self.request.GET.get('v21primary', '')
        context['checked_v22general'] = self.request.GET.get('v22general', '')
        context['checked_v23town'] = self.request.GET.get('v23town', '')
        
        return context


class VoterDetailView(DetailView):
    ''' View to display a single Voter's detailed information '''
    
    template_name = "voter_analytics/voter_detail.html"
    model = Voter
    context_object_name = "voter"

class VoterGraphsView(ListView):
    ''' View to display graphs of aggregate Voter data '''
    
    template_name = "voter_analytics/graphs.html"
    model = Voter
    context_object_name = "voters"
    
    def get_queryset(self):
        ''' Filter results based on form parameters - reusing logic from VoterListView '''
        
        queryset = super().get_queryset()
        
        # Get filter parameters from GET request
        party = self.request.GET.get('party')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')
        
        # Apply filters
        if party:
            queryset = queryset.filter(party=party)
        
        if min_birth_year:
            queryset = queryset.filter(DOB__year__gte=int(min_birth_year))
        
        if max_birth_year:
            queryset = queryset.filter(DOB__year__lte=int(max_birth_year))
        
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        
        # Filter by election participation
        if v20state:
            queryset = queryset.filter(v20state='TRUE')
        
        if v21town:
            queryset = queryset.filter(v21town='TRUE')
        
        if v21primary:
            queryset = queryset.filter(v21primary='TRUE')
        
        if v22general:
            queryset = queryset.filter(v22general='TRUE')
        
        if v23town:
            queryset = queryset.filter(v23town='TRUE')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        ''' Create graphs using Plotly and add to context '''
        
        context = super().get_context_data(**kwargs)
        
        # Get filtered queryset
        voters = self.get_queryset()
        
        # Graph 1: Histogram of voters by year of birth
        birth_years = voters.values_list('DOB__year', flat=True)
        birth_year_counts = {}
        for year in birth_years:
            birth_year_counts[year] = birth_year_counts.get(year, 0) + 1
        
        sorted_years = sorted(birth_year_counts.keys())
        year_counts = [birth_year_counts[year] for year in sorted_years]
        
        fig1 = go.Figure(data=[
            go.Bar(x=sorted_years, y=year_counts, marker_color='lightblue')
        ])
        fig1.update_layout(
            title='Distribution of Voters by Year of Birth',
            xaxis_title='Year of Birth',
            yaxis_title='Number of Voters',
            template='plotly_white'
        )
        
        graph1_div = plot(fig1, output_type='div', include_plotlyjs=True)
        
        # Graph 2: Pie chart of voters by party affiliation
        party_counts = voters.values('party').annotate(count=Count('party')).order_by('-count')
        parties = [item['party'] for item in party_counts]
        counts = [item['count'] for item in party_counts]
        
        fig2 = go.Figure(data=[
            go.Pie(labels=parties, values=counts, hole=0.3)
        ])
        fig2.update_layout(
            title='Distribution of Voters by Party Affiliation',
            template='plotly_white'
        )
        
        graph2_div = plot(fig2, output_type='div', include_plotlyjs=False)
        
        # Graph 3: Histogram of voter participation by election
        elections = {
            '2020 State': voters.filter(v20state='TRUE').count(),
            '2021 Town': voters.filter(v21town='TRUE').count(),
            '2021 Primary': voters.filter(v21primary='TRUE').count(),
            '2022 General': voters.filter(v22general='TRUE').count(),
            '2023 Town': voters.filter(v23town='TRUE').count(),
        }
        
        election_names = list(elections.keys())
        election_counts = list(elections.values())
        
        fig3 = go.Figure(data=[
            go.Bar(x=election_names, y=election_counts, marker_color='lightgreen')
        ])
        fig3.update_layout(
            title='Voter Participation by Election',
            xaxis_title='Election',
            yaxis_title='Number of Voters Who Participated',
            template='plotly_white'
        )
        
        graph3_div = plot(fig3, output_type='div', include_plotlyjs=False)
        
        # Add graphs to context
        context['graph1'] = graph1_div
        context['graph2'] = graph2_div
        context['graph3'] = graph3_div
        
        # Add filter options to context (reusing from VoterListView)
        parties = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['parties'] = parties
        context['years'] = range(1920, 2010)
        context['voter_scores'] = range(0, 6)
        
        # Preserve filter parameters in context
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_year'] = self.request.GET.get('min_birth_year', '')
        context['selected_max_year'] = self.request.GET.get('max_birth_year', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['checked_v20state'] = self.request.GET.get('v20state', '')
        context['checked_v21town'] = self.request.GET.get('v21town', '')
        context['checked_v21primary'] = self.request.GET.get('v21primary', '')
        context['checked_v22general'] = self.request.GET.get('v22general', '')
        context['checked_v23town'] = self.request.GET.get('v23town', '')
        
        # Add count of filtered voters
        context['total_voters'] = voters.count()
        
        return context