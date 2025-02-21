import { useState } from "react";
import reactLogo from "./assets/react.svg";
import { invoke } from "@tauri-apps/api/core";
import "./App.css";
import { Button } from "@arco-design/web-react";
import "@arco-design/web-react/dist/css/arco.css";
import { ConfigProvider } from "@arco-design/web-react";
import BasicLayout from "./layouts /BasicLayout";

function App() {

  document.body.setAttribute('arco-theme', 'dark');

  return (
      <BasicLayout />
 );
}

export default App;
