from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

import markdown2
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-10 col-lg-10'}))
    content = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control col-md-10 col-lg-10', 'rows': 12}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def createEntry(request):
    if request.method != "POST":
        return render(request,"encyclopedia/new_entry.html", {"form": NewEntryForm()})
    else:
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
            else:
                return render(request, "encyclopedia/new_entry.html", {
                    "form": form,
                    "existing": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/new_entry.html", {"form": form})

def editEntry(request, title):
    entry = util.get_entry(title)
    
    if entry is None:
        return render(request, "encyclopedia/missing_entry.html", {
            "title": title   
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = title
        form.fields["content"].initial = entry
        form.fields["edit"].initial = True

        return render(request, "encyclopedia/new_entry.html", {
            "form": form,
            "title": title,
            "edit": form.fields["edit"].initial
        })

def entry(request, title):
    entry = util.get_entry(title)
    
    if entry != None:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry), "title": title
        })
    else:
        return render(request, "encyclopedia/missing_entry.html", {
            "title": title
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def randomEntry(request):
    entries = util.list_entries()
    randomEntry = random.choice(entries)

    return HttpResponseRedirect(reverse("entry", kwargs={'title': randomEntry}))

def search(request):
    searched_entry = request.GET.get('q','')

    if(util.get_entry(searched_entry) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'title': searched_entry }))
    else:
        matchingEntries = []

        for entry in util.list_entries():
            if searched_entry.upper() in entry.upper():
                matchingEntries.append(entry)

        return render(request, "encyclopedia/index.html", {
            "entries": matchingEntries, "searched_entry": searched_entry
    })