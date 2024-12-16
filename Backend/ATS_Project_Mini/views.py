from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UploadedFile
from .forms import UploadFileForm
from .functions import load_job_criteria, analyze_resume, calculate_score, generate_feedback, generate_appreciation
import os
from django.conf import settings
from django.templatetags.static import static 

# Create your views here.


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('upload_file')
#     else:
#         form = UploadFileForm()
#     files = UploadedFile.objects.all()
#     return render(request, 'upload_file.html', {'form': form, 'files': files})

def index(request):
    return render(request, "index.html")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file
            uploaded_file = form.save()

            # Get the file path of the uploaded file
            file_path = uploaded_file.file.path  # Django automatically saves files in MEDIA_ROOT
            print(f"File path after upload: {file_path}")
            try:
                # Process the uploaded resume using ATS algorithm
                print("***********************--------------------************************")
                print(f"File path passed to ats_algorithm: {file_path}")  # Debug print

                score, feedback_path = ats_algorithm(file_path)
                print("***********************--------------------************************")

                # Display the score and feedback path to the user
                return render(request, 'upload_file.html', {
                    'form': form,
                    'score': score,
                    'feedback_path': feedback_path,
                    'files': UploadedFile.objects.all()
                })
            except FileNotFoundError as e:
                # Handle file not found errors
                return render(request, 'upload_file.html', {
                    'form': form,
                    'error': f"File not found: {str(e)}",
                    'files': UploadedFile.objects.all()
                })

            except Exception as e:
                # Handle any errors in processing the file
                return render(request, 'upload_file.html', {
                    'form': form,
                    'error': f"Error processing the file: {str(e)}",
                    'files': UploadedFile.objects.all()
                })
    else:
        form = UploadFileForm()

    # Initial render with no score
    return render(request, 'upload_file.html', {
        'form': form,
        'files': UploadedFile.objects.all()
    })




def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response



# View to pass resume to Analyzer Framework
def ats_algorithm(filepath):
    # Ensure the path to job_criteria.json is correct
    job_criteria_path = os.path.join(r'C:\Users\ILG2KOR\Desktop\CERTIFICATES\Isolated\Backend', 'ATS_Project_Mini', 'static', 'job_criteria.json')
    print("---------------------------------*************************---------------------------")

    print(f"Job criteria path: {job_criteria_path}")
    print("---------------------------------*************************---------------------------")
     # Ensure the file exists before loading it
    if not os.path.exists(job_criteria_path):
        raise FileNotFoundError(f"The job_criteria.json file was not found at {job_criteria_path}")
    
    job_criteria = load_job_criteria(job_criteria_path)
    print('Job Criters is executed',job_criteria)
    print("-------------------------------------------------------------------------------")
    results, text = analyze_resume(filepath, job_criteria)
    print('Result is executed',results)
    print("-------------------------------------------------------------------------------")
    score = calculate_score(results, job_criteria)
    feedback_file = generate_feedback(results)
    appreciation_file = generate_appreciation(results)
    return score, feedback_file