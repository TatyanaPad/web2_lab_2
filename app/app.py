from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')


@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/cookies')
def cookies():
    resp = make_response(render_template('cookies.html'))
    if 'name' in request.cookies:
        resp.delete_cookie('name')
    else:
        resp.set_cookie('name', 'value')
    return resp


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')


@app.errorhandler(404)
def page_not_found(error):
    """Handles page not found errors."""
    return render_template('page_not_found.html'), 404


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    result = ''
    error_text = ''

    if request.method == 'POST':
        try:
            first_num = int(request.form['firstnumber'])
            second_num = int(request.form['secondnumber'])
        except ValueError:
            return render_template('calc.html', result=result, error_text='Содержимое ввода не является цифрой!')

        operation = request.form['operation']
        if operation == '+':
            result = first_num + second_num
        elif operation == '-':
            result = first_num - second_num
        elif operation == '*':
            result = first_num * second_num
        elif operation == '/':
            if second_num == 0:
                error_text = 'На ноль делить нельзя!'
            else:
                result = first_num / second_num

    return render_template('calc.html', result=result, error_text=error_text)


def convert_tel_to_number(tel):
    """Convert phone number to a sequence of numbers."""
    return tel.replace(' ', '').replace('-', '').replace('+', '').replace('(', '').replace(')', '').replace('.', '')


def is_digit(tel):
    """Check if all characters in the string are numbers."""
    return tel if tel.isdigit() else None


def check_length(tel):
    """Check the length of the phone number."""
    if len(tel) == 10 or (len(tel) == 11 and tel[0] in ['7', '8']):
        return tel
    return None


def validate_phone_input(tel):
    """Check if the phone number meets input conditions."""
    tel = convert_tel_to_number(tel)
    if is_digit(tel) == tel:
        if check_length(tel) == tel:
            return 'Номер телефона верный', tel, {'input_class': 'is-valid', 'div_class': 'valid-feedback'}
        else:
            return 'Недопустимый ввод. Неверное количество цифр!', None, {'input_class': 'is-invalid',
                                                                          'div_class': 'invalid-feedback'}
    return 'Недопустимый ввод. В номере телефона встречаются недопустимые символы!', None, {'input_class': 'is-invalid',
                                                                                            'div_class': 'invalid-feedback'}


def standardize_phone_number(tel):
    """Convert the phone number to a standard format."""
    if len(tel) == 11:
        prefix = '8-' if tel[0] == '8' else '8-'
        return prefix + tel[1:4] + '-' + tel[4:7] + '-' + tel[7:9] + '-' + tel[9:11]
    return '8-' + tel[0:3] + '-' + tel[3:6] + '-' + tel[6:8] + '-' + tel[8:10]


@app.route('/tel_form', methods=['GET', 'POST'])
def tel_form():
    message = ''
    tel = ''
    bootstrap_class = {}

    if request.method == 'POST':
        phone_number = str(request.form['tel'])
        message, tel, bootstrap_class = validate_phone_input(phone_number)

        if tel is not None:
            tel = standardize_phone_number(tel)

    return render_template(
        'tel_form.html',
        message=message,
        phone_number=tel,
        bootstrap_class=bootstrap_class,
        input_class=bootstrap_class.get('input_class', ''),
        div_class=bootstrap_class.get('div_class', '')
    )


if __name__ == '__main__':
    app.run(debug=True, port=5002)
