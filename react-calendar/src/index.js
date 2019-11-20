import React from "react";
import ReactDOM from "react-dom";

import Calendar from "./components/calendar";
import "./css/style.css"
import "mdbreact/dist/css/mdb.css";

class NewComponent extends React.Component {
  render() {
    return (
      <div>
        new component
      </div>
    );
  }
}

function App() {
  return (<div>
        <nav class="mb-0 navbar fixed-top navbar-expand-lg navbar-dark shadow-none" style={{"backgroundColor": "#32323f"}}>
        <a className="navbar-brand" href="#">CALENDAR</a>
        </nav>
        <nav className="mb-0 navbar navbar-expand-lg navbar-dark shadow-none" style={{"backgroundColor": "#32323f"}}>
        <a className="navbar-brand" href="#">CALENDAR</a>
        </nav>
    <div className="sidenav border-right">
        <div className="card bg-white rounded-0">
            <div className="card-body">
                <i className="fas fa-lg fa-chalkboard-teacher"></i>
                <span id="fname"></span>
                <small id="fcode" className="text-muted">F-Code</small>
            </div>
        </div>
        <button className="btn btn-light active rounded-0 w-100 m-0 shadow-none"><i className="fas fa-home"></i> Home
        </button>
        <button className="btn btn-light rounded-0 w-100 m-0 shadow-none"><i className="fas fa-bell"></i> Notifications
            <span className="badge bg-danger">1</span> </button>
        <button id="logout" className="btn btn-light rounded-0 w-100 m-0 shadow-none"><i className="fas fa-sign-out-alt"></i> LOGOUT
        </button>
    </div>
        <Calendar />
  </div>);
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
