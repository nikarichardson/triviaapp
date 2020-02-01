 @app.route('/play', methods=['GET'])
  def play_quiz():
    body = request.get_json() 
    previous_questions = body.get(previousQuestions)
    category_id = body.get(quiz_category)

    try: 
      questions_in_category = Question.query.filter(Question.category == category_id).all() 
      ids_in_category = Question.id.query.filter(Question.category == category_id).all() 
      question = questions_in_category.filter(~Question.id.in_(ids_in_category)).order_by(func.rand()).first()
      
      if len(question) > 0: 
        return jsonify({
          'success': True,
          'question': Question.format(question)
        })

      else:
        abort(416)

    except:
      abort(422)
  