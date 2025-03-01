import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import './App.css'
import { ConfigProvider } from "@arco-design/web-react";
import store from "./store/store";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
    <ConfigProvider theme='dark'>
                <App />
    </ConfigProvider>
    </Provider>
  </React.StrictMode>,
);
