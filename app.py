from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/web')
def web():
    return """<!doctype html>
        <html> 
           <body> 
                <h1>Web-сервес на flask </h1> 
                <a href="/author">author</a>
           </body> 
        </html>"""

@app.route('/author')
def author():
    name = "Булыгина Елизавета Денисовна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html> 
           <body> 
                <P>Студент: """ + name + """</p> 
                <P>Группа: """ + group + """</p> 
                <P>Факультет: """ + faculty+ """</p> 
                <a href="/web">web</a>
           </body> 
        </html>"""

@app.route('/image')
def image():
    path = url_for("static",filename="kitty.png")
    return '''
<!doctype html>
<html> 
    <body> 
        <h1> Грустный котик (Я) </h1>
        <img src="''' + path +'''">
    </body> 
</html>
'''