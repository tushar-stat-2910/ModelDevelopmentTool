import os
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Define a global variable to store uploaded data
InputData = None

@csrf_exempt
def FileUpload(request):
    global InputData  # Use global variable to store data in memory

    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        # Ensure upload directory exists
        upload_dir = "media/uploads/"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Define file save path
        save_path = os.path.join(upload_dir, uploaded_file.name)

        try:
            # Save file to disk
            with open(save_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Load file into memory as DataFrame
            if save_path.endswith(".csv"):
                InputData = pd.read_csv(save_path)
            else:
                InputData = pd.read_excel(save_path)

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "No file uploaded."})
