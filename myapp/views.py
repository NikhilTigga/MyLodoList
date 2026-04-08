from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
## message framework
from django.contrib import messages
from django.db.models import Sum

# Create your views here.
User = get_user_model()

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        image = request.FILES.get("image")

        #  Check existing email
        if User.objects.filter(email=email).exists():

            messages.error(request, "Email already exists")
            return render(request, "pages/register.html", {"error": "Email already exists"})

        #  Check existing username
        if User.objects.filter(username=username).exists():
            return render(request, "pages/register.html", {"error": "Username already exists"})

        #  Create user (IMPORTANT: use create_user)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if not image:
            messages.error(request, "No image uploaded, using default.")
            return render(request, "pages/register.html", {"error": "Username already exists"})


        #  Save image
        if  image:
            user.image = image
            user.save()

        return render(request, "pages/register.html")

    return render(request, "pages/register.html")


def homeView(request):
    if not request.user.is_authenticated:
        return redirect("login")  # optional but recommended

    taskdata = Task.objects.filter(user=request.user).all()

    # score = Task.objects.filter(user=request.user ,staus='completed').aaggregate
    score = Task.objects.filter(user=request.user,status='completed').aggregate(total_score=Sum('score'))
    context = {
        "data": taskdata,
        "score":score
    }

    messages.success(request, "Welcome to your dashboard!")
    return render(request, "pages/home.html", context)

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect("homeView")  # change this
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "pages/login.html")

    return render(request, "pages/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


from .models import Task

def createView(request):
    if not request.user.is_authenticated:
        return redirect("login")   # or your login url name

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Task.objects.create(
            user=request.user,
            title=title,
            description=description
        )

        return redirect("homeView")  # change to your page

    return render(request, "pages/create.html")


def profile(request):

    if request.user.is_authenticated:
        return render(request,"pages/profile.html")


def editView(request , id):

    if not request.user.is_authenticated:
        return redirect("homeView")
    
    if request.method == "GET":
        tododata =Task.objects.get(id =id)
        context ={

            "data":tododata
        }

        return render(request,"pages/edit.html",context)
    
    ## for edit 

    if request.method =="POST":

        edittitle = request.POST.get("title")
        editdesc = request.POST.get("description")
        status = request.POST.get("is_done")

        if not edittitle or not editdesc or not status:

            return redirect("homeView")
        
        tododata = Task.objects.get(id = id)

        tododata.title=edittitle
        tododata.description = editdesc
        tododata.status = status

        tododata.save()

        return redirect("homeView")




#view for delete to do list

def deleteTodoListview(request, deleteid):
    if not request.user.is_authenticated:
        return redirect("homeView")
    
    if request.method =="GET":

        tododata =Task.objects.get(id=deleteid)

        tododata.delete()

        return redirect("homeView")



    
    



    
    