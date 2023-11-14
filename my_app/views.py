
import os
import tempfile
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive"]
folder_id = '1DUaOtg-_HeQrm2jFccPZ2q7mvfeUzVOD'


def home(request):
    return render(request,'base.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        # Check if username is unique
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('signup')

        # Create and save the user
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, 'Account created successfully!')
        print('Account created successfully!')
        return redirect('login')
      
    return render(request, 'signup.html')

def drive_authenticate():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    print(creds.to_json())            
    return creds

def login_handler(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                drive_authenticate()
            except Exception as e:
                messages.warning(request, f"Failed to authenticate: {str(e)}")
                return redirect('login.html')
                            
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')  # Replace 'home' with the name of your home view or URL
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')


@login_required(login_url='login')  
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file_to_upload = request.FILES['file']

        try:
            # Authenticate with Google Drive
            service = build("drive", "v3", credentials=drive_authenticate())

            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in file_to_upload.chunks():
                    temp_file.write(chunk)

            # Set up the file metadata
            file_metadata = {
                'name': file_to_upload.name,
                'parents': [folder_id],
            }

            # Set up the media upload using the file path
            media = MediaFileUpload(temp_file.name, mimetype=file_to_upload.content_type)

            # Execute the file upload
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            # Delete the temporary file
            os.remove(temp_file.name)

            return redirect('show_files')

        except HttpError as error:
            return HttpResponse(f'File upload failed: {error}', status=500)

    return render(request, 'file_upload.html')

@login_required(login_url='login')  
def show_files(request):
    try:
        # Authenticate with Google Drive
        creds = drive_authenticate()

        if creds:
            # Initialize the Google Drive service
            service = build("drive", "v3", credentials=creds)

            try:
                query = f"'{folder_id}' in parents and trashed=false"
                results = service.files().list(q=query).execute()
                files = results.get('files', [])

                for file in files:
                    # Add image URL to the file object
                    file['image_url'] = f'https://drive.google.com/uc?export=view&id={file["id"]}'
                    print(file['image_url'])

                # Render the show_files.html template with the files
                return render(request, 'show_files.html', {'files': files})

            except HttpError as error:
                print(f"An error occurred: {error}")
                # Render the error.html template with an error message
                return render(request, 'error.html', {'error_message': 'Failed to fetch files from Google Drive.'})

    except Exception as e:
        # Render the error.html template with the exception message
        return render(request, 'error.html', {'error_message': str(e)})
    

def delete_file(request, file_id):
    try:
        # Authenticate with Google Drive
        creds = drive_authenticate()

        if creds:
            service = build("drive", "v3", credentials=creds)

            if file_id:
                try:
                    service.files().delete(fileId=file_id).execute()
                    print(f'File ID: {file_id} deleted successfully.')
                except HttpError as error:
                    print(f"An error occurred: {error}")

                return redirect('show_files')
            else:
                # If file ID is not provided, show an error
                return render(request, 'error.html', {'error_message': 'File ID not provided for deletion.'})

        # If credentials are not available, show an authentication error
        return render(request, 'error.html', {'error_message': 'Authentication failed. Please authenticate with Google Drive.'})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})
    
    




