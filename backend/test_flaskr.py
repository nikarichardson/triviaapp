import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia" 
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        question = Question(question="Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",answer="Maya Angelou",difficulty=2,category=4)
        question.insert() 
        self.id = question.id

        self.new_question = {
            'question': 'Who was the first man on the moon?',
            'answer': 'Neil Armstrong',
            'difficulty': 1,
            'category':1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        # restore deleted question
        
        question = Question(question="Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",answer="Maya Angelou",difficulty=2,category=4)
        question.insert() 

        # delete new question
        res = self.client().delete('/questions/' + str(self.id))
        pass

    """
    Test get categories endpoint. 
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalCategories'])
        self.assertTrue(len(data['categories']))

    """
    Test get questions endpoint.
    """
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))

    """
    Test question deletion.
    """
    def test_delete_question(self):
        res = self.client().delete('/questions/'+str(self.id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], self.id)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        question = Question.query.filter(Question.id == self.id).one_or_none()
        self.assertEqual(question, None)

    """
    Test that error 404 arises if delete question fails by testing the deletion of a non-existent question.
    """
    def test_404_delete_question(self):
        res = self.client().delete('/questions/'+str(4000))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    """
    Test that error 422 arises if trying to add an invalid question. 
    """
    def test_422_add_bad_question(self):
        res = self.client().post('/questions', json=None)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)

    """
    Test create questions endpoint.  
    """
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        question = data['question']
        self.id = question['id']

    """
    Test get questions by category.
    """
    def test_get_by_category(self):
        res = self.client().get('/categories/2/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(len(data))
        self.assertEqual(data['currentCategory'], 2)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()