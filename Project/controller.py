from flask import Flask, render_template, request
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask import Flask
from wtforms import Form, FloatField, validators
# from compute import compute
# from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)

app = Flask(__name__)
title_list1 =[]
content_list = []
dictionary = {}

# View
@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("view_input.html")


@app.route('/result', methods=['GET', 'POST'])
def sum():
	if request.method == 'POST': 
		global gauth 
		gauth = GoogleAuth()
		gauth.LocalWebserverAuth()
		global drive
		drive = GoogleDrive(gauth)
		global AvNotesFolderId

		#Folder to Create
		FolderName = 'av_notes'

		#List of files/folders in drive
		file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

		#If av_notes already present, fetch folder ID
		for file1 in file_list:
			if 'av_notes' in file1['title']:
				# print("inside this*******************************************")
				AvNotesFolderId = file1['id']

		#Create list of file/folder titles in drive
		title_list = []
		for file1 in file_list:
			title_list.append(file1['title'])

		#AvNotesFolderId = '1fXAgB5ViLII2uXquHrYAHAJPS4og1h6N'

		#Check if folder is already created or not
		if FolderName not in title_list:
			#print("inside first if")
			#Create folder
			folder_metadata = {'title' : FolderName, 'mimeType' : 'application/vnd.google-apps.folder'}
			folder = drive.CreateFile(folder_metadata)
			folder.Upload()
			# AvNotesFolderId = FolderName['id']

		#Fetch folder ID
		file_list2 = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
		for file1 in file_list2:
			if 'av_notes' in file1['title']:
				AvNotesFolderId = file1['id']

		#Lists files of av_notes directory
		file_list1 = drive.ListFile({'q': "\'"+AvNotesFolderId+"\' in parents and trashed=false"}).GetList()
		return render_template("list.html", file_list=file_list, file_list1=file_list1)


@app.route('/new_note', methods=['GET', 'POST'])
def new_note():
	#print("yoloswag")
	if request.method == 'GET':
		return render_template('new_note.html')
	else:
		global Heading
		Heading = request.form.get('Heading')
		global Note
		Note = request.form.get('Note')

		#file_name = 'yomama.txt'
		#AvNotesFolderId = '1fXAgB5ViLII2uXquHrYAHAJPS4og1h6N'
		file_list1 = drive.ListFile({'q': "\'"+AvNotesFolderId+"\' in parents and trashed=false"}).GetList()
		
		#Create list of file titles in the folder
		global title_list1
		title_list1 = []
		for file3 in file_list1:
			title_list1.append(file3['title'])

		#Create file
		#Added check if file is already created or not
		if Heading not in title_list1:
			# print("inside if")
			file_metadata = {'title': Heading, "parents": [{"id": AvNotesFolderId, "kind": "drive#childList"}]}
			file_drive = drive.CreateFile(file_metadata)
			file_drive.SetContentString(Note)
			file_drive.Upload()

		global content_list
		content_list = []
		for test_file in file_list1:
			test_file.FetchMetadata()
			content_list.append(test_file.GetContentString())

		# for contents in content_list:
		# 	content_list.append(contents['Note'])
		# print(content_list)
		dictionary = dict(zip(title_list1,content_list))
		# f = open('test.txt','w')
		# for key in dictionary.keys():
		# 	f.write(key)
		# 	f.write("\t")
		# 	f.write(dictionary[key])
		# 	f.write("\n")
		# f.close()
		# f = open('test2.txt','w')
		# for key in content_list:
		# 	f.write(key)
		# 	f.write("\n")
		# f.close()

		# f = open('test3.txt','w')
		# for key in title_list1:
		# 	f.write(key)
		# 	f.write("\n")
		# f.close()

		return render_template('post_note.html', Heading=Heading ,Note=Note)

@app.route('/view_note', methods=['GET', 'POST'])
def view_note():
	global dictionary
	dictionary = dict(zip(title_list1,content_list))
	print(dictionary)
	return render_template('view_note.html', dictionary=dictionary)


@app.route('/logout')
def logout():
    #GoogleAuth.signOut()
    #gapi.auth2.getAuthInstance().disconnect();
    return render_template('logout.html')

if __name__ == '__main__':
	app.run(debug=True)