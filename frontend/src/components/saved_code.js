componentDidMount(){
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }

   getCategories = () => {
    $.ajax({ 
      url: `/categories`, 
      type: "GET",
      success: (result) => {
        this.setState({
          categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again here')
        return;
      }
    })
  }


     <select name="category" onChange={this.handleChange}>
              {Object.keys(this.state.categories).map(id => {
                  return ( 
                    <option key={id} value={id}>{this.state.categories[id]}</option>
                  )
                })}
            </select>


     {Object.keys(this.state.categories).map((id, ) => (
              <option key={id} onClick={() => {this.getByCategory(id)}}>
                {this.state.categories[id]}
               </option> 
            ))}

           {Object.keys(this.state.categories).map((id, ) => (
              <li key={id} onClick={() => {this.getByCategory(id)}}>
                {this.state.categories[id]}
                <img className="category" src={`${this.state.categories[id]}.png`}/>
              </li>
            ))}



 <select name="category" onChange={this.handleChange}>
              {Object.keys(this.state.categories).map((id, ) => (
              <option key={id} value={id} onClick={() => {this.getByCategory(id)}}>
                {this.state.categories[id]}</option>
            </select>