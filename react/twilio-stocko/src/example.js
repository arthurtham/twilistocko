import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import './example.css';

// This site has 3 pages, all of which are rendered
// dynamically in the browser (not server rendered).
//
// Although the page does not ever refresh, notice how
// React Router keeps the URL up to date as you navigate
// through the site. This preserves the browser history,
// making sure things like the back button and bookmarks
// work properly.

export default function BasicExample() {
  return (
    <Router>
      <div>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/about">About</Link>
          </li>
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
        </ul>

        <hr />

        {/*
          A <Switch> looks through all its children <Route>
          elements and renders the first one whose path
          matches the current URL. Use a <Switch> any time
          you have multiple routes, but you want only one
          of them to render at a time
        */}
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="/about">
            <About />
          </Route>
          <Route path="/dashboard">
            <Dashboard />
          </Route>
          
        </Switch>
      </div>
    </Router>
  );
}

// You can think of these components as "pages"
// in your app.

function Home() {
  return (
    <div>
      <h2>Welcome to Twilio Stocko</h2>
      <b>Get all your Twilio Stock</b>

      <p>
          <Link to="/dashboard">Dashboard</Link>
      </p>
    </div>
  );
}

function About() {
  return (
    <div>
      <h2>About</h2>
    </div>
  );
}

function Dashboard() {
    

    return (
        <div>
            <h2>Dashboard</h2>
            <form>
                Phone Number<input name="form-phone-number" id="form-phone-number" />
                <button type="submit" name="form-phone-number-search" id="form-phone-number-search" onClick={GetDataByPhone}>Search</button>
            </form>

            <hr />

            <div name="mongo-results" id="mongo-results">

            </div>

            <div name="mongo-submit-div" id="mongo-submit-div" style={{visibility:'hidden'}}>
            <button name='update-notifications' id='update-notifications' onClick={HelloWorld}>Submit</button>
            </div>

            <div name="add-notification-div" id="add-notification-div" style={{visibility:'hidden'}}>

            </div>

        </div>
    );
}


// Dashboard functions

function HelloWorld(e) {
    e.preventDefault();

    console.log("Hello world!");
    return false;
}

function ShowSubmitButtons() {
    //var submitElement = document.getElementById("mongo-submit-div");
    document.getElementById("mongo-submit-div").style.visibility = "visible";
    document.getElementById("add-notification-div").style.visibility = "visible";

}

function SubmitData(e){
    var submitData = {
        "phone": "00000000", //Dummy Data
        "stocks": []
    };



}

function GetDataByPhone(e) {
    e.preventDefault();

    var phoneNumberElement = document.getElementById("form-phone-number");
    var phoneNumber = phoneNumberElement.value;
    console.log(phoneNumber);
    //phoneNumberElement.disabled = true;

    //TODO: Get back results. Send: "+194955512345", return a JSON with our data

    var results = {
        "_id": {
            "$oid": "605d670452b3c30869b3d95f"
        },
        "phone": "000002222",
        "stocks": [
            {
                "symbol": "AAPL",
                "target": 60,
                "mode": "less"
            },
            {
                "symbol": "MSFT",
                "target": 50,
                "mode": "greater"
            }
        ]
    }

    var stocks = results["stocks"];
    console.log(stocks)

    var resultHtml = "<h1>Results for Phone Number <span name='shown-phone-number' id='shown-phone-number'>"+phoneNumber+"</span></h1>\
    \
    <table><tr><th>Stock</th><th>Target Point</th><th>Mode</th><th>Remove?</th></tr>";

    for (var _i = 0; _i < stocks.length; ++_i) {
        var stocksEntry = stocks[_i];
        console.log(stocksEntry);
        console.log(stocksEntry["mode"].valueOf() === "less");
        resultHtml += "<tr>\
            <td>"+stocksEntry["symbol"]+"</td>\
            <td><input name='target"+_i.toString()+"' id='target"+_i.toString()+"' value='"+stocksEntry["target"]+"' /></td>\
            <td>\
                Less    <input name='mode"+_i.toString()+"' id='mode"+_i.toString()+"' type='radio' "+(stocksEntry["mode"].valueOf() === "less" ? "checked" : "")+" />\
                Greater <input name='mode"+_i.toString()+"' id='mode"+_i.toString()+"' type='radio' "+(stocksEntry["mode"].valueOf() === "greater" ? "checked" : "")+" />\
            </td>\
            <td>\
                <input name=<input name='delete"+_i.toString()+"' id='delete"+_i.toString()+"' type='checkbox' />\
            </td>\
            </tr>";

    }
    

    resultHtml += "</table>";

    document.getElementById("mongo-results").innerHTML = resultHtml;
    ShowSubmitButtons();

    //TODO: "Add stock" section
    var addHtml = "<h2>Add a stock notification</h2>\
    <table><tr><th>Stock</th><th>Target Point</th><th>Mode</th></tr>\
    <tr>\
    <td><input name='symbolAdd' id='symbolAdd' value='AAPL'</td>\
    <td><input name='targetAdd' id='targetAdd' value=100 /></td>\
    <td>\
        Less    <input name='modeAdd' id='modeAdd' type='radio' checked />\
        Greater <input name='modeAdd' id='modeAdd' type='radio') />\
    </td>\
    </tr></table>";

    document.getElementById("add-notification-div").innerHTML = addHtml;

    
}