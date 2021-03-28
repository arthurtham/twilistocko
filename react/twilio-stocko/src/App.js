import React, { useState } from "react";
// import {
//   BrowserRouter as Router,
//   Switch,
//   Route,
//   Link
// } from "react-router-dom";
import './example.css';

// This site has 3 pages, all of which are rendered
// dynamically in the browser (not server rendered).
//
// Although the page does not ever refresh, notice how
// React Router keeps the URL up to date as you navigate
// through the site. This preserves the browser history,
// making sure things like the back button and bookmarks
// work properly.

// export default function BasicExample() {
//   return (
//     <Router>
//       <div>
//         <ul>
//           <li>
//             <Link to="/">Home</Link>
//           </li>
//           <li>
//             <Link to="/about">About</Link>
//           </li>
//           <li>
//             <Link to="/dashboard">Dashboard</Link>
//           </li>
//         </ul>

//         <hr />

//         {/*
//           A <Switch> looks through all its children <Route>
//           elements and renders the first one whose path
//           matches the current URL. Use a <Switch> any time
//           you have multiple routes, but you want only one
//           of them to render at a time
//         */}
//         <Switch>
//           <Route exact path="/home">
//             <Home />
//           </Route>
//           <Route path="/about">
//             <About />
//           </Route>
//           <Route path="/">
//             <Dashboard />
//           </Route>
          
//         </Switch>
//       </div>
//     </Router>
//   );
// }

// You can think of these components as "pages"
// in your app.

// function Home() {
//   return (
//     <div>
//       <h2>Welcome to Twilio Stocko</h2>
//       <b>Get all your Twilio Stock</b>

//       <p>
//           <Link to="/dashboard">Dashboard</Link>
//       </p>
//     </div>
//   );
// }

// function About() {
//   return (
//     <div>
//       <h2>About</h2>
//     </div>
//   );
// }

function MongoResults({stocksEntry}) {
  //console.log("Yolo");
  //console.log(stocksEntry);
  return (
    <tr>
      <td>{stocksEntry["symbol"]}</td>
      <td>{stocksEntry["target"]}</td>
      <td>{stocksEntry["mode"]}</td>
      <td>
          <button onClick={(e) => (RemoveEntry(e, {stocksEntry}))}>Delete</button>
      </td>
    </tr>
  );
}

export default function App() {
    //var temp = [{"symbol": "AMZN","target": 80,"mode": "less"},{"symbol": "MSFT","target": 40,"mode": "greater"}];
    const [mongoResults, setMongoResults] = useState([]);
    const updateMongoResults = (e) => {
      e.preventDefault();
      document.getElementById("mongo-results").style.visibility = "visible";
      document.getElementById("shown-phone-number").innerHTML = document.getElementById("form-phone-number").value;
      setMongoResults(GetDataByPhone(e))
    }
    return (
        <div>
            <h2>Dashboard</h2>
            <form>
                Phone Number<input name="form-phone-number" id="form-phone-number" placeholder="+15551234567" />
                <button type="submit" name="form-phone-number-search" id="form-phone-number-search" onClick={updateMongoResults}>Search</button>
            </form>

            <hr />

            <div name="mongo-results" id="mongo-results" style={{visibility:'hidden'}}>
              <h1>Results for Phone Number <span name='shown-phone-number' id='shown-phone-number'>null</span></h1>
              <table>
              <thead><tr><th>Stock</th><th>Target</th><th>Mode</th><th>Delete?</th></tr></thead>
              <tbody>
              {mongoResults.map((result, index) => (
                //console.log({result})
                <MongoResults key={index} stocksEntry={result}></MongoResults>
              ))}
              </tbody>             
              </table>
            </div>

            {/* <div name="mongo-submit-div" id="mongo-submit-div" style={{visibility:'hidden'}}>
              <button name='update-notifications' id='update-notifications' onClick={HelloWorld}>Submit</button>
            </div> */}

            <div name="add-notification-div" id="add-notification-div" style={{visibility:'hidden'}}>
              <h2>Add a stock notification</h2>
              <table>
                <thead>
                  <tr><th>Stock</th><th>Target Point</th><th>Mode</th></tr>
                </thead>
                <tbody>
                  <tr>
                    <td><input name='symbolAdd' id='symbolAdd' value='AAPL'></input></td>
                    <td><input name='targetAdd' id='targetAdd' value="100" /></td>
                    <td>
                        Less    <input name='modeAdd' id='modeAdd' type='radio' defaultChecked />
                        Greater <input name='modeAdd' id='modeAdd' type='radio' />
                    </td>
                  </tr>
                </tbody>
              </table>
              <button name='add-notifications' id='add-notifications' onClick={AddNotification}>Add</button>
            </div>
        </div>
    );
}

var MONGO_LINK = "http://127.0.0.1:5000";

// Dashboard functions
function HelloWorld(e) {
    e.preventDefault();

    console.log("Hello world!");
    return false;
}

function ShowSubmitButtons() {
    //var submitElement = document.getElementById("mongo-submit-div");
    //document.getElementById("mongo-submit-div").style.visibility = "visible";
    //document.getElementById("add-notification-div").style.visibility = "visible";

}

function HideSubmitButtons() {
    //document.getElementById("mongo-submit-div").style.visibility = "hidden";
    //document.getElementById("add-notification-div").style.visibility = "hidden";
}

function RemoveEntry(e, stocksEntry) {
  console.log("Remove");
  console.log(stocksEntry);

  GetDataByPhone(e);
}

function AddNotification(e){
    var greater = false;
    var greaterOrLessOptions = document.getElementsByName("modeAdd");
    if (greaterOrLessOptions[0].checked === true) {
      greater = false;
    } else if (greaterOrLessOptions[1].checked === true) {
      greater = true;
    }

    var submitData = {
        "phone": document.getElementById("shown-phone-number").innerHTML, 
        "stock": document.getElementById("symbolAdd").value,
        "target": document.getElementById("targetAdd").value,
        "mode": greater ? "greater" : "less" // or less
    };

    console.log("AddNotification");
    console.log(submitData);

    const requestOptions = {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify( submitData )
    };

    fetch(MONGO_LINK+"/hello-world", requestOptions)
    .then(response => response.json())
    .then(data => 
      console.log(data)
      );
      //TODO: Connect to ConfirmNotificationAdded function

}

function ConfirmNotificationAdded(data) {

}

function GetDataByPhone(e) {
    e.preventDefault();

    var phoneNumberElement = document.getElementById("form-phone-number");
    var phoneNumber = phoneNumberElement.value;
    console.log(phoneNumber);
    //phoneNumberElement.disabled = true;

    //TODO: Get back results. Theoretically: send phone number to mongo, and we will get JSON back with the necessary data
    var results = {
      "+15101234567" : [
        {
          "symbol": "AMZN",
          "target": 80,
          "mode": "less", 
        },
        {
          "symbol": "MSFT",
          "target": 30,
          "mode": "greater"
        }
      ]
    }

    var stocks;
    document.getElementById("add-notification-div").style.visibility = "visible";
    if (phoneNumber in results) {
      stocks = results[phoneNumber]
      console.log(stocks);
      ShowSubmitButtons();
      return stocks;
  } else {
    console.log("phone number not found");
    HideSubmitButtons();
    //document.getElementById("add-notification-div").style.visibility = "visible";
    return [];
  }
    
}

//export default App;