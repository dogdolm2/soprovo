# Волынцев Антон - "сопровождающий.рф"
# Пользовательские сценарии

### Группа: 10 - И - 5
### Электронная почта: aavolyntsev@edu.hse.ru


### [ Сценарий 1 - Регистрация пользователя ]

1. Пользователь вводит почту, с которой он будет заходить в систему (обязательно корпоративную, проводится проверка)
2. Пользователь вводит пароль, с которым он будет заходить в систему
3. Если выбранная почта уже существует в системе, то пользователю сообщается об этом и предлагается ввечти другую или войт
4. Если пароль содержит менее 6 символов, система сообщает, что пароль должен быть от 6 до 30 символов и пользователь должен придумать новый пароль
5. Если введённый адрес электронной почты не соответствует формату, то система выводит сообщение об ошибке и просит ввести адрес ещё раз
6. Если все введённые данные соответствуют требованиям регистрации, то система отправляет на почту письмо для подтверждения почты.

### [ Сценарий 2 - Вход ]

1. Пользователь вводит почту, которую указывал при регистрации.
2. Пользователь вводит пароль, указанный при регистрации.
3. Пользователь нажимает кнопку "войти", после чего, при не соответствии хотя бы одного параметра, возвращает пользователю ошибку.

### [ Сценарий 3 - Регистрация / отмена регистрации на поездку ]

1. После входа, пользователь выбирает понравившуюся поездку, пользуясь экраном предпросмотра.
2. После выбора понравившейся поездки, при нажатии на нее, открывается экран просмотра поездки.
3. Пользователь нажимает кнопку "Зарегестрироваться", при наличии достаточного количества мест.
4. При отсутствии достаточного количества мест, запрос на регистрацию пользователя отправляется организатору поездки.
3а. Пользователь нажимает кнопку "Отменить регистрацию", если статус поездки не "Согласовано" или "Проведено".

### [ Сценарий 4 - Добавление поездки ]

1. После входа, на экране предпросмотра, пользователь вводит все необходимые данные поездки в разделе добавления поездок.
2. Пользователь нажимает кнопку добавления поездки.

### [ Сценарий 5 - Отчет / справка о поездке ]

1. После входа, пользователь выбирает интересующую его поездку.
2. Пользователь нажимает на поездку на экране предпросмотра.
(3). Пользователь регистрируется на поездку, при отсутствии регистрации.
4. Появляется возможность экспортировать данные о поездке в виде csv файла или pdf файла для печати.
5. Пользователь выбирает нужную ему опцию экспорта и нажимает на соответствующую кнопку.
6. В отедльной вкладке открывается запрошеный документ или начинается скачивание файла csv.

