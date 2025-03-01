import { useState } from "react";
import reactLogo from "./assets/react.svg";
import { invoke } from "@tauri-apps/api/core";
import "./App.css";
import { Button } from "@arco-design/web-react";
import "@arco-design/web-react/dist/css/arco.css";
import LoginPage from "./pages/Login/LoginPage";
import BasicLayout from "./layouts/BasicLayout";

function App() {
  const [status, setStatus] = useState(false)
  return (
    <>
      { !status ?  <LoginPage setStatus={setStatus} /> : <BasicLayout />}
    </>
 );
}

export default App;
