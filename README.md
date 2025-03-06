# ModelDevelopmentTool
import os
import pandas as pd
from django.conf import settings
from django.http import JsonResponse

def load_stored_file():
    # Assuming the file is stored in the 'media/uploads' directory
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    
    # Get the latest uploaded file
    files = sorted(
        [f for f in os.listdir(upload_dir) if f.endswith(('.csv', '.xlsx'))],
        key=lambda x: os.path.getctime(os.path.join(upload_dir, x)),
        reverse=True,
    )
    
    if not files:
        return JsonResponse({"error": "No uploaded file found"}, status=400)
    
    latest_file = os.path.join(upload_dir, files[0])
    
    # Load file using pandas
    if latest_file.endswith(".csv"):
        df = pd.read_csv(latest_file)
    else:
        df = pd.read_excel(latest_file)
    
    return df  # Return DataFrame for further processing
