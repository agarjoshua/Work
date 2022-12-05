from django.urls import path
from .views import (
    home,
    addrequest,
    library,
    approverequest,
    delete_request,
    search,
    addrequest,
    request,
    issuerequest,
    myissues,
    issue_book,
    requestedissues,
    sort,
    doccenter,
    ictservices,
)

urlpatterns = [
    path("", home, name="home"),
    path("search/", search),
    path("sort/", sort),
    path("addrequest/", addrequest),
    path("requests/", request),
    # DOC CENTER 
    path("doccenter/", doccenter),
    path('doclibrary/', library),
    # ICT SERVICES
    path("ictservices/", ictservices),


    path("approve/<int:issueid>/", approverequest),
    path("deleterequest/<int:issueid>/", delete_request),
    path("request-book-issue/<int:bookID>/", issuerequest),
    path("my-issues/", myissues),
    path("all-issues/", requestedissues),
    path("issuebook/<int:issueID>/", issue_book),
]
