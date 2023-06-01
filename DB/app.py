import hashlib
import os
import datetime
from main import rezult_test_lic
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, string
from flask import Flask, render_template, request, session, url_for, redirect, abort, jsonify
from base import residents, residents_search, residents_upset, residents_input, rooms_selctor, residents_selctor, \
    equipments_selctor, contract_input, contract_equipment_input, contract_room_input, contract_search, contracts, \
    contracts_search, room_upset, equipment, equipment_search, equipment_upset, type_reference, reference_input, \
    reference, disciplinary_input, disciplinary, reference_search, disciplinary_search, file_create, \
    contract_equipment_prov, residents_search_min,rooms_name
from werkzeug.utils import secure_filename
from mail import send_mail, send_password_reset_mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fsa87asd782asd'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


href_intr = ["../static/css/trade_intr.css", "../static/css/profile_intr.css", "../static/css/style_intr.css",
             "../static/css/reset_intr.css", "../static/css/courses_intr.css", "../static/css/account_styl_intr.css",
             "../static/css/header_intr.css", "intr", "../static/css/course_intr.css", "../static/css/table_intr.css"]


@app.route('/', methods=['GET', 'POST'])
def base():
    if request.method == "GET":
        return render_template('Home.html', title="Список проживающих",
                               href=href_intr,
                               navig=["Список проживающих"],
                               count_res=len(residents()),
                               data=residents())
    if request.method == "POST":

        if "search__input" in request.form:
            return render_template('Home.html', title="Список проживающих",
                                   href=href_intr,
                                   navig=["Список проживающих"],
                                   count_res=len(residents_search(request.form["search__input"])),
                                   data=residents_search(request.form["search__input"]))
        else:
            s = {}
            for i in request.form:
                if i.split("/")[1] in s:
                    s[i.split("/")[1]] += [request.form[i]]
                else:
                    s[i.split("/")[1]] = [request.form[i]]
            print(request.form)
            print(s)
            residents_upset(s)
        return render_template('Home.html', title="Список проживающих",
                               href=href_intr,
                               navig=["Список проживающих"],
                               count_res=len(residents()),
                               data=residents())


@app.route('/new_rez', methods=['GET', 'POST'])
def new_rez():
    if request.method == "GET":
        return render_template('new_rez.html', title="Добавить проживающего",
                               href=href_intr,
                               navig=["Добавить проживающего"], rooms=rooms_selctor())
    if request.method == "POST":
        print(request.form)
        if request.form["floor"] == "М":
            p = 1
        else:
            p = 0
        if (residents_input(list(
                (request.form["name"], request.form["surname"], request.form["fatherland"], request.form["phone"],
                 request.form["group"], p, request.form["date"], 0)))) == 1:
            print("saasdsa", residents_search(request.form["name"]))
            id_rez = residents_search_min(request.form["name"])[-1][0]
            name = request.form["name"] + request.form["surname"] + request.form["fatherland"]
            name_room=rooms_name(request.form["rooms"])
            s = string(request.form["date"] + request.form["rooms"], str(name_room[0])+name_room[1]+name_room[2], datetime.datetime.now().day,
                       datetime.datetime.now().month, datetime.datetime.now().year, name, request.form["group"])
            file_create(s, request.form["date"] + request.form["rooms"])
            """Файлы создаются дальше нужно инфу по договору заполнить"""
            contract_input([id_rez, request.form["date"] + request.form["rooms"],
                            request.form["date"] + request.form["rooms"] + ".pdf", datetime.date.today(), 0])
            id = contract_search(id_rez)[0][-1]
            contract_room_input([id, request.form["rooms"], datetime.date.today(), 0])
            return redirect(url_for("base"))
        return render_template('new_rez.html', title="Добавить проживающего",
                               href=href_intr,
                               navig=["Добавить проживающего"], rooms=rooms_selctor(),error="Проживающий уже существует")


@app.route('/new_contract', methods=['GET', 'POST'])
def new_contract():
    if request.method == "GET":
        return render_template('new_contract.html', title="Добавить договор",
                               href=href_intr,
                               navig=["Добавить договор"], rooms=rooms_selctor(), contract=residents_selctor(),
                               equipments=equipments_selctor())
    if request.method == "POST":
        print(request.form)
        print(request.files)
        id = request.form["contract"]
        for i in request.form:
            if "checkbox" in i:
                if len(contract_equipment_prov(id, i.split("/")[1])) == 0:
                    contract_equipment_input([id, i.split("/")[1], datetime.date.today(), 0])

        return redirect(url_for("equipment_table"))


@app.route('/contracts', methods=['GET', 'POST'])
def contracts_table():
    if request.method == "GET":
        return render_template('contracts.html', title="Список договоров",
                               href=href_intr,
                               navig=["Список договоров"],
                               count_res=len(contracts()),
                               data=contracts(),
                               resid=residents_selctor())
    if request.method == "POST":

        if "search__input" in request.form:
            return render_template('contracts.html', title="Список договоров",
                                   href=href_intr,
                                   navig=["Список договоров"],
                                   count_res=len(contracts_search(request.form["search__input"])),
                                   data=contracts_search(request.form["search__input"]))
        else:
            s = {}
            for i in request.form:
                s[i.split("/")[1]] = 0
                if "elder" in i:
                    s[i.split("/")[1]] = 1
            print(request.form)
            print(s)
            room_upset(s)
        return render_template('contracts.html', title="Список договоров",
                               href=href_intr,
                               navig=["Список договоров"],
                               count_res=len(contracts()),
                               data=contracts())


@app.route('/equipment', methods=['GET', 'POST'])
def equipment_table():
    if request.method == "GET":
        return render_template('equipm.html', title="Список оборудования",
                               href=href_intr,
                               navig=["Список оборудования"],
                               count_res=len(equipment()),
                               data=equipment(),
                               resid=residents_selctor())
    if request.method == "POST":

        if "search__input" in request.form:
            return render_template('equipm.html', title="Список оборудования",
                                   href=href_intr,
                                   navig=["Список оборудования"],
                                   count_res=len(equipment_search(request.form["search__input"])),
                                   data=equipment_search(request.form["search__input"]))
        else:
            s = {}
            for i in request.form:
                s[i.split("/")[1]] = 0
                if "elder" in i:
                    s[i.split("/")[1]] = 1
            print(request.form)
            print(s)
            equipment_upset(s)
        return render_template('equipm.html', title="Список оборудования",
                               href=href_intr,
                               navig=["Список оборудования"],
                               count_res=len(equipment()),
                               data=equipment())


@app.route('/new_reference', methods=['GET', 'POST'])
def new_reference():
    if request.method == "GET":
        return render_template('new_reference.html', title="Добавить справку",
                               href=href_intr,
                               navig=["Добавить справку"], reference=type_reference(), resid=residents())
    if request.method == "POST":
        print(request.form)
        print(request.files)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   request.form["resident"] + "-" + request.form["reference"] + "." +
                                   filename.split(".")[-1]))
            reference_input([request.form["resident"], request.form["reference"],
                             request.form["resident"] + "-" + request.form["reference"] + "." + filename.split(".")[-1],
                             datetime.date.today()])
        return redirect(url_for("references"))


@app.route('/reference', methods=['GET', 'POST'])
def references():
    if request.method == "GET":
        return render_template('reference.html', title="Список справок",
                               href=href_intr,
                               navig=["Список справок"],
                               count_res=len(reference()),
                               data=reference(),
                               resid=residents_selctor())
    if request.method == "POST":

        if "search__input" in request.form:
            return render_template('reference.html', title="Список справок",
                                   href=href_intr,
                                   navig=["Список справок"],
                                   count_res=len(reference_search(request.form["search__input"])),
                                   data=reference_search(request.form["search__input"]))
        else:
            s = {}
            for i in request.form:
                s[i.split("/")[1]] = 0
                if "elder" in i:
                    s[i.split("/")[1]] = 1
            print(request.form)
            print(s)
            equipment_upset(s)
        return render_template('reference.html', title="Список справок",
                               href=href_intr,
                               navig=["Список справок"],
                               count_res=len(reference()),
                               data=reference())


@app.route('/new_disciplinary', methods=['GET', 'POST'])
def new_disciplinary():
    if request.method == "GET":
        return render_template('new_disciplinary.html', title="Добавить дисциплинарку",
                               href=href_intr,
                               navig=["Добавить дисциплинарку"], resid=residents())
    if request.method == "POST":
        print(request.form)
        disciplinary_input([request.form["resident"], request.form["reason"], datetime.date.today()])
        return redirect(url_for("disciplinarys"))


@app.route('/disciplinary', methods=['GET', 'POST'])
def disciplinarys():
    if request.method == "GET":
        return render_template('disciplinary.html', title="Список дисциплинарок",
                               href=href_intr,
                               navig=["Список дисциплинарок"],
                               count_res=len(disciplinary()),
                               data=disciplinary(),
                               resid=residents_selctor())
    if request.method == "POST":

        if "search__input" in request.form:
            return render_template('disciplinary.html', title="Список дисциплинарок",
                                   href=href_intr,
                                   navig=["Список дисциплинарок"],
                                   count_res=len(disciplinary_search(request.form["search__input"])),
                                   data=disciplinary_search(request.form["search__input"]))
        else:
            s = {}
            for i in request.form:
                s[i.split("/")[1]] = 0
                if "elder" in i:
                    s[i.split("/")[1]] = 1
            print(request.form)
            print(s)
            equipment_upset(s)
        return render_template('disciplinary.html', title="Список дисциплинарок",
                               href=href_intr,
                               navig=["Список дисциплинарок"],
                               count_res=len(disciplinary()),
                               data=disciplinary())


if __name__ == '__main__':
    app.run(debug=True)
