import datetime
import os
import re
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
uploads_dir = os.path.join(app.root_path, 'static')


@app.route('/')
def hello_world():
    file_list = os.listdir('static')
    result = []
    for i in file_list:
        if i.endswith('.txt'):
            file_name = i.split('.')[0]
            file_date = re.findall(r'\[.+]', file_name)
            file_name = file_name.replace(file_date[0], '')
            with open(os.path.join(app.root_path, 'static', i), 'r') as f:
                lines = f.readlines()
                result.append({'file_name': file_name, 'comment': lines[0], 'ip': lines[1], 'date': file_date[0]})
    return render_template('uploader.html', file_list=result)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    info = request.form['input-info']
    currentDate = '[' + datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S") + '] '
    if file:
        file.filename = currentDate + file.filename
        file.save(os.path.join(uploads_dir, file.filename))
        file_without_extension = file.filename.split('.')[0]

        with open('static/' + file_without_extension + '.txt', 'w') as txt:
            if info:
                txt.write(info)
            else:
                txt.write('-')

            txt.write('\n')
            txt.write(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))

        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
