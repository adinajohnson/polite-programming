from flask import Flask, request, render_template
import interpret
import sys

app = Flask(__name__)

@app.route('/')
def mn():
   return render_template('index.html')

@app.route('/result', methods = ['POST'])
def result():
   if request.method == 'POST':
      result = request.form['text']
      print(result, file=sys.stderr)
      lexer = interpret.Lexer(result)
      parser = interpret.Parser(lexer)
      interpreter = interpret.Interpreter(parser)
      done = interpreter.interpret()
      return render_template("result.html", result = done)

if __name__ == '__main__':
   app.run(debug = True)
