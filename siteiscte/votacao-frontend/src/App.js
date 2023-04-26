import logo from './logo.svg';
import './App.css';
import React, { Component, Fragment } from "react"; //(7)
import Header from "./components/Header";
import Home from "./components/Home";
class App extends Component { //(6)
 render() {
   return (
  <Fragment>
  <Header/>
  <Home/>
  </Fragment>
 );
 }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
