import os
from flask import Flask, request, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  '''Configure pagination according to questions per page constant'''
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  Sets up CORSand allows '*' for origins.
  '''
  CORS(app, resources={r'/*': {'origins': '*'}})

  '''
  Uses the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  Handles GET requests for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
      selection = Category.query.order_by(Category.id).all()

      if len(selection) == 0:
          abort(404)

      categories = [category.format() for category in selection]

      return jsonify({
        'success': True,
        'categories': categories,
        'totalCategories': len(Category.query.all())
      })

  '''
  Handles GET requests for questions, including pagination (every 10 questions).
  Returns a list of questions, number of total questions, current category, categories.
  '''
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
      ## get current questions 
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      if len(current_questions) == 0:
          abort(404)

      ## get all categories 
      query = Category.query.all()
      categories = {}

      ## create a dictionary in accordance w/ frontend req
      for category in query:
        i = str(category.id)
        categories[i] = category.type

      return jsonify({
        'success': True,
        'questions': current_questions,
        'totalQuestions': len(Question.query.all()),
        'categories':  categories,
        'currentCategory': categories
      })

  '''
  Handles POST request to create a new question. 
  Attempt searching existing questions before proceeding
  to question creation. 
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    search = body.get('searchTerm',None)
    question = Question(question=new_question, answer=new_answer, category=new_category,difficulty=new_difficulty)
    question.insert()

    ## get all categories 
    query = Category.query.all()
    categories = {}
    for category in query:
      i = str(category.id)
      categories[i] = category.type


    try:
      if search:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request,selection)

        return jsonify({
          'success': True,
          'questions': current_questions, 
          'totalQuestions': len(selection.all()),
          'categories': categories,
          'currentCategory': categories
        })

      else:
        # get new current questions 
        selection = Question.query.order_by(Question.category).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'question': question.format() 
        })

    except:
      abort(422)

  '''
  Provides search functionality on questons with partial string search. 
  Returns questions that contains the search term. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json() 
    questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))

    ## get all categories 
    query = Category.query.all()
    categories = {}
    for category in query:
      i = str(category.id)
      categories[i] = category.type

    return jsonify({
      'success': True,
      'questions': questions,
      'totalQuestions': len(Question.query.all()),
      'categories':  categories,
      'currentCategory': categories 
    })


  '''
  Get questions by category. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def retrieve_questions_by_category(category_id):
    try:
      questions = Question.query.filter(Question.category == category_id).all() 
      currentCategory = Category.query.filter(Category.id == category_id)

      return jsonify({ 
        'success': True, 
        'questions': questions,
        'totalQuestions': len(questions),
        'categories':  categories,
        'currentCategory': currentCategory.type
        })

    except:
      abort(422) 

  '''
  Enables question deletion. Aborts if unsuccessful.  
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try: 
      question = Question.query.filter(Question.id == question_id).one_or_none()
  
      if question is None:
        abort(404)

      question.delete()

      ## get current questions 
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'totalQuestions': len(Question.query.all()),
      })

    except:
      abort(422)

  '''
  Error Handlers 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 500
  
  return app
