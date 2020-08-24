import React, { Component } from "react";
import { render } from "react-dom";

class InstructorApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("api/instructors")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }

  render() {
    return (
      <ul>
        {this.state.data.map(instructor => {
          return (
            <li key={instructor.instructor_id}>
              {instructor.instructor_id}
            </li>
          );
        })}
      </ul>
    );
  }
}

export default InstructorApp;

const container = document.getElementById("InstructorApp");
render(<InstructorApp />, container);