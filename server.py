import collections
import os.path
import uuid
from flask import Flask, render_template, redirect, request, session


app = Flask(__name__)


def load_table(filename="form_export.csv"):
    results = []
    if os.path.isfile("form_export.csv"):
        with open("form_export.csv") as f:
            for line in f:
                results.append(line.strip().split(","))
            return results


@app.route('/')
def route_index():
    results = load_table()
    return render_template('list.html', results=results)


@app.route('/add-story')
def route_add():
    return render_template('form.html')


@app.route('/delete-story', methods=['POST'])
def route_delete():
    results = load_table()
    img_id = request.form['bin']
    for row in results:
        if img_id == row[0]:
            results.remove(row)
    with open("form_export.csv", "w") as f:
        for record in results:
            row = ','.join(record)
            f.write(row + "\n")
    return redirect('/')


@app.route('/story/<story_id>', methods=['POST'])
def route_edit(story_id):
    story_id = request.form['edit']
    results = load_table()
    img_id = request.form['edit']
    for row in results:
        if img_id == row[0]:
            story_to_edit = row
            results.remove(row)
    with open("form_export.csv", "w") as f:
        for record in results:
            row = ','.join(record)
            f.write(row + "\n")
    return render_template('form_edit.html', story=story_to_edit)


@app.route('/save-story', methods=['POST'])
def route_save():
    print('POST request recieved')
    form_dict = dict(request.form)
    form_dict = collections.OrderedDict(sorted(form_dict.items()))
    form_list = list(form_dict.values())
    form_list.insert(0, uuid.uuid4())
    form_string = ",".join(str(x).strip("[]''") for x in form_list)
    if os.path.isfile("form_export.csv"):
        with open("form_export.csv", 'a') as f:
            [f.write(form_string)]
            [f.write("\n")]
    else:
        with open("form_export.csv", 'w') as f:
            [f.write(form_string)]
            [f.write("\n")]
    return redirect('/')


@app.route('/save-modified-story', methods=['POST'])
def route_save_modified():
    print('POST request recieved')
    form_dict = dict(request.form)
    form_dict = collections.OrderedDict(sorted(form_dict.items()))
    form_list = list(form_dict.values())
    form_string = ",".join(str(x).strip("[]''") for x in form_list)
    with open("form_export.csv", 'a') as f:
        [f.write(form_string)]
        [f.write("\n")]
    return redirect('/')


if __name__ == "__main__":
    app.secret_key = 'secret_key_change_this_please'
    app.run(debug=True, port=5000)
