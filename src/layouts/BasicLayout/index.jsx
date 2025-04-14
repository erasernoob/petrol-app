import { Layout } from "@arco-design/web-react";
import { useEffect, useRef, useState } from "react";
import { RouterProvider } from "react-router-dom";
import routerList from "../../routers";
import NavBar from "./components/Navbar";
import "./style.css";


export default function BasicLayout() {
  const [visible, setVisible] = useState(false);
  const contentRef = useRef(null);

  // 初始动画
  useEffect(() => {
    setTimeout(() => {
      requestAnimationFrame(() => setVisible(true));
    }, 100);
  }, []);

  return (
    <div className={`basic-layout fade-in ${visible ? "visible" : ""}`}>
      <NavBar />
      <div ref={contentRef} className="content">
        {<RouterProvider router={routerList} />}
      </div>
    </div>
  );
}
