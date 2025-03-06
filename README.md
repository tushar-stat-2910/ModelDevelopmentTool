from django.shortcuts import render
import pandas as pd

def DataExploration(request):
    global InputData

    if InputData is None:
        return render(request, "App/DataExploration.html", {"summary": None, "error": "No data uploaded yet."})

    try:
        # Compute column-wise summary
        summary = pd.DataFrame({
            "Column Name": InputData.columns,
            "Data Type": InputData.dtypes.values,
            "Missing Values": InputData.isnull().sum().values,
            "Unique Values": InputData.nunique().values
        })

        # Convert DataFrame to a list of dictionaries for easy rendering in Django
        summary_data = summary.to_dict(orient="records")

        return render(request, "App/DataExploration.html", {"summary": summary_data})

    except Exception as e:
        return render(request, "App/DataExploration.html", {"summary": None, "error": str(e)})
