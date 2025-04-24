from flask import Flask
app = Flask(__name__)

def user(name):
    if name.isalpha() and name.isupper():
        name = name.lower()
    elif name.isalpha() and name.islower():
        name = name.upper()
    elif name.isalpha():
        name = name.upper()  # Convert mixed case to uppercase
    name = name.lstrip()  # Remove leading spaces
    name = ''.join(filter(str.isalpha, name))  # Remove numbers
    return f"<h1>Welcome, {name}, to my CSCB20 website!</h1>"

@app.route('/<name>')
def greet(name):
    return user(name)

if __name__ == '__main__':
    app.run(debug=True)
