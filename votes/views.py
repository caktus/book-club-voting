from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone

from books.models import Book
from .models import Election, Ballot
from .forms import ElectionForm
from .helpers import find_winner, gather_ballots


def open_elections_list(request):
    elections = Election.objects.all()
    form = ElectionForm()
    print(elections)
    return render(request, "votes/election_list.html", {
        'elections': elections,
        'form': form,
    })


def election_detail_view(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    # See if a winner needs to be selected
    if election.is_closed and election.winner is None:
        winner = find_winner(gather_ballots(election), election.candidates.count())
        if len(winner) == 1:
            election.winner = Book.objects.get(id=int(winner[0]))
        else:
            # There is more than one winner; kick off a runoff election
            pass
    return render(request, "votes/election_detail.html", {'election': election})


def new_election(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('/')


def create_ballot(request):
    if request.method == 'POST':
        election = get_object_or_404(Election, id=request.POST['election_id'])
        selections = request.POST['selections'].split(',')
        vote = Ballot(election=election, selections=selections)
        vote.save()
        return redirect('election_detail', election_id=election.id)
    return redirect('/')


def close_election(request):
    if request.method == 'POST':
        election = get_object_or_404(Election, id=request.POST['election_id'])
        election.close = timezone.now()
        election.save()
        return redirect('election_detail', election_id=election.id)
    return redirect('/')