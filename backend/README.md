# Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is recommended to run this app within a virtual environment. More instructions for setting up a virtual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM is used to handle the lightweight sqlite database. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests from the frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```
bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```
bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints

## GET '/categories'
- **Description:** Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- **Request Arguments:** None
- **Returns:** An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
```
{
'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"
}
```
- **Errors:** If no categories are found, results in a 404 error. 

## GET '/questions'
- **Description:** Fetches a dictionary of questions. 
- Request Arguments: None 
- **Returns:** An object with the values of a questions object, defined in `models.py`, with id, question, answer, category, and difficulty. 
```
{
'success': True,
'questions': current_questions,
'totalQuestions': len(Question.query.all()),
'categories':  categories,
'currentCategory': 0
}
```
where success indicates that the questions have been retrieved successfully, totalQuestions is a count of all the questions in the database, categories is a dictionary id:type of all the categories in the database, and currentCategory is equal to 0 implying that all categories have been selected. 
- **Errors:** Results in 404 error if no questions found. If a problem has arisen with the query and the questions cannot be retrieved, results in a 422 error. 


## POST '/questions'
- **Description:** Creates a new question with this endpoint via the Question Form. The new question object will be created with the chosen question, answer, category, and difficulty level. If the search is activated instead, this endpoint 
- **Request Arguments:** None
- **Returns:**
If it finds a question that matches the searchTerm, the following will be returned
```
{
'success': True,
'questions': current_questions, 
'totalQuestions': len(selection.all()),
'categories': categories,
}
```
 where questions is the collection of question(s) objects that have returned from the search query using partial string search, totalQuestions is a number representing the total count of Questions, and categories is a dictionary of all the categories with key:value pairs id:*category_type*. *Category_type* is drawn from a list in the given database. 
 - Otherwise, new question creation will return
```
{
'success': True,
'question': question.format() 
}
 ```
 where success indicates that the new question has been successfully added to the database, and question is the formatted object of the newly created question. 
 - **Errors:** If either no search term is provided or no response body is given to fill the fields of a newly created question, then aborts in 404 error. If a new question cannot be added to the datbase, it aborts in a 422 error. 

 ## GET '/categories/category_id/questions'
- **Description:** Returns all the questions under the category identified by the given category id.
- Request Arguments: category_id
- **Returns:**
```
{
'success': True,
'questions': current_questions,
'totalQuestions': len(selection),
'categories':  categories,
'currentCategory': category_id
}
```
where currentCategory holds the category id of the query, categories points to the full dictionary of categories, questions holds the Question objects within the chosen category, and totalQuestions is a count of the total number of questions in the database. 
- **Errors:** If no questions found, aborts in 404 error. If there is an issue with querying and retrieving the categories, aborts in 422 error. 

## DELETE /questions/<int:question_id> 
- **Description:** Allows for the deletion of a question by question id. In the interface, a small trashbin button next to each question can be used to activate this endpoint. 
- **Request Arguments:** question_id 
- **Returns:**
```
{
'success': True,
'deleted': question_id,
'questions': current_questions,
'totalQuestions': len(Question.query.all()),
}
```
where success indicates the chosen question has been deleted from the database, deleted holds the id of the deleted question, and totalQuestions is a newly updated count of the questions in the database. 
- **Errors:** If no question has been found, it will abort in a 404 error. If there is a problem implementing the successful deletion of the question through the database connection, it will result in a 422 error. 

## POST '/quizzes' 
- **Description:** Allows for a quiz-like interface of randomized questions from a chosen category or from all categories, where a score is kept that indicates the number of accurate answers given. 
- **Request Arguments:** None (Gets previous questions and quiz category from the response body)
- **Returns:** If there are enough remaining questions that have not been used within the category, one such formatted question is returned thus. 
 ```
{
'success': True,
'question': Question.format(question)
}
```
It will force an end to the quiz if there are not any remaining questions within the category and the quiz has not come to an end yet. The final score will still be rendered to the user. It will also force an end to the quiz if there are no questions within the category. 
- **Errors:** If any failure has resulted from the querying, it will abort in a 422 error. 

## Error Handling
Errors are returned as JSON objects. See an example error handler below.

```
{
"success": False, 
"error": 422,
"message": "unprocessable"
}, 422
```

This api will return the following errors: 
- **400:** Bad Request
- **404:** Resource Not Found
- **422:** Not Processable 
- **500:** Internal Server Error
- **416:** Range Not Satisfiable 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
