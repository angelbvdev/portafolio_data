from flask import Flask, render_template

app = Flask(__name__)

# Home
@app.route("/")
def index():
    return render_template("index.html")


# Sobre mí
@app.route('/about')
def about():
    return render_template("about.html")

# Proyectos
@app.route('/projects')
def projects():
    return render_template("projects.html")

# Contacto
@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
