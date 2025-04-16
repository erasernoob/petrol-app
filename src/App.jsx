import "@arco-design/web-react/dist/css/arco.css";
import { useState } from "react";
import { useDispatch } from 'react-redux';
import "./App.css";
import BasicLayout from "./layouts/BasicLayout";
import LoginPage from "./pages/Login/LoginPage";
import { setUseInitialOrNot } from "./store/dataSlice";

function App() {
  const [status, setStatus] = useState(false)
  const [test, setTest] = useState(false)
  if (test) {
    const dispatch = useDispatch()
    dispatch(setUseInitialOrNot(true))
  }

  return (
    <>
      {!status ? <LoginPage setStatus={setStatus} setTest={setTest} /> : <BasicLayout />}
    </>
  );
}

export default App;
