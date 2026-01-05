import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Auth from "./components/Auth";
import TaskManager from "./components/TaskManager";
import Analytics from "./components/Analytics";
import { UserProvider } from "./context/UserContext";

const App = () => {
  return (
    <UserProvider>
      <Router>
        <Switch>
          <Route path="/auth" component={Auth} />
          <Route path="/tasks" component={TaskManager} />
          <Route path="/analytics" component={Analytics} />
          <Route path="/" exact component={() => <div>Welcome</div>} />
        </Switch>
      </Router>
    </UserProvider>
  );
};

export default App;