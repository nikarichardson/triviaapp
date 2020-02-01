import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {}
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({ 
      url: `/questions?page=1`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.totalQuestions,
          categories: result.categories,
          currentCategory: result.currentCategory })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again here')
        return;
      }
    })
  }

  getByCategory= (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, 
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.totalQuestions,
          currentCategory: result.currentCategory })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions', 
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        alert('Question successfully added!')
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question.')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
          <label>
            Question
            <input type="text" name="question" onChange={this.handleChange}/>
          </label>
          <label>
            Answer
            <input type="text" name="answer" onChange={this.handleChange}/>
          </label>
          <label>
            Difficulty
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </label>
          <label>
            Category
            <select name="category" onChange={this.handleChange}>
              {Object.keys(this.state.categories).map((id, ) => (
             <option key={id} value={id} onClick={() => {this.getByCategory(id)}}>
                {this.state.categories[id]}
               </option> 
            ))}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;
