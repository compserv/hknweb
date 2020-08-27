import { render } from "react-dom";
import React from "react";

import BaseApp from "./components/BaseApp";
import { DEPARTMENTAPP_NAME } from "./components/constants";


class DepartmentApp extends BaseApp {
  API_PATH = "api/departments"

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

const container = document.getElementById(DEPARTMENTAPP_NAME);
render(<DepartmentApp />, container);
