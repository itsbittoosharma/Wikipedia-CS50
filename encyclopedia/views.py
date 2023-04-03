from django.shortcuts import redirect, render
from django.http import HttpResponseNotFound
from django import forms
from django.urls import reverse
from . import util
import markdown2
import random as rand

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title ", max_length=20,min_length=3,required=True)
    content = forms.CharField(widget=forms.Textarea())

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

def index(request):
    if request.GET.__contains__('q'):
        q=request.GET['q']
        if util.get_entry(q) is not None:
            return redirect(reverse("wiki",kwargs={"title":q}))
        else:
            return render(request,"encyclopedia/index.html",
                          {
                "entries": util.list_entries(q),
                "title": f"Search Results for \"{q}\""
                          })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "All Pages"
        })

def wiki(request, title):
    if(title==None):
        return HttpResponseNotFound(render(request,"encyclopedia/error_not_found.html"))
    content = util.get_entry(title)
    if content is None:
        return HttpResponseNotFound(render(request,"encyclopedia/error_not_found.html"))
    else:
        content = markdown2.markdown(content)
        return render(request,"encyclopedia/wiki.html",
                  {
        "title":title,
        "content":content
                  })
    
def newpage(request):
    if request.method=="GET":
        return render(request,"encyclopedia/newpage.html",
                    {
            "title":"Create New Page",
            "form":NewPageForm()
                    })  
    else:
        form = NewPageForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            content=form.cleaned_data['content']
            util.save_entry(title,content)
            return redirect(reverse("wiki",kwargs={"title":title}))
        else:
            return render(request,"encyclopedia/newpage.html",
                          {
                "title":"Create New Page",
                "form":NewPageForm(form)
                          })
        
def editpage(request,title):
    if request.method == "GET":
        return render(request,"encyclopedia/editpage.html",
                      {
            "title":title,
            "content":util.get_entry(title),
                      })
    else:
        content = request.POST['content']
        util.save_entry(title,content)
        return redirect(reverse("wiki",kwargs={"title":title}))
    
def random(request):
    list = util.list_entries()
    if len(list) == 0:
        return HttpResponseNotFound(render(request,"encyclopedia/error_not_found.html"))
    title_index = rand.randint(0,len(list)-1)
    return redirect(reverse("wiki",kwargs={"title":list[title_index]}))