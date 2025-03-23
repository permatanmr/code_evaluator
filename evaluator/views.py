import subprocess
from django.http import JsonResponse
from django.shortcuts import render
import shutil


def home(request):
    return render(request, "home.html")

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
