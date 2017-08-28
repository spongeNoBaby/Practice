from flask import Flask, request, url_for, send_from_directory
import os
import Q4
import Q2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 1024

html = '''
	<!DOCTYPE html>
	<title>Upload File</title>
	<center>
	<h1>Upload File</h1>
	<form method=post enctype=multipart/form-data>
		*Test File: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=file name=test_file><p/>
		Synonym File: <input type=file name=syn_file><p/>
		Antonym File: <input type=file name=ant_file> <input type=submit value=upload> <p/> 
		Note: Test File is compulsory, and you need to upload either synonym file or antonym file. All files should be in .txt format.
	</form>
	</center>
	'''

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] == "txt"


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':

		test_file = request.files['test_file']

		if test_file and allowed_file(test_file.filename):
			test_file.save(os.path.join(app.config['UPLOAD_FOLDER'], test_file.filename))
			file_url = url_for('uploaded_file', filename = test_file.filename)

			syn_file = request.files['syn_file']
			ant_file = request.files['ant_file']

			if syn_file and allowed_file(syn_file.filename):
				syn_file.save(os.path.join(app.config['UPLOAD_FOLDER'], syn_file.filename))
				file_url = url_for('uploaded_file', filename = syn_file.filename)
				Q4.final_count_result(syn_file.filename, "", test_file.filename)
				return html + '<center><h1>Simple Output:</h1><br>' + Q4.read_output("Q1_Synonym.txt").replace("\n", "<br/>") + '</center>'
			elif ant_file and allowed_file(ant_file.filename):
				ant_file.save(os.path.join(app.config['UPLOAD_FOLDER'], ant_file.filename))
				file_url = url_for('uploaded_file', filename = ant_file.filename)
				Q4.final_count_result("", ant_file.filename, test_file.filename)
				return html + '<center><h1>Simple Output:</h1><br>' + Q4.read_output("Q1_Antonym.txt").replace("\n", "<br/>") + Q2.replace_antonym(ant_file.filename, test_file.filename).replace("\n", "<br/>") + '</center>'
			else:
				return html + '<center><h1>Synonym/Antonym File Upload Error!</h1></center>'
		else:
			return html + '<center><h1>Test File Upload Error!</h1></center>'
	return html


if __name__ == '__main__':
	app.run()