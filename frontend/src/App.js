import React, { useEffect } from "react";

import { useSelector } from "react-redux";

import Login from "./components/login";
import List from "./components/list";

function App() {
    const { authorized } = useSelector((state) => state.auth);

    return authorized ? <List /> : <Login />;
}

export default App;
