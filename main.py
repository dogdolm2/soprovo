import flask
import hashlib
import random
import os
import smtplib
import documents
import db_op
from db_op import read_trips

application = flask.Flask("__name__")
const_enter = """
"""


def check_mail(email, state):
    if state == "god":
        if email[-7:] == "@hse.ru":
            return 1
        else:
            return 0
    else:
        if email[-11:] == "@edu.hse.ru":
            return 1
        else:
            return 0


def send_mail(code, to_addrs, from_addr):
    """lines = [f"From: {from_addr}", f"To: {', '.join(to_addrs)}",
             code]
    msg = "\r\n".join(lines)
    smtp = smtplib.SMTP('mail.hosting.reg.ru', 587)
    smtp.set_debuglevel(False)
    smtp.connect('mail.hosting.reg.ru', 587)
    smtp.ehlo()
    smtp.login(from_addr, 'AntonVolky2009*')
    smtp.sendmail(from_addr, to_addrs, msg)
    smtp.quit()"""


@application.route("/admin/", methods=['POST', 'GET'])
def admin():
    if flask.request.cookies.get("key") == "97905576762507071195365227107652262209004166140" or \
            flask.request.cookies.get("key") == "58341574981824171660262120297766530067860640204":
        if flask.request.method == "POST":
            print("entered post")
            l = read_trips()
            for i in range(1, len(l) + 1):
                print(l[i - 1][5], flask.request.form.get("state" + str(i)))
                if l[i - 1][5] != flask.request.form.get("state" + str(i)) and flask.request.form.get(
                        "state" + str(i)) is not None:
                    db_op.update_state(i, flask.request.form.get("state" + str(i)))
            if flask.request.form.get("description") != '':
                id = db_op.add_trip(flask.request.form.get("location"), flask.request.form.get("description"),
                                    flask.request.form.get("class"),
                                    flask.request.form.get("cost"), "На проверке",
                                    flask.request.form.get("quant"))
                db_op.add_participant(flask.request.cookies.get("key"), id)
            return flask.redirect("/admin/")
        else:
            tl = db_op.read_trips()
            fl = list()
            for i in range(len(tl)):
                desc = list()
                curline = ""
                for i1 in range(len(tl[i][2])):
                    if tl[i][2][i1] != const_enter:
                        curline += str(tl[i][2][i1])
                    else:
                        desc.append(curline)
                        curline = ""
                desc.append(curline)
                fl.append({"location": tl[i][1], "description": desc,
                           "class": tl[i][3], "count": tl[i][0],
                           "cost": tl[i][4], "state": tl[i][5], "quant": tl[i][6]})
            key = flask.request.cookies.get("key")
            fsd = {}
            tsl = db_op.get_trips_verifies()
            for i in range(len(tsl)):
                if key in tsl[i]:
                    fsd[i + 1] = True
                else:
                    fsd[i + 1] = False
            del key
            print(fsd)
            return flask.render_template("admin.html", fl=fl, fsd=fsd)


@application.route("/", methods=['POST', 'GET'])
def index():
    if flask.request.cookies.get("key") is None:
        return flask.render_template("index.html")
    else:
        print(flask.request.cookies.get("key"))
        if db_op.check_whitelisting(flask.request.cookies.get("key")):
            if len(str(flask.request.cookies.get("key"))) == 47:
                print("verified")
                if flask.request.method == "POST":
                    print("entered post")
                    if flask.request.form.get("description") != '':
                        id = db_op.add_trip(flask.request.form.get("location"), flask.request.form.get("description"),
                                            flask.request.form.get("class"),
                                            flask.request.form.get("cost"), "На проверке",
                                            flask.request.form.get("quant"))
                        db_op.add_participant(flask.request.cookies.get("key"), id)
                    return flask.redirect("/")
                else:
                    tl = db_op.read_trips()
                    fl = list()
                    for i in range(len(tl)):
                        if tl[i][5] != "На проверке":
                            desc = list()
                            curline = ""
                            for i1 in range(len(tl[i][2])):
                                if tl[i][2][i1] != const_enter:
                                    curline += str(tl[i][2][i1])
                                else:
                                    desc.append(curline)
                                    curline = ""
                            desc.append(curline)
                            fl.append({"location": tl[i][1], "description": desc,
                                       "class": tl[i][3], "count": tl[i][0],
                                       "cost": 0, "state": tl[i][5], "quant": tl[i][6]})
                    key = flask.request.cookies.get("key")
                    fsd = {}
                    tsl = db_op.get_trips_verifies()
                    for i in range(len(tsl)):
                        if key in tsl[i]:
                            fsd[i + 1] = True
                        else:
                            fsd[i + 1] = False
                    del key
                    print(fsd)
                    return flask.render_template("registered.html", fl=fl, fsd=fsd)
            else:
                print("verified")
                if flask.request.method == "POST":
                    print("entered post")
                    if flask.request.form.get("description") != '':
                        id = db_op.add_trip(flask.request.form.get("location"), flask.request.form.get("description"),
                                            flask.request.form.get("class"),
                                            flask.request.form.get("cost"), "На проверке",
                                            flask.request.form.get("quant"))
                        db_op.add_participant(flask.request.cookies.get("key"), id)
                    return flask.redirect("/")
                else:
                    tl = db_op.read_trips()
                    fl = list()
                    for i in range(len(tl)):
                        if tl[i][5] != "На проверке":
                            desc = list()
                            curline = ""
                            for i1 in range(len(tl[i][2])):
                                if tl[i][2][i1] != const_enter:
                                    curline += str(tl[i][2][i1])
                                else:
                                    desc.append(curline)
                                    curline = ""
                            desc.append(curline)
                            fl.append({"location": tl[i][1], "description": desc,
                                       "class": tl[i][3], "count": tl[i][0],
                                       "cost": tl[i][4], "state": tl[i][5], "quant": tl[i][6]})
                    key = flask.request.cookies.get("key")
                    fsd = {}
                    tsl = db_op.get_trips_verifies()
                    for i in range(len(tsl)):
                        if key in tsl[i]:
                            fsd[i + 1] = True
                        else:
                            fsd[i + 1] = False
                    del key
                    print(fsd)
                    return flask.render_template("registered.html", fl=fl, fsd=fsd)
        else:
            return flask.render_template("index.html")


@application.route("/clear/")
def clear():
    if flask.request.cookies.get("key") is None:
        return flask.render_template("index.html")
    else:
        print(flask.request.cookies.get("key"))
        if db_op.check_whitelisting(flask.request.cookies.get("key")):
            if len(str(flask.request.cookies.get("key"))) == 47:
                print("verified")
                tl = db_op.read_trips()
                fl = list()
                for i in range(len(tl)):
                    if tl[i][5] != "На проверке":
                        desc = list()
                        curline = ""
                        for i1 in range(len(tl[i][2])):
                            if tl[i][2][i1] != const_enter:
                                curline += str(tl[i][2][i1])
                            else:
                                desc.append(curline)
                                curline = ""
                        desc.append(curline)
                        fl.append({"location": tl[i][1], "description": desc,
                                   "class": tl[i][3], "count": tl[i][0],
                                   "cost": 0, "state": tl[i][5], "quant": tl[i][6]})
                key = flask.request.cookies.get("key")
                fsd = {}
                tsl = db_op.get_trips_verifies()
                for i in range(len(tsl)):
                    if key in tsl[i]:
                        fsd[i + 1] = True
                    else:
                        fsd[i + 1] = False
                del key
                print(fsd)
                return flask.render_template("clear.html", fl=fl, fsd=fsd)
            else:
                print("verified")
                tl = db_op.read_trips()
                fl = list()
                for i in range(len(tl)):
                    if tl[i][5] != "На проверке":
                        desc = list()
                        curline = ""
                        for i1 in range(len(tl[i][2])):
                            if tl[i][2][i1] != const_enter:
                                curline += str(tl[i][2][i1])
                            else:
                                desc.append(curline)
                                curline = ""
                        desc.append(curline)
                        fl.append({"location": tl[i][1], "description": desc,
                                   "class": tl[i][3], "count": tl[i][0],
                                   "cost": tl[i][4], "state": tl[i][5], "quant": tl[i][6]})
                key = flask.request.cookies.get("key")
                fsd = {}
                tsl = db_op.get_trips_verifies()
                for i in range(len(tsl)):
                    if key in tsl[i]:
                        fsd[i + 1] = True
                    else:
                        fsd[i + 1] = False
                del key
                print(fsd)
                return flask.render_template("clear.html", fl=fl, fsd=fsd)
        else:
            return flask.render_template("index.html")


@application.route("/trip/<path:path>/", methods=['POST', 'GET'])
def card(path):
    if flask.request.cookies.get("key") is None:
        return flask.render_template("index.html")
    else:
        if db_op.check_whitelisting(flask.request.cookies.get("key")):
            if len(str(flask.request.cookies.get("key"))) == 47:
                print("verified")
                if flask.request.method == "POST":
                    print("entered post")
                    if flask.request.form.get("var" + str(path)) == "1":
                        print("var", str(path), "set to true")
                        if str(flask.request.cookies.get("key")) not in db_op.read_trip_participants(path):
                            db_op.add_participant(flask.request.cookies.get("key"), path)
                        tl = db_op.read_trips()[int(path) - 1]
                        desc = list()
                        curline = ""
                        for i1 in range(len(tl[2])):
                            if tl[2][i1] != const_enter:
                                curline += tl[2][i1]
                            else:
                                desc.append(curline)
                                curline = ""
                        desc.append(curline)
                        fl = {"location": tl[1], "description": desc,
                              "class": tl[3], "count": tl[0],
                              "cost": 0, "state": tl[5], "quant": tl[6]}
                        if len(db_op.read_trip_participants(path)) > int(tl[6]):
                            send_mail(
                                "You need to reach agreement with " + db_op.read_trip_participants(path)[
                                    0] + " on letting " +
                                db_op.read_trip_participants(path)[
                                    len(db_op.read_trip_participants(path)) - 1] + " join trip #" + str(path),
                                "administrative_director@xn--80adghmg3aabhlj7izc.xn--p1ai",
                                "generalniy_director@xn--80adghmg3aabhlj7izc.xn--p1ai")
                    if flask.request.form.get("var" + str(path)) is None and str(path).isnumeric() is True:
                        print("var", str(path), "set to false")
                        db_op.delete_participant(flask.request.cookies.get("key"), path)
                    return flask.redirect(f"/trip/{path}/")
                else:
                    tsl = db_op.read_trip_participants(path)
                    tl = db_op.read_trips()[int(path) - 1]
                    desc = list()
                    curline = ""
                    for i1 in range(len(tl[2])):
                        if tl[2][i1] != const_enter:
                            curline += tl[2][i1]
                        else:
                            desc.append(curline)
                            curline = ""
                    desc.append(curline)
                    fl = {"location": tl[1], "description": desc,
                          "class": tl[3], "count": tl[0],
                          "cost": 0, "state": tl[5], "quant": int(tl[6])}
                    lcodes = db_op.read_trip_participants(path)
                    l = list()
                    actual_quant = len(lcodes) - 1
                    if int(fl["quant"]) <= actual_quant:
                        fl["state"] = "Участники набраны"
                    for i in range(len(lcodes)):
                        cur_user = db_op.get_user_data(verify_number=lcodes[i])
                        l.append(str(cur_user[5] + " " + cur_user[6] + " " + cur_user[7]))
                        if len(lcodes[i]) == 47:
                            l[-1] += " - сопровождающий"
                    key = flask.request.cookies.get("key")
                    fsd = {}
                    for i in range(len(tsl)):
                        if key == tsl[i]:
                            fsd[path] = True
                        else:
                            fsd[path] = False
                    del key
                    print(fsd)
                    return flask.render_template("cards.html", fl=fl, fsd=fsd, path=str(path), l=l, ac=actual_quant)
            else:
                print("verified")
                if flask.request.method == "POST":
                    print("entered post")
                    if flask.request.form.get("var" + str(path)) == "1":
                        print("var", str(path), "set to true")
                        if str(flask.request.cookies.get("key")) not in db_op.read_trip_participants(path):
                            db_op.add_participant(flask.request.cookies.get("key"), path)
                        tl = db_op.read_trips()[int(path) - 1]
                        desc = list()
                        curline = ""
                        for i1 in range(len(tl[2])):
                            if tl[2][i1] != const_enter:
                                curline += tl[2][i1]
                            else:
                                desc.append(curline)
                                curline = ""
                        desc.append(curline)
                        fl = {"location": tl[1], "description": desc,
                              "class": tl[3], "count": tl[0],
                              "cost": tl[4], "state": tl[5], "quant": tl[6]}
                        if len(db_op.read_trip_participants(path)) > int(tl[6]):
                            send_mail(
                                "You need to reach agreement with " + db_op.read_trip_participants(path)[
                                    0] + " on letting " +
                                db_op.read_trip_participants(path)[
                                    len(db_op.read_trip_participants(path)) - 1] + " join trip #" + str(path),
                                "administrative_director@xn--80adghmg3aabhlj7izc.xn--p1ai",
                                "generalniy_director@xn--80adghmg3aabhlj7izc.xn--p1ai")
                    if flask.request.form.get("var" + str(path)) is None and str(path).isnumeric() is True:
                        print("var", str(path), "set to false")
                        db_op.delete_participant(flask.request.cookies.get("key"), path)
                    return flask.redirect(f"/trip/{path}/")
                else:
                    tsl = db_op.read_trip_participants(path)
                    tl = db_op.read_trips()[int(path) - 1]
                    desc = list()
                    curline = ""
                    for i1 in range(len(tl[2])):
                        if tl[2][i1] != const_enter:
                            curline += tl[2][i1]
                        else:
                            desc.append(curline)
                            curline = ""
                    desc.append(curline)
                    fl = {"location": tl[1], "description": desc,
                          "class": tl[3], "count": tl[0],
                          "cost": tl[4], "state": tl[5], "quant": int(tl[6])}
                    lcodes = db_op.read_trip_participants(path)
                    l = list()
                    actual_quant = len(lcodes) - 1
                    if int(fl["quant"]) <= actual_quant:
                        fl["state"] = "Участники набраны"
                    for i in range(len(lcodes)):
                        cur_user = db_op.get_user_data(verify_number=lcodes[i])
                        l.append(str(cur_user[5] + " " + cur_user[6] + " " + cur_user[7]))
                        if len(lcodes[i]) == 47:
                            l[-1] += " - сопровождающий"
                    key = flask.request.cookies.get("key")
                    fsd = {}
                    for i in range(len(tsl)):
                        if key == tsl[i]:
                            fsd[path] = True
                        else:
                            fsd[path] = False
                    del key
                    print(fsd)
                    return flask.render_template("cards.html", fl=fl, fsd=fsd, path=str(path), l=l, ac=actual_quant)
        else:
            return flask.render_template("index.html")


@application.route("/preview/<path:path>/")
def preview(path):
    tsl = db_op.read_trip_participants(path)
    tl = db_op.read_trips()[int(path) - 1]
    desc = list()
    curline = ""
    for i1 in range(len(tl[2])):
        if tl[2][i1] != const_enter:
            curline += tl[2][i1]
        else:
            desc.append(curline)
            curline = ""
    desc.append(curline)
    fl = {"location": tl[1], "description": desc,
          "class": tl[3], "count": tl[0],
          "cost": 0, "state": tl[5], "quant": int(tl[6])}
    lcodes = db_op.read_trip_participants(path)
    l = list()
    actual_quant = len(lcodes) - 1
    if int(fl["quant"]) <= actual_quant:
        fl["state"] = "Участники набраны"
    for i in range(len(lcodes)):
        cur_user = db_op.get_user_data(verify_number=lcodes[i])
        l.append(str(cur_user[5] + " " + cur_user[6] + " " + cur_user[7]))
        if len(lcodes[i]) == 47:
            l[-1] += " - сопровождающий"
    key = flask.request.cookies.get("key")
    fsd = {}
    for i in range(len(tsl)):
        if key == tsl[i]:
            fsd[path] = True
        else:
            fsd[path] = False
    del key
    print(fsd)
    return flask.render_template("preview.html", fl=fl, fsd=fsd, path=str(path), l=l, ac=actual_quant)


@application.route("/login/", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        fulll = db_op.read_users()
        ul = list()
        pl = list()
        for i in range(len(fulll)):
            ul.append(fulll[i][2])
            pl.append(fulll[i][3])
        print(pl, ul)
        if flask.request.form.get("email") in ul:
            md5_hashl = hashlib.new('md5')
            md5_hashl.update(flask.request.form.get("passw").encode())
            print(md5_hashl.hexdigest())
            if md5_hashl.hexdigest() == pl[ul.index(flask.request.form.get("email"))] and db_op.check_whitelisting(
                    fulll[ul.index(flask.request.form.get("email"))][1]):
                res = flask.redirect("/")
                res.set_cookie("key", str(fulll[ul.index(flask.request.form.get("email"))][1]), 60 * 60 * 24 * 365 * 5)
                return res
            else:
                return flask.render_template("index.html", show={"show": 1})
        else:
            return flask.render_template("login.html")
    else:
        return flask.render_template("login.html")


@application.route("/reg/", methods=["POST", "GET"])
def register():
    if flask.request.method == "POST":
        if check_mail(flask.request.form.get("email"), flask.request.form.get("options")) and flask.request.form.get(
                "passw") == flask.request.form.get("passwrep"):
            fulll = db_op.read_users()
            ul = list()
            pl = list()
            for i in range(len(fulll)):
                ul.append(fulll[i][2])
                pl.append(fulll[i][3])
            if flask.request.form.get("email") in ul:
                return flask.render_template("register.html")
            if flask.request.form.get("options") == "god":
                verifylink = str(random.randint(10000000000000000000000000000000000000000000001,
                                                99999999999999999999999999999999999999999999999))
            else:
                verifylink = str(random.randint(100000000, 1000000000000000000000000000000000000000000000))
            send_mail(
                "Your verification code link is https://xn--80adghmg3aabhlj7izc.xn--p1ai/verify/" + str(verifylink),
                flask.request.form.get("email"),
                "noreply@xn--80adghmg3aabhlj7izc.xn--p1ai")  # temp bypassed in function
            md5_hashl = hashlib.new('md5')
            md5_hashl.update(verifylink.encode())
            md5_hashp = hashlib.new('md5')
            md5_hashp.update(flask.request.form.get("passw").encode())
            db_op.add_user(flask.request.form.get("email"), flask.request.form.get("FIO1"),
                           flask.request.form.get("FIO2"), flask.request.form.get("FIO3"), md5_hashp.hexdigest(),
                           verifylink)
            return flask.render_template("index.html", show={"show": 1})
        else:
            return flask.render_template("register.html")
    else:
        return flask.render_template("register.html")


@application.route('/style/<path:path>')
def stylefiles(path):
    return flask.send_from_directory('../../soprovo-experimental/soprovo-experimental/style', path)


@application.route('/clearcookie/')
def clearcookie():
    res = flask.redirect("/")
    res.delete_cookie("key")
    return res


@application.route('/money/')
def money():
    return flask.render_template("money.html")


@application.route('/verify/<path:path>/')
def verify(path):
    vl = db_op.read_users_verify_number()
    if str(path) in vl:
        res = flask.redirect("/")
        res.set_cookie("key", str(path), 60 * 60 * 24 * 365 * 5)
        db_op.check_whitelisting(path)
        return res
    else:
        return 'Почта НЕ подтверждена! <a href="/">На главную</a>'


@application.route('/contacts/')
def contacts():
    return flask.render_template("contacts.html")


@application.route('/documents/<path:path>/')
def document_files(path):
    lcodes = db_op.read_trip_participants(path)
    tempf = open("temp.txt", "w", encoding="utf-8")
    wl = ["Фамилия,Имя,Отчество,Электронная Почта,\n"]
    for i in range(len(lcodes)):
        curuser = db_op.get_user_data(verify_number=lcodes[i])
        wl.append(curuser[5] + "," + curuser[6] + "," + curuser[7] + "," + curuser[2] + "\n")
    tempf.writelines(wl)
    tempf.close()
    documents.generateSpravka(len(wl) - 1, path)
    return flask.send_file("output.pdf")


@application.route('/documents_admin/<path:path>/')
def document_admin_files(path):
    lcodes = db_op.read_trip_participants(path)
    tempf = open("temp.txt", "w", encoding="utf-8")
    wl = ["Фамилия,Имя,Отчество,Электронная Почта,\n"]
    for i in range(len(lcodes)):
        curuser = db_op.get_user_data(verify_number=lcodes[i])
        wl.append(curuser[5] + "," + curuser[6] + "," + curuser[7] + "," + curuser[2] + "\n")
    tempf.writelines(wl)
    tempf.close()
    documents.generateAdminSpravka(len(wl) - 1, path)
    return flask.send_file("output.pdf")


@application.route('/raw/<path:path>/')
def raw_files(path):
    lcodes = db_op.read_trip_participants(path)
    tempf = open("output.csv", "w", encoding="utf-8")
    wl = ["Фамилия,Имя,Отчество,Электронная Почта,\n"]
    for i in range(len(lcodes)):
        curuser = db_op.get_user_data(verify_number=lcodes[i])
        wl.append(curuser[5] + "," + curuser[6] + "," + curuser[7] + "," + curuser[2] + "\n")
    tempf.writelines(wl)
    tempf.close()
    return flask.send_file("output.csv", as_attachment=True)


if __name__ == '__main__':
    application.run()
