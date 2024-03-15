from flask import Flask, render_template, flash, url_for, request, redirect, make_response

app = Flask(__name__)
app.secret_key = b'8878102d42a432616c6d66ca3bcaee01ce934fae9bfa9c2f7c3924c832842e82'

# Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан
# cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия,
# где будет отображаться имя пользователя. На странице приветствия должна быть кнопка «Выйти»,
# при нажатии на которую будет удалён cookie-файл с данными пользователя и произведено перенаправление
# на страницу ввода имени и электронной почты.

@app.route('/')
def to_login():
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['email']:
            flash('Заполните данные!', 'danger')
            return redirect(url_for('login'))
        name = request.form['name']
        email = request.form['email']
        response = make_response(redirect(url_for('main')))
        response.set_cookie('name', name)
        response.set_cookie('email', email)
        return response
    return render_template('login.html')


@app.route('/main/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        response = make_response(redirect(url_for('login')))
        response.set_cookie('name', 'None', max_age=0)
        response.set_cookie('email', 'None', max_age=0)
        return response
    context = {}
    if name := request.cookies.get('name'):
        context['name'] = name
    else:
        context['name'] = 'крутой хакер'
    if email := request.cookies.get('email'):
        context['email'] = email
    return render_template('main.html', **context)


if __name__ == '__main__':
    app.run(debug=True)