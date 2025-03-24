import subprocess
from django.http import JsonResponse
from django.shortcuts import render
import shutil


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from .models import Exam
from django.contrib import messages

#Registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            full_name = form.cleaned_data.get('full_name')

            # Splitting Full Name into First & Last Name
            name_parts = full_name.split()
            user.first_name = name_parts[0]
            user.last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            user.save()

            # Show success message
            messages.success(request, 'Your account has been successfully created! You can now log in.')

            return render(request, 'register.html', {'form': CustomUserCreationForm(), 'delay_redirect': True})
        else:
            # Show error message
            messages.error(request, 'Registration failed! Please check the form and try again.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

# Login View
from .forms import EmailAuthenticationForm
def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  # Django's default field is still called "username"
            password = form.cleaned_data['password']
            user = authenticate(request, email=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, "Login successful!")
                return redirect('exam_index')  # Redirect to a protected page
            else:
                print("error email or password")
                messages.error(request, "Invalid email or password.")
        else:
             print('Form error')
             print(form.errors)
             messages.error(request, form.errors)
    else:
        form = EmailAuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Exam Page (Restricted)
@login_required
def exam_index(request):
    return render(request, 'index.html')

# @csrf_exempt  # REMOVE THIS IN PRODUCTION (Use proper CSRF handling instead)
def run_code(request):
    if request.method == "POST":
        code = request.POST.get("code", "")
        language = request.POST.get("language", "python")
        expected_output = request.POST.get("expected_output", "").strip()

        # Check if Dart is installed
        dart_path = shutil.which("dart")  
        if language == "dart" and not dart_path:
            return JsonResponse({"result": "fail", "output": "Dart not installed"}, status=400)

        # Select appropriate command
        if language == "python":
            command = ["python", "-c", code]
        elif language == "javascript":
            command = ["node", "-e", code]
        elif language == "dart":
            command = [dart_path, "-e", code]
        else:
            return JsonResponse({"result": "fail", "output": "Unsupported language"}, status=400)

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            output = result.stdout.strip() or result.stderr.strip()

            if output == expected_output:
                return JsonResponse({"result": "pass", "output": output})
            else:
                return JsonResponse({"result": "fail", "output": output})
        except Exception as e:
            return JsonResponse({"result": "fail", "output": str(e)})

    return JsonResponse({"error": "Invalid request"}, status=400)

def exam_list(request):
    exams = Exam.objects.all()  # Fetch all exams
    return render(request, 'exam_list.html', {'exams': exams})