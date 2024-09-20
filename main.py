import flask
import hashlib
import random
import os
import smtplib

application = flask.Flask("__name__")


def student():
    pass


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


def send_mail(code, to_addrs):
    from_addr = "noreply@xn--80adghmg3aabhlj7izc.xn--p1ai"
    lines = [f"From: {from_addr}", f"To: {', '.join(to_addrs)}",
             f"Your verification link is: https://xn--80adghmg3aabhlj7izc.xn--p1ai/verify/{code}"]
    msg = "\r\n".join(lines)
    smtp = smtplib.SMTP('mail.hosting.reg.ru', 587)
    smtp.set_debuglevel(False)
    smtp.connect('mail.hosting.reg.ru', 587)
    smtp.ehlo()
    smtp.login('noreply@xn--80adghmg3aabhlj7izc.xn--p1ai', 'AntonVolky2009*')
    smtp.sendmail(from_addr, to_addrs, msg)
    smtp.quit()


@application.route("/", methods=['POST', 'GET'])
def index():
    v = open("verified.txt", 'a+', encoding="utf-8")
    v.seek(0)
    vl = [line.strip() for line in v]
    v.close()
    if flask.request.cookies.get("key") is None:
        return flask.render_template("index.html")
    else:
        if flask.request.cookies.get("key") in vl:
            if len(str(flask.request.cookies.get("key"))) == 47:
                print("verified")
                if flask.request.method == "POST":
                    print("entered post")
                    t = open("trips.txt", "a+", encoding="utf8")
                    t.seek(0)
                    tl = [line.strip() for line in t]
                    print(flask.request.form.get("description"))
                    for i in range(0, len(tl), 6):
                        print("var", tl[i], "set to ---")
                        if flask.request.form.get("var" + tl[i]) == "1":
                            print("var", tl[i], "set to true")
                            with open("tripsStatus.txt", 'r') as file:
                                lines = file.readlines()
                                file.close()
                            print(lines)
                            lines[lines.index(str(tl[i]) + '\n') + 1] = str(lines[lines.index(tl[i] + '\n') + 1])[
                                                                        :-1] + " " + str(
                                flask.request.cookies.get("key")) + "\n"
                            with open("tripsStatus.txt", 'w') as file:
                                file.writelines(lines)
                                file.close()
                        if flask.request.form.get("var" + tl[i]) is None and tl[i].isnumeric() is True:
                            print("var", tl[i], "set to false")
                            with open("tripsStatus.txt", 'r') as file:
                                lines = file.readlines()
                                file.close()
                            print(lines[lines.index(str(tl[i]) + '\n') + 1])
                            if str(flask.request.cookies.get("key")) in lines[lines.index(str(tl[i]) + '\n') + 1]:
                                print("replace procedure initiated")
                                lines[lines.index(str(tl[i]) + '\n') + 1] = lines[
                                    lines.index(str(tl[i]) + '\n') + 1].replace(" " + str(flask.request.cookies.get("key")), '')
                            with open("tripsStatus.txt", 'w') as file:
                                file.writelines(lines)
                                file.close()
                    if flask.request.form.get("description") != '':
                        t.write("onReview" + '\n')
                        t.write(flask.request.form.get("location") + '\n')
                        t.write(flask.request.form.get("description") + '\n')
                        t.write(flask.request.form.get("class") + '\n')
                        t.write(flask.request.form.get("cost") + '\n')
                        t.write('На проверке\n')
                        with open("tripsStatus.txt", 'a+', encoding="utf-8") as file:
                            file.write("onReview\n")
                            file.write(str(flask.request.cookies.get("key")) + "\n")
                    return flask.redirect("/")
                else:
                    t = open("trips.txt", "a+", encoding="utf8")
                    t.seek(0)
                    tl = [line.strip() for line in t]
                    fl = list()
                    ts = open("tripsStatus.txt", "a+", encoding="utf8")
                    ts.seek(0)
                    tsl = [line.strip() for line in ts]
                    for i in range(0, len(tl), 6):
                        if tl[i] != "onReview":
                            fl.append(
                                {"location": tl[i + 1], "description": tl[i + 2], "class": tl[i + 3], "count": tl[i]})
                    key = flask.request.cookies.get("key")
                    fsd = {}
                    for i in range(1, len(tsl), 2):
                        if key in tsl[i]:
                            fsd[tsl[i - 1]] = True
                        else:
                            fsd[tsl[i - 1]] = False
                    t.close()
                    ts.close()
                    del key
                    print(fsd)
                    return flask.render_template("registered-teacher.html", fl=fl, fsd=fsd)
            else:
                print("verified")
                if flask.request.method == "POST":
                    print("entered post")
                    t = open("trips.txt", "a+", encoding="utf8")
                    t.seek(0)
                    tl = [line.strip() for line in t]
                    print(flask.request.form.get("description"))
                    for i in range(0, len(tl), 6):
                        print("var", tl[i], "set to ---")
                        if flask.request.form.get("var" + tl[i]) == "1":
                            print("var", tl[i], "set to true")
                            with open("tripsStatus.txt", 'r') as file:
                                lines = file.readlines()
                                file.close()
                            print(lines)
                            lines[lines.index(str(tl[i]) + '\n') + 1] = str(lines[lines.index(tl[i] + '\n') + 1])[
                                                                        :-1] + " " + str(
                                flask.request.cookies.get("key")) + "\n"
                            with open("tripsStatus.txt", 'w') as file:
                                file.writelines(lines)
                                file.close()
                        if flask.request.form.get("var" + tl[i]) is None and tl[i].isnumeric() is True:
                            print("var", tl[i], "set to false")
                            with open("tripsStatus.txt", 'r') as file:
                                lines = file.readlines()
                                file.close()
                            print(lines[lines.index(str(tl[i]) + '\n') + 1])
                            if str(flask.request.cookies.get("key")) in lines[lines.index(str(tl[i]) + '\n') + 1]:
                                print("replace procedure initiated")
                                lines[lines.index(str(tl[i]) + '\n') + 1] = lines[
                                    lines.index(str(tl[i]) + '\n') + 1].replace(" " + str(flask.request.cookies.get("key")), '')
                            with open("tripsStatus.txt", 'w') as file:
                                file.writelines(lines)
                                file.close()
                    if flask.request.form.get("description") != '':
                        t.write("onReview" + '\n')
                        t.write(flask.request.form.get("location") + '\n')
                        t.write(flask.request.form.get("description") + '\n')
                        t.write(flask.request.form.get("class") + '\n')
                        t.write(flask.request.form.get("cost") + '\n')
                        t.write('На проверке\n')
                        with open("tripsStatus.txt", 'a+', encoding="utf-8") as file:
                            file.write("onReview\n")
                            file.write(str(flask.request.cookies.get("key")) + "\n")
                    return flask.redirect("/")
                else:
                    t = open("trips.txt", "a+", encoding="utf8")
                    t.seek(0)
                    tl = [line.strip() for line in t]
                    fl = list()
                    ts = open("tripsStatus.txt", "a+", encoding="utf8")
                    ts.seek(0)
                    tsl = [line.strip() for line in ts]
                    for i in range(0, len(tl), 6):
                        if tl[i] != "onReview":
                            fl.append(
                                {"location": tl[i + 1], "description": tl[i + 2], "class": tl[i + 3], "count": tl[i],
                                 "cost": tl[i + 4]})
                    key = flask.request.cookies.get("key")
                    fsd = {}
                    for i in range(1, len(tsl), 2):
                        if key in tsl[i]:
                            fsd[tsl[i - 1]] = True
                        else:
                            fsd[tsl[i - 1]] = False
                    t.close()
                    ts.close()
                    del key
                    print(fsd)
                    return flask.render_template("registered.html", fl=fl, fsd=fsd)
        else:
            return flask.render_template("index.html")


@application.route("/trip/<path:path>/", methods=['POST', 'GET'])
def card(path):
    path = int(path)
    v = open("verified.txt", 'a+', encoding="utf-8")
    v.seek(0)
    vl = [line.strip() for line in v]
    v.close()
    if flask.request.cookies.get("key") is None:
        return flask.render_template("index.html")
    else:
        if flask.request.cookies.get("key") in vl:
            if len(str(flask.request.cookies.get("key"))) == 47:
                print("verified")
                if flask.request.method == "POST":
                    print("entered post")
                    t = open("trips.txt", "a+", encoding="utf8")
                    t.seek(0)
                    tl = [line.strip() for line in t]
                    print("var", str(path), "set to ---")
                    if flask.request.form.get("var" + str(path)) == "1":
                        print("var", str(path), "set to true")
                        with open("tripsStatus.txt", 'r') as file:
                            lines = file.readlines()
                            file.close()
                        print(lines)
                        lines[lines.index(str(path) + '\n') + 1] = str(lines[lines.index(str(path) + '\n') + 1])[
                                                                   :-1] + " " + str(
                            flask.request.cookies.get("key")) + "\n"
                        with open("tripsStatus.txt", 'w') as file:
                            file.writelines(lines)
                            file.close()
                    if flask.request.form.get("var" + str(path)) is None and str(path).isnumeric() is True:
                        print("var", str(path), "set to false")
                        with open("tripsStatus.txt", 'r') as file:
                            lines = file.readlines()
                            file.close()
                        print(lines[lines.index(str(path) + '\n') + 1])
                        if str(flask.request.cookies.get("key")) in lines[lines.index(str(path) + '\n') + 1]:
                            print("replace procedure initiated")
                            lines[lines.index(str(path) + '\n') + 1] = lines[lines.index(str(path) + '\n') + 1].replace(" " +
                                str(flask.request.cookies.get("key")), '')
                        with open("tripsStatus.txt", 'w') as file:
                            file.writelines(lines)
                            file.close()
                    return flask.redirect(f"/trip/{path}/")
                else:
                    t = open("trips.txt", "a+", encoding="utf8")
                    t.seek(0)
                    tl = [line.strip() for line in t]
                    fl = dict()
                    ts = open("tripsStatus.txt", "a+", encoding="utf8")
                    ts.seek(0)
                    tsl = [line.strip() for line in ts]
                    print(tl[(path - 1) * 6])
                    if tl[(path - 1) * 6] != "onReview":
                        fl = {"location": tl[(path - 1) * 6 + 1], "description": tl[(path - 1) * 6 + 2],
                              "class": tl[(path - 1) * 6 + 3], "cost": "0", "count": tl[(path - 1) * 6],
                              "state": tl[(path - 1) * 6 + 5]}
                        lcodes = tsl[tsl.index(str(path)) + 1].split()
                        l = list()
                        n = open("names.txt", "a+", encoding="utf8")
                        n.seek(0)
                        nl = [line.strip() for line in n]
                        v = open("verified.txt", "a+", encoding="utf8")
                        v.seek(0)
                        vl = [line.strip() for line in v]
                        print(vl)
                        for code in lcodes:
                            l.append(nl[vl.index(code)].replace("_", " "))
                            if len(code) == 47:
                                l[-1] += " - сопровождающий"
                    key = flask.request.cookies.get("key")
                    fsd = {}
                    for i in range(1, len(tsl), 2):
                        if key in tsl[i]:
                            fsd[tsl[i - 1]] = True
                        else:
                            fsd[tsl[i - 1]] = False
                    t.close()
                    ts.close()
                    n.close()
                    del key
                    print(fsd)
                    return flask.render_template("cards.html", fl=fl, fsd=fsd, path=str(path), l=l)
            else:
                print("verified")
                if flask.request.method == "POST":
                    print("entered post")
                    t = open("trips.txt", "a+", encoding="utf8")
                    t.seek(0)
                    tl = [line.strip() for line in t]
                    print("var", str(path), "set to ---")
                    if flask.request.form.get("var" + str(path)) == "1":
                        print("var", str(path), "set to true")
                        with open("tripsStatus.txt", 'r') as file:
                            lines = file.readlines()
                            file.close()
                        print(lines)
                        lines[lines.index(str(path) + '\n') + 1] = str(lines[lines.index(str(path) + '\n') + 1])[
                                                                   :-1] + " " + str(
                            flask.request.cookies.get("key")) + "\n"
                        with open("tripsStatus.txt", 'w') as file:
                            file.writelines(lines)
                            file.close()
                    if flask.request.form.get("var" + str(path)) is None and str(path).isnumeric() is True:
                        print("var", path, "set to false")
                        with open("tripsStatus.txt", 'r') as file:
                            lines = file.readlines()
                            file.close()
                        print(lines[lines.index(str(path) + '\n') + 1])
                        if str(flask.request.cookies.get("key")) in lines[lines.index(str(path) + '\n') + 1]:
                            print("replace procedure initiated")
                            lines[lines.index(str(path) + '\n') + 1] = lines[lines.index(str(path) + '\n') + 1].replace(" " +
                                str(flask.request.cookies.get("key")), '')
                        with open("tripsStatus.txt", 'w') as file:
                            file.writelines(lines)
                            file.close()
                    return flask.redirect(f"/trip/{path}/")
                else:
                    t = open("trips.txt", "a+", encoding="utf8")
                    t.seek(0)
                    tl = [line.strip() for line in t]
                    fl = dict()
                    ts = open("tripsStatus.txt", "a+", encoding="utf8")
                    ts.seek(0)
                    tsl = [line.strip() for line in ts]
                    print(tl[(path - 1) * 6])
                    if tl[(path - 1) * 6] != "onReview":
                        fl = {"location": tl[(path - 1) * 6 + 1], "description": tl[(path - 1) * 6 + 2],
                              "class": tl[(path - 1) * 6 + 3], "count": tl[(path - 1) * 6],
                              "cost": tl[(path - 1) * 6 + 4], "state": tl[(path - 1) * 6 + 5]}
                        lcodes = tsl[tsl.index(str(path)) + 1].split()
                        l = list()
                        n = open("names.txt", "a+", encoding="utf8")
                        n.seek(0)
                        nl = [line.strip() for line in n]
                        v = open("verified.txt", "a+", encoding="utf8")
                        v.seek(0)
                        vl = [line.strip() for line in v]
                        print(vl)
                        for code in lcodes:
                            l.append(nl[vl.index(code)].replace("_", " "))
                            if len(code) == 47:
                                l[-1] += " - сопровождающий"
                    key = flask.request.cookies.get("key")
                    fsd = {}
                    for i in range(1, len(tsl), 2):
                        if key in tsl[i]:
                            fsd[tsl[i - 1]] = True
                        else:
                            fsd[tsl[i - 1]] = False
                    t.close()
                    ts.close()
                    n.close()
                    del key
                    print(fsd)
                    return flask.render_template("cards.html", fl=fl, fsd=fsd, path=str(path), l=l)
        else:
            return flask.render_template("index.html")


@application.route("/login/", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        p = open("passwds.txt", 'a+', encoding="utf-8")
        p.seek(0)
        pl = [line.strip() for line in p]
        u = open("users.txt", 'a+', encoding="utf-8")
        u.seek(0)
        ul = [line.strip() for line in u]
        v = open("verified.txt", 'a+', encoding="utf-8")
        v.seek(0)
        vl = [line.strip() for line in v]
        w = open("whitelisted.txt", 'a+', encoding="utf-8")
        w.seek(0)
        wl = [line.strip() for line in w]
        if flask.request.form.get("email") in ul:
            md5_hashl = hashlib.new('md5')
            md5_hashl.update(flask.request.form.get("passw").encode())
            print(md5_hashl.hexdigest())
            print(pl[ul.index(flask.request.form.get("email"))])
            print(wl)
            print(str(vl[ul.index(flask.request.form.get("email"))]))
            if md5_hashl.hexdigest() == pl[ul.index(flask.request.form.get("email"))] and str(
                    vl[ul.index(flask.request.form.get("email"))]) in wl:
                res = flask.redirect("/")
                res.set_cookie("key", str(vl[ul.index(flask.request.form.get("email"))]), 60 * 60 * 24 * 365 * 5)
                p.close()
                u.close()
                v.close()
                w.close()
                return res
            else:
                p.close()
                u.close()
                v.close()
                w.close()
                return flask.render_template("index.html", show={"show": 1})
        else:
            p.close()
            u.close()
            v.close()
            w.close()
            return flask.render_template("login.html")
    else:
        return flask.render_template("login.html")


@application.route("/reg/", methods=["POST", "GET"])
def register():
    if flask.request.method == "POST":
        p = open("passwds.txt", 'a+', encoding="utf-8")
        u = open("users.txt", 'a+', encoding="utf-8")
        u.seek(0)
        ul = [line.strip() for line in u]
        v = open("verified.txt", 'a+', encoding="utf-8")
        n = open("names.txt", 'a+', encoding="utf-8")
        if check_mail(flask.request.form.get("email"), flask.request.form.get("options")) and flask.request.form.get(
                "passw") == flask.request.form.get("passwrep"):
            if flask.request.form.get("email") in ul:
                return flask.render_template("register.html")
            if flask.request.form.get("options") == "god":
                verifylink = str(random.randint(10000000000000000000000000000000000000000000001,
                                                99999999999999999999999999999999999999999999999))
            else:
                verifylink = str(random.randint(100000000, 1000000000000000000000000000000000000000000000))
            send_mail(verifylink, flask.request.form.get("email"))
            md5_hashl = hashlib.new('md5')
            md5_hashl.update(verifylink.encode())
            md5_hashp = hashlib.new('md5')
            md5_hashp.update(flask.request.form.get("passw").encode())
            p.write(str(md5_hashp.hexdigest()) + '\n')
            u.write(str(flask.request.form.get("email") + '\n'))
            v.write(verifylink + '\n')
            n.write(str(flask.request.form.get("FIO1")) + "_" + str(flask.request.form.get("FIO2")) + "_" + str(
                flask.request.form.get("FIO3")) + '\n')
            n.close()
            v.close()
            u.close()
            p.close()
            return flask.render_template("index.html", show={"show": 1})
        else:
            n.close()
            v.close()
            u.close()
            p.close()
            return flask.render_template("register.html")
    else:
        return flask.render_template("register.html")


@application.route('/style/<path:path>')
def stylefiles(path):
    return flask.send_from_directory('style', path)


@application.route('/verify/<path:path>')
def verify(path):
    v = open("verified.txt", 'a+', encoding="utf-8")
    v.seek(0)
    vl = [line.strip() for line in v]
    if str(path) in vl:
        res = flask.redirect("/")
        res.set_cookie("key", str(path), 60 * 60 * 24 * 365 * 5)
        w = open("whitelisted.txt", 'a+', encoding="utf-8")
        w.write(str(path) + '\n')
        w.close()
        v.close()
        return res
    else:
        v.close()
        return 'Почта НЕ подтверждена! <a href="/">На главную</a>'


if __name__ == '__main__':
    application.run()
