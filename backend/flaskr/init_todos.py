	'''
	TEST: At this point, when you start the application
	you should see questions and categories generated,
	ten questions per page and pagination at the bottom of the screen for three pages.
	Clicking on the page numbers should update the questions. 
	'''

	'''
	@TODO: 
	Create an endpoint to DELETE question using a question ID. 
	
	TEST: When you click the trash icon next to a question, the question will be removed.
	This removal will persist in the database and when you refresh the page. 
	
	@TODO: 
	Create an endpoint to POST a new question, 
	which will require the question and answer text, 
	category, and difficulty score.

	TEST: When you submit a question on the "Add" tab, 
	the form will clear and the question will appear at the end of the last page
	of the questions list in the "List" tab.  
	'''


@app.route('/questions', methods=['POST'])
  def create_questions():
    body = request.get_json()

    new_question = body.get('title', None)
    new_answer = body.get('author', None)
    new_difficulty = body.get('rating', None)
    new_category = body.get('category',None)
    try:
       question = Question(question=new_question,answer=new_answer,difficulty=new_difficulty,category=new_category)
       question.insert()

       return jsonify({
          'success': True
        })

    except:
      abort(422)
 

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(book_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
   
      return jsonify({
        'success': True})

    except:
      abort(422)

	'''
	@TODO: 
	Create a POST endpoint to get questions based on a search term. 
	It should return any questions for whom the search term 
	is a substring of the question. 

	TEST: Search by any phrase. The questions list will update to include 
	only question that include that string within their question. 
	Try using the word "title" to start. 
	'''

	'''
	@TODO: 
	Create a GET endpoint to get questions based on category. 

	TEST: In the "List" tab / main screen, clicking on one of the 
	categories in the left column will cause only questions of that 
	category to be shown. 
	'''


	'''
	@TODO: 
	Create a POST endpoint to get questions to play the quiz. 
	This endpoint should take category and previous question parameters 
	and return a random questions within the given category, 
	if provided, and that is not one of the previous questions. 

	TEST: In the "Play" tab, after a user selects "All" or a category,
	one question at a time is displayed, the user is allowed to answer
	and shown whether they were correct or not. 
	'''
	## take parameters ?? 
	@app.route('/quizzes/<int:question_id>', methods=['DELETE'])
  	def delete_question(book_id):
   		pass

	'''
	@TODO: 
	Create error handlers for all expected errors 
	including 404 and 422. 
	'''
	