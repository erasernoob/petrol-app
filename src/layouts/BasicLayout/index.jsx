import { Layout } from "@arco-design/web-react";
import { useEffect, useRef, useState } from "react";
import { RouterProvider } from "react-router-dom";
import routerList from "../../routers";
import NavBar from "./components/Navbar";
import "./style.css";

const Sider = Layout.Sider;
const Content = Layout.Content;
const Header = Layout.Header;

export default function BasicLayout() {
  const [visible, setVisible] = useState(false);
  const [shouldRenderNewContent, setShouldRenderNewContent] = useState(true);
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
        {shouldRenderNewContent && <RouterProvider router={routerList} />}
      </div>
    </div>
  );
}
