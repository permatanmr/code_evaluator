import subprocess
from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, "home.html")

# @csrf_exempt  # REMOVE THIS IN PRODUCTION (Use proper CSRF handling instead)
def run_code(request):
    if request.method == "POST":
        code = request.POST.get("code", "")
        language = request.POST.get("language", "python")

        if language == "python":
            command = ["python", "-c", code]
        elif language == "javascript":
            command = ["node", "-e", code]
        elif language == "dart":
            command = ["dart run", "-e", code]
        else:
            return JsonResponse({"output": "Unsupported language"}, status=400)

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            output = result.stdout or result.stderr
        except Exception as e:
            output = str(e)

        return JsonResponse({"output": output})

    return JsonResponse({"error": "Invalid request"}, status=400)

