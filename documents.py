import csv
import datetime
from fpdf import FPDF


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.cell(0, 10, f"Страница {self.page_no()}/{{nb}}", align="C")

    def improved_table(self, headings, rows, col_widths=(35, 35, 50, 70)):
        self.set_font('DejaVu', size=11)
        self.cell(190, 10, "Приложение №1 справки формы №027С", align="R")
        self.ln(5)
        self.cell(190, 10, "Выписка из базы данных", align="R")
        self.ln(20)
        self.set_font('DejaVu', size=9)
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 7, heading, border=1, align="C")
        self.ln()
        for row in rows:
            self.cell(col_widths[0], 6, row[0], border="LRTB")
            self.cell(col_widths[1], 6, row[1], border="LRTB")
            self.cell(col_widths[2], 6, row[2], border="LRTB")
            self.cell(col_widths[3], 6, row[3], border="LRTB", align="R")
            self.ln()
        self.cell(sum(col_widths), 0, "", border="T")


def load_data_from_csv(csv_filepath):
    headings, rows = [], []
    with open(csv_filepath, encoding="utf8") as csv_file:
        for row in csv.reader(csv_file, delimiter=","):
            if not headings:  # извлечение имен столбцов из первой строки:
                headings = row
            else:
                rows.append(row)
    return headings, rows


def generateAdminSpravka(count, id, filename="temp.txt"):
    col_names, data = load_data_from_csv(filename)
    pdf = PDF()
    pdf.add_font('DejaVu', fname='style/moscowsansregular.ttf')
    pdf.set_font('DejaVu', size=11)
    pdf.add_page()
    current_time = datetime.datetime.now()
    pdf.multi_cell(190, 8, str(str(current_time.day) + "." + str(current_time.month) + "."
                               + str(current_time.year)),
                   align="L")
    pdf.ln(30)
    pdf.set_font('DejaVu', size=20)
    pdf.multi_cell(190, 8, "Справка о поездке №_____________ формы №027С", align="C")
    pdf.ln(30)
    pdf.set_font('DejaVu', size=11)
    pdf.multi_cell(190, 8, "Справка предоставляется по месту требования.")
    pdf.ln(1)
    pdf.multi_cell(190, 8,
                   str("Данная справка подтверждает наличие на интернет ресурсе по адресу сопровождающий.рф,"
                       " находящемся в информационно-телекоммуникационной сети Интернет (далее - сайт) записей"
                       " на соответствующую экскурсию, поездку или мероприятие (далее - мероприятие) от пользователей,"
                       " соответствующий список которых представлен в таблице приложения №1 непосредственно данной"
                       " справки."
                       " Все пользователи данного сайта подтверждены с использованием корпоративной почты ФГАОУВО НИУ"
                       " ВШЭ, соответствующие записи также представлены в приложении №1."
                       " Сведений о добровольности записи и о действительности мероприятия сайт не имеет и не"
                       " предоставляет. Справка действительна в течение 3 суток после даты выдачи, указанной"
                       " непосредственно в справке."))
    pdf.ln(1)
    pdf.multi_cell(190, 8,
                   str("Таблица приложения №1 состоит из {count} записей/записи. Данная справка соответствует"
                       " мероприятию №{id}, размещенному на сайте, просмотр мероприятия доступен по ссылке"
                       " https://сопровождающий.рф/preview/{id} и"
                       " soprovozhdayushiy.pythonanywhere.com/preview/{id}.").format(id=id, count=count))
    pdf.ln(30)
    pdf.multi_cell(190, 4, "сопровождающий.рф - Отдел справок, внешних операций      ", align="R")
    pdf.ln(1)
    pdf.multi_cell(190, 4, "и коммуникаций      ", align="R")
    pdf.ln(13)
    pdf.multi_cell(190, 8, "М.П.                         ", align="R")
    pdf.add_page()
    pdf.improved_table(col_names, data)
    pdf.output("output.pdf")


def generateSpravka(count, id, filename="temp.txt"):
    col_names, data = load_data_from_csv(filename)
    pdf = PDF()
    pdf.add_font('DejaVu', fname='style/moscowsansregular.ttf')
    pdf.set_font('DejaVu', size=11)
    pdf.add_page()
    current_time = datetime.datetime.now()
    pdf.multi_cell(190, 8, str(str(current_time.day) + "." + str(current_time.month) + "."
                               + str(current_time.year)),
                   align="L")
    pdf.ln(30)
    pdf.set_font('DejaVu', size=22)
    pdf.multi_cell(190, 8, "Справка о поездке формы №027С", align="C")
    pdf.ln(30)
    pdf.set_font('DejaVu', size=11)
    pdf.multi_cell(190, 8, "Справка предоставляется по месту требования.")
    pdf.ln(1)
    pdf.multi_cell(190, 8,
                   str("Данная справка подтверждает наличие на интернет ресурсе по адресу сопровождающий.рф,"
                       " находящемся в информационно-телекоммуникационной сети Интернет (далее - сайт) записей"
                       " на соответствующую экскурсию, поездку или мероприятие (далее - мероприятие) от пользователей,"
                       " соответствующий список которых представлен в таблице приложения №1 непосредственно"
                       " данной справки."
                       " Все пользователи данного сайта подтверждены с использованием корпоративной почты ФГАОУВО НИУ"
                       " ВШЭ, соответствующие записи также представлены в приложении №1."
                       " Сведений о добровольности записи и о действительности мероприятия сайт не имеет и не"
                       " предоставляет. Справка действительна в течение 3 суток после даты выдачи, указанной"
                       " непосредственно в справке. Бумажная справка выдается по дополнительному запросу на"
                       " электронную почту generalniy_director@сопровождающий.рф."))
    pdf.ln(1)
    pdf.multi_cell(190, 8,
                   str("Таблица приложения №1 состоит из {count} записей/записи. Данная справка соответствует"
                       " мероприятию №{id}, размещенному на сайте, просмотр мероприятия доступен по ссылке"
                       " https://сопровождающий.рф/preview/{id} и soprovozhdayushiy.pythonanywhere.com/preview/{id}"
                       " дополнительные сведения могут быть"
                       " изложены только в бумажной справке.").format(id=id, count=count))
    pdf.ln(30)
    pdf.multi_cell(190, 4, "сопровождающий.рф - Отдел справок, внешних операций      ", align="R")
    pdf.ln(1)
    pdf.multi_cell(190, 4, "и коммуникаций      ", align="R")
    pdf.ln(13)
    pdf.multi_cell(190, 8, "М.П.                         ", align="R")
    pdf.add_page()
    pdf.improved_table(col_names, data)
    pdf.output("output.pdf")
