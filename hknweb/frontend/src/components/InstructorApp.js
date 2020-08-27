import { render } from "react-dom";
import React from "react";

import BaseApp from "./BaseApp";
import { INSTRUCTORAPP_NAME } from "./constants"


class InstructorApp extends BaseApp {
  API_PATH = "api/instructors"

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

const container = document.getElementById(INSTRUCTORAPP_NAME);
render(<InstructorApp />, container);
