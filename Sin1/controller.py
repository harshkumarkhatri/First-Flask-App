from flask import Flask, render_template, request
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask import Flask
from wtforms import Form, FloatField, validators
from compute import compute

app = Flask(__name__)

# Model
class InputForm(Form):
	a = FloatField(validators=[validators.InputRequired()])
	b = FloatField(validators=[validators.InputRequired()])

# View
@app.route('/', methods=['GET', 'POST'])
def index():
	form = InputForm(request.form)
	return render_template("view_input.html", form=form)


@app.route('/result', methods=['GET', 'POST'])
def sum():
	form = InputForm(request.form)
	if request.method == 'POST' and form.validate():
		a = form.a.data
		b = form.b.data
		s = compute(a, b)
		global gauth 
		gauth = GoogleAuth()
		gauth.LocalWebserverAuth()
		global drive
		drive = GoogleDrive(gauth)

		#Folder to Create
		#ToDo : Later access file from this folder only
		FolderName = 'av_notes'
		#List files
		#ToDo : List files of a certain directory only
		file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
		# for file1 in file_list:
		# 	print('title: %s, id: %s' % (file1['title'], file1['id']))

		#Create list of file titles
		title_list = []
		for file1 in file_list:
			title_list.append(file1['title'])

		AvNotesFolderId = '1fXAgB5ViLII2uXquHrYAHAJPS4og1h6N'
		#check if folder is already created or not
		if FolderName not in title_list:
			print("inside first if")
			#Create folder
			folder_metadata = {'title' : FolderName, 'mimeType' : 'application/vnd.google-apps.folder'}
			folder = drive.CreateFile(folder_metadata)
			folder.Upload()
		# #Lists files of a av_notes directory only
		file_list1 = drive.ListFile({'q': "'1fXAgB5ViLII2uXquHrYAHAJPS4og1h6N' in parents and trashed=false"}).GetList()
		# for file2 in file_list1:
		# 	print('title: %s, id: %s' % (file2['title'], file2['id']))
		return render_template("list.html", file_list=file_list, file_list1=file_list1)

	#return render_template("view_output.html", form=form, s=s)


@app.route('/new_note', methods=['GET', 'POST'])
def new_note():
	if request.method == 'GET':
		return render_template('new_note.html')
	else:
		Heading = request.form.get('Heading')
		Note = request.form.get('Note')
		#file_name = 'yomama.txt'
		AvNotesFolderId = '1fXAgB5ViLII2uXquHrYAHAJPS4og1h6N'
		file_list1 = drive.ListFile({'q': "'1fXAgB5ViLII2uXquHrYAHAJPS4og1h6N' in parents and trashed=false"}).GetList()
		#Create list of file titles in the folder
		title_list1 = []
		for file3 in file_list1:
			title_list1.append(file3['title'])

		#Create file
		#Added check if file is already created or not
		if Heading not in title_list1:
			print("inside if")
			file_metadata = {'title': Heading, "parents": [{"id": AvNotesFolderId, "kind": "drive#childList"}]}
			file_drive = drive.CreateFile(file_metadata)
			file_drive.SetContentString(Note)
			file_drive.Upload()
		return render_template('post_note.html', Heading=Heading ,Note=Note)


if __name__ == '__main__':
	app.run(debug=True)