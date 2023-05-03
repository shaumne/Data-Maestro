from flask import Flask, request, render_template
from NewsBriefCompiler_KWFilter import get_summary


class NewsBriefApp:

    def __init__(self):
        self.app = Flask(__name__, template_folder="template")

        self.app.route('/', methods=['GET', 'POST'])(self.index)

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)

    @staticmethod
    def index():
        if request.method == 'POST':
            keywords = request.form['keywords'].split(',')
            political_view = request.form['political_view']
            challenge_reinforce = request.form['challenge_reinforce']
            tone = request.form['tone']
            profession = request.form.get("profession")
            favourite_artist = request.form.get("favourite_artist")
            output_type = "a"
            summary = get_summary(keywords, political_view, challenge_reinforce, tone, profession, favourite_artist, output_type)
            return render_template('summary.html', summary=summary)
        elif request.method == "GET":
            return render_template('index.html')


if __name__ == '__main__':
    app = NewsBriefApp()
    app.run(debug=True)
