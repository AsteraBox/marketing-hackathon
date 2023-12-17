import React from "react";
import ReactDOM from "react-dom/client";

import { ConfigProvider } from "antd";
import ruRU from "antd/locale/ru_RU";

import { Provider } from "react-redux";
import { store } from "./redux/store";

import App from "./App";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <React.StrictMode>
        <Provider store={store}>
            <ConfigProvider locale={ruRU}>
                <App />
            </ConfigProvider>
        </Provider>
    </React.StrictMode>
);
