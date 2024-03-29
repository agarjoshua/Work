from django.shortcuts import render, redirect
from .models import Book, Author, Docservice, ServiceType, Issue
from user.models import Department
from servicemanager.models import Book, Employee
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
import datetime
from .utilities import getmybooks
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth
from core import settings




def home(request):
    return render(
        request,
        "servicemanager/home.html",
    )

# Book
def library(request):
    requestedbooks, issuedbooks = getmybooks(request.user)
    allbooks = Book.objects.all()

    return render(
        request,
        "servicemanager/doclibrary.html",
        {
            "books": allbooks,
            "issuedbooks": issuedbooks,
            "requestedbooks": requestedbooks,
        },
    )


def sort(request):
    sort_type = request.GET.get("sort_type")
    sort_by = request.GET.get("sort")
    requestedbooks, issuedbooks = getmybooks(request.user)
    if "author" in sort_type:
        author_results = Author.objects.filter(name__startswith=sort_by)
        return render(
            request,
            "servicemanager/home.html",
            {
                "author_results": author_results,
                "issuedbooks": issuedbooks,
                "requestedbooks": requestedbooks,
                "selected": "author",
            },
        )
    else:
        books_results = Book.objects.filter(name__startswith=sort_by)
        return render(
            request,
            "servicemanager/home.html",
            {
                "books_results": books_results,
                "issuedbooks": issuedbooks,
                "requestedbooks": requestedbooks,
                "selected": "book",
            },
        )


def search(request):
    search_query = request.GET.get("search-query")
    search_by_author = request.GET.get("author")
    requestedbooks, issuedbooks = getmybooks(request.user)

    if search_by_author is not None:
        author_results = Author.objects.filter(name__icontains=search_query)
        return render(
            request,
            "servicemanager/home.html",
            {
                "author_results": author_results,
                "issuedbooks": issuedbooks,
                "requestedbooks": requestedbooks,
            },
        )
    else:
        books_results = Book.objects.filter(
            Q(name__icontains=search_query) | Q(category__icontains=search_query)
        )
        return render(
            request,
            "servicemanager/home.html",
            {
                "books_results": books_results,
                "issuedbooks": issuedbooks,
                "requestedbooks": requestedbooks,
            },
        )


@login_required(login_url="/employee/login/")
def addrequest(request):  # sourcery skip: avoid-builtin-shadow
    test = Employee.objects.all()
    service_type = ServiceType.objects.all()
    all_departments = Department.objects.all()
    doc_service = Docservice.objects.all()
    print(doc_service.status)

    if request.method != "POST":
        return render(
            request,
            "servicemanager/addrequest.html",
            {
                "service_type": service_type,
                "department": all_departments,
                "doc_service": doc_service
            },
        )
    department = request.POST.get("department")
    details = request.POST.get("details")
    pages = request.POST.get("pages")
    file = request.FILES.get("file")
    type = request.POST.get("service")

    try:
        test = Docservice.objects.create(
            employee=request.user,
            type=request.POST["service"],
            details=details,
            pages=pages,
            Department=department,
            file=file,
        )
    except Exception as e:
        print(e)

    messages.success(request, "Request Added succesfully")
    return render(
        request,
        "servicemanager/addrequest.html"
    )


@login_required(login_url="/employee/login/")
def doccenter(request):  # sourcery skip: avoid-builtin-shadow
    all_departments = Department.objects.all()
    test = Employee.objects.all()
    service_type = ServiceType.objects.all()

    if request.method != "POST":
        return render(
            request,
            "servicemanager/doccenter.html",
            {"service_type": service_type, "department": all_departments},
        )
    title = request.POST.get("title")
    name = request.POST.get("name")
    staff_id = request.POST["staff_id"]
    department = request.POST.get("department")
    type = request.POST.get("service")
    pages = request.POST.get("pages")
    rate = request.POST.get("rate")
    try:
        cost = int(pages) * int(rate)
    except Exception as e:
        print(e)
        messages.success(request, f"There was an error: {e}")
    details = request.POST.get("details")
    signature = request.FILES.get("signature")
    status = request.POST.get('status')
    if status in [choice[0] for choice in Docservice.STATUS_CHOICES]:
        status = status
        

    try:
        test = Docservice.objects.create(
            title=title,
            name=name,
            staff_id=staff_id,
            department=department,
            service_type=type,
            pages=pages,
            rate=rate,
            cost=cost,
            status = status,
            details=details,
            signature=signature,
        )
        messages.success(request, "Request Added succesfully")

        dept = Department.objects.get(name=department).vote
        new_vote_head = int(dept) - int(cost)
        new_vote = Department.objects.get(name=department)
        new_vote.vote = new_vote_head
        new_vote.save()

    except Exception as e:
        print(e)

    return render(
        request,
        "servicemanager/doccenter.html",
    )


@login_required(login_url="/employee/login/")
def ictservices(request):
    department = Employee.objects.get(staff_id=request.user).department
    test = Employee.objects.all()
    service_type = ServiceType.objects.all()

    if request.method == "POST":
        department = Employee.objects.filter(staff_id=request.user)
        details = request.POST.get("details")
        pages = request.POST.get("pages")
        file = request.FILES.get("file")
        type = request.POST.get("service")
        print("---------------------------------------------")
        print(type)
        print("---------------------------------------------")

        try:
            test = Service.objects.create(
                employee=request.user,
                type=request.POST["service"],
                details=details,
                pages=pages,
                Department=Employee.objects.get(staff_id=request.user).department,
                file=file,
            )
        except Exception as e:
            print(e)

        messages.success(request, f"Request Added succesfully")
        return render(
            request,
            "servicemanager/doccenter.html",
            # {'authors': authors,}
        )

    else:
        return render(
            request,
            "servicemanager/doccenter.html",
            {
                # 'authors': authors,
                "service_type": service_type
            },
        )


@login_required(login_url="/employee/login/")
@user_passes_test(lambda u: u.is_superuser, login_url="/employee/login/")
def deletebook(request, bookID):
    book = Book.objects.get(id=bookID)
    messages.success(request, f"Book - {book.name} Deleted succesfully ")
    book.delete()
    return redirect("/")


#  ISSUES
def request(request):
    issues = Docservice.objects.all()
    print(issues)
    return render(request, "servicemanager/requests.html", {"issues": issues})


# approval function
# @user_passes_test(lambda u: not u.is_superuser, login_url='/employee/login/') 

def delete_request(request, issueid):
    issues = Docservice.objects.all()
    old_issue = Docservice.objects.get(id=issueid)
    print(old_issue)
    old_issue.delete()
    return render(request, "servicemanager/requests.html", {"issues": issues})


@login_required(login_url="/admin/")
@user_passes_test(lambda u: u.is_superuser, login_url="/employee/login/")
def approverequest(request, issueid):
    issues = Docservice.objects.all()
    service = Docservice.objects.get(id=issueid)

    service.return_date = timezone.now() + datetime.timedelta(days=15)
    service.issued_at = timezone.now()
    service.issued = True
    service.save()
    return render(request, "servicemanager/requests.html", {"issues": issues})


@login_required(login_url="/employee/login/")
@user_passes_test(lambda u: not u.is_superuser, login_url="/employee/login/")
def issuerequest(request, bookID):

    employee = Employee.objects.get(staff_id=request.user)
    print(employee)
    if employee:
        book: str = Book.objects.get(id=bookID)
        issue, created = Issue.objects.get_or_create(book=book, employee=employee)
        print(issue, created)
        messages.success(request, f"Book - {book.name} Requested succesfully")
        return redirect("home")

    messages.error(request, "You are Not a employee !")

    return redirect("/")


@login_required(login_url="/employee/login/")
@user_passes_test(lambda u: not u.is_superuser, login_url="/employee/login/")
def myissues(request):
    if Employee.objects.filter(staff_id=request.user):
        # employee = employee.objects.filter(staff_id=request.user)[0]
        # issues = Docservice.objects.filter(employee=request.user)
        issues = Docservice.objects.all()
        print(issues)

        # if request.GET.get('issued') is not None:
        #     issues = Issue.objects.filter(employee=employee, issued=True)
        # elif request.GET.get('notissued') is not None:
        #     issues = Issue.objects.filter(employee=employee, issued=False)
        # else:
        #     issues = Issue.objects.filter(employee=employee)

        return render(request, "servicemanager/myissues.html", {"issues": issues})

    messages.error(request, "You are Not a employee !")
    return redirect("/")


@login_required(login_url="/admin/")
@user_passes_test(lambda u: u.is_superuser, login_url="/admin/")
def requestedissues(request):
    if (
        request.GET.get("employeeID") is not None
        and request.GET.get("employeeID") != ""
    ):
        try:
            user = User.objects.get(username=request.GET.get("employeeID"))
            employee = Employee.objects.filter(staff_id=user)
            if employee:
                employee = employee[0]
                issues = Issue.objects.filter(employee=employee, issued=False)
                return render(
                    request, "servicemanager/allissues.html", {"issues": issues}
                )
            messages.error(request, "No employee found")
            return redirect("/all-issues/")
        except User.DoesNotExist:
            messages.error(request, "No employee found")
            return redirect("/all-issues/")

    else:
        issues = Issue.objects.filter(issued=False)
        return render(request, "servicemanager/allissues.html", {"issues": issues})


@login_required(login_url="/admin/")
@user_passes_test(lambda u: u.is_superuser, login_url="/employee/login/")
def issue_book(request, issueID):
    issue = Issue.objects.get(id=issueID)
    issue.return_date = timezone.now() + datetime.timedelta(days=15)
    issue.issued_at = timezone.now()
    issue.issued = True
    issue.save()
    return redirect("/all-issues/")
