from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Document
from .forms import UploadFileForm
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

import json
import os
import tempfile
import boto
import boto.s3
import sys
from boto.s3.key import Key
import boto.s3.connection

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect('/upload/')
	else:
		return HttpResponse("Invalid Credentials. Please refresh the page.")

def get_secret(setting):
    file_path = BASE_DIR+"/image_to_link/secrets.json"
    try:
        with open(file_path) as file:
            secrets = json.loads(file.read())
            try:
                return secrets[setting]
            except KeyError:
                error_message = "Set the {0} variable".format(setting)
                raise ImproperlyConfigured(error_message)
    except FileNotFoundError:
        error_message = "secrets.json not found."
        raise ImproperlyConfigured(error_message)

@login_required(login_url='/')
def upload_file(request):
    if request.method == 'POST':
    	form = UploadFileForm(request.POST, request.FILES)
    	
    	if form.is_valid():
    		
    		AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
    		AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")

    		bucket_name = "flyrobe.image"
    		conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, calling_format=boto.s3.connection.OrdinaryCallingFormat(), host ='s3-ap-southeast-1.amazonaws.com')

    		bucket = conn.get_bucket(bucket_name)
    		bucket = conn.get_bucket(bucket_name, validate=True)


    		filename= request.FILES['docfile'].name
    		filename_part = filename.split('.')
    		tempfile_type = '.' + str(filename_part[1])

    		if request.POST['title']:
    			key_name = request.POST['title']
    			key = boto.s3.key.Key(bucket, key_name)
    		else:
    			key_name = filename

    		data = request.FILES.get('docfile')
    		tup = tempfile.mkstemp(suffix = tempfile_type) # make a tmp file
    		f = os.fdopen(tup[0], 'w')
    		f.write(data.read()) # write the tmp file
    		f.close()

    		filepath = tup[1]
    		with open(filepath) as f:
    			#import pdb; pdb.set_trace()
    			key.set_contents_from_file(f)
    		os.remove(filepath)

    		cloudfront_link = "https://d3nfc7oea1f362.cloudfront.net/" + key_name
    		form = UploadFileForm()
    		context = {'cloudfront_link': cloudfront_link, 'form': form}

    		# form = UploadFileForm()
    		return render(request, 'image_to_link/upload.html', context)
    		#return HttpResponse(cloudfront_link)
    		
    # else:
    # 	return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'image_to_link/upload.html', {'form': form})
