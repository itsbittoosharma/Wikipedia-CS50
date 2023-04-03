from django.shortcuts import redirect, render
from django.http import HttpResponseNotFound
from django.urls import reverse
from . import util
import markdown2

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