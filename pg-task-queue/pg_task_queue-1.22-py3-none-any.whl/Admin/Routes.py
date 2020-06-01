import sys
import os
import json
import datetime
from pydoc import locate
from flask import request, send_from_directory, render_template, session, jsonify, redirect, url_for
from Admin.Core import core
from Admin import app, print_request, json_response


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route("/", methods=['GET'])
def index():
    print_request(f'{sys._getframe().f_code.co_name}()', via_print=True)
    return render_template("index.html")


@app.route("/test", methods=['GET'])
def test():
    print_request(f'{sys._getframe().f_code.co_name}()', via_print=True)
    return jsonify({'result': 'ok'})


@app.route("/cookies_info")
def cookies_info():
    for k, v in dict(request.cookies).items():
        print(f'cookie_key {k}: {v}')
    return render_template(".tests/cookies_info.html", cookies=request.cookies)


@app.route("/session_info")
def session_info():
    return render_template(".tests/session_info.html", session_info=session)


@app.route("/datatables")
def datatables():
    return render_template(".tests/datatables.html")


@app.route("/update-row", methods=['POST'])
def update_row():
    print_request(f'{sys._getframe().f_code.co_name}()', via_print=True)
    row = dict(request.form);
    action = 'add' if 'id' not in row else 'update';
    if 'id' not in row:
        row['id'] = 100
    return json_response({'status': 200, 'row': row, 'action': action})


@app.route("/jquery-ui")
def jquery_ui():
    # print_request(f'{sys._getframe().f_code.co_name}()', via_print=True)
    columns = ['id', 'name']
    values = [{'id': 1, 'name': 'One'}, {'id': 2, 'name': 'Two'}]
    table = {'columns': columns, 'values': values}
    return render_template(".tests/jquery_ui.html", table=table)


def get_args():
    if request.form:
        args = request.form
    else:
        try:
            args = request.get_json(force=True)
        except Exception as ex:
            args = request.args
    return args


@app.route('/api/answer', methods=['GET'])
def get_answer():
    text = get_args().get('text')
    print_request(f'{sys._getframe().f_code.co_name}()', via_print=True)
    return jsonify({'text': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')})


@app.route('/api/write_difference', methods=['POST'])
def write_difference():
    print_request(f'{sys._getframe().f_code.co_name}()', via_print=True)
    new_line = ''
    # for k, v in request.form.items():
    #     if new_line != '':
    #         new_line += '; '
    #     new_line += f"{k}: {v}"
    # print(f'new_line: {new_line}')
    diff_filename = os.path.join(os.path.abspath(os.curdir), '.diff.txt')
    # print(f'diff_filename: {diff_filename}')
    with open(diff_filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(request.form) + '\n')
        json.dumps(json.dumps(request.form))
        f.close()
    return jsonify({'sleep_min': 2})


@app.route('/api/get_difference', methods=['GET'])
def get_difference():
    diff_filename = os.path.join(os.path.abspath(os.curdir), '.diff.txt')
    if not os.path.exists(diff_filename):
        return jsonify({'error': f'"{diff_filename}" file not exists...'})
    if not os.path.isfile(diff_filename):
        return jsonify({'error': f'"{diff_filename}" file not a file...'})
    lines = list()
    with open(diff_filename, 'r', encoding='utf-8') as f:
        for x in f:
            line = x.replace('\n', '')
            lines.append(json.loads(line))
        # contents = f.read()
        f.close()
    return jsonify(lines)


@app.route("/zendesk")
def zendesk():
    return render_template(".tests/zendesk.html")


@app.route("/update-cronjob-task", methods=['POST'])
def update_cronjob_task():
    # print_request(f'{sys._getframe().f_code.co_name}()', via_print=True)
    request_data = json.loads(request.get_data())
    columns_types = request_data.get('columnsTypes')
    row = request_data.get('row');
    for k, v in row.items():
        column_type = columns_types.get(k, 'str')
        val_type = locate(column_type)
        row[k] = val_type(v)
    result = core.update_cronjob_task(**row)
    if isinstance(result, str):
        return json_response({'status': 400, 'error': result})
    else:
        action = 'add' if 'task_id' not in row else 'update';
        return json_response({'status': 200, 'row': result, 'action': action})


@app.route("/cronjob_tasks")
def cronjob_tasks():
    # table = core.get_cronjob_tasks()
    # error = None
    # if isinstance(table, str):
    #     error = table
    #     table = None
    # return render_template("cronjob_tasks.html", error=error, table=table)
    return render_template("cronjob_tasks.html")


@app.route("/tasks")
def tasks():
    return render_template("tasks.html")


@app.route("/get-by-ajax", methods=['GET'])
def get_by_ajax():
    # print_request(f'{sys._getframe().f_code.co_name}()', via_print=False)
    request_args = request.args.to_dict()
    if 'get' in request_args:
        get_what = request_args.get('get')
        if get_what in ['cronjob_tasks', 'tasks']:
            if get_what == 'tasks':
                table = core.get_tasks()
            elif get_what == 'cronjob_tasks':
                table = core.get_cronjob_tasks()
            if isinstance(table, str):
                return json_response({'status': 400, 'error': table})
            else:
                return json_response({'status': 200, 'table': table})
        elif get_what == 'footer':
            return json_response({'status': 200, 'footer': core.get_footer()})
        else:
            error = f'unknown get "{get_what}"'
            return json_response({'status': 400, 'error': error})
    else:
        error = f'unknown request_args "{request_args}"'
        return json_response({'status': 400, 'error': error})


@app.route("/pure_ajax", methods=['GET'])
def pure_ajax():
    print_request(f'{sys._getframe().f_code.co_name}()', via_print=True)
    return jsonify({'result': 'ok'})


@app.route("/post-by-ajax", methods=['POST'])
def post_by_ajax():
    # print_request(f'{sys._getframe().f_code.co_name}()', via_print=True)
    request_data = json.loads(request.get_data())
    # print(f'request_data: {request_data}')
    if 'row' in request_data and 'columnsTypes' in request_data:
        columns_types = request_data.get('columnsTypes')
        row = request_data.get('row')
        # print(f'row[0]: {row}')
        for k, v in row.items():
            column_type = columns_types.get(k, 'str')
            val_type = locate(column_type)
            row[k] = val_type(v)
        print(f'row[1]: {row}')
    else:
        error = f'unknown request_data (not exists key "row" and "columnsTypes"): {request_data}'
        return json_response({'status': 400, 'error': error})

    if 'tableName' in request_data:
        table_name = request_data.get('tableName')
        if table_name in ['cronjob_tasks', 'tasks']:
            if table_name == 'tasks':
                result = core.update_task(**row)
            elif table_name == 'cronjob_tasks':
                result = core.update_cronjob_task(**row)
            if isinstance(result, str):
                return json_response({'status': 400, 'error': result})
            else:
                return json_response({'status': 200, 'row': result})
        else:
            error = f'unknown request_data (not exists key "row" and "columnsTypes"): {request_data}'
            return json_response({'status': 400, 'error': error})
    else:
        error = f'unknown request_data (not exists key "tableName"): {request_data}'
        return json_response({'status': 400, 'error': error})
    # return jsonify({'result': 'ok'})

