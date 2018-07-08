from flask import Flask, request, render_template, jsonify
import interpret
import sys

app = Flask(__name__)

@app.route('/')
def mn():
   return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
   try:
      result = request.args.get('prog', 0, type=str)      
      lexer = interpret.Lexer(result)
      parser = interpret.Parser(lexer)
      interpreter = interpret.Interpreter(parser)
      done = interpreter.interpret()
      return jsonify(result = done)
   except Exception as e:
      return jsonify(result = str(e))

if __name__ == '__main__':
   app.run(debug = True)
