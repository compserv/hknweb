import React, { Component } from "react";
import { render } from "react-dom";

class DepartmentApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("api/departments")
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
        {this.state.data.map(department => {
          return (
            <li key={department.id}>
              {department.name} - {department.abbr}
            </li>
          );
        })}
      </ul>
    );
  }
}

export default DepartmentApp;

const container = document.getElementById("departments_app");
render(<DepartmentApp />, container);