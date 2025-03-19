import { Layout } from "@arco-design/web-react";
import { useEffect, useState } from "react";
import { RouterProvider } from "react-router-dom";
import routerList from "../../routers";
import NavBar from "./components/Navbar";
import "./style.css";

const Sider = Layout.Sider;
const Content = Layout.Content;
const Header = Layout.Header;

export default function BasicLayout() {
  const [visible, setVisible] = useState(false);
  const [isChangingRoute, setIsChangingRoute] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false); // 控制动画完成后再渲染内容

  // 监听路由变化
  useEffect(() => {
    const handleRouteChange = () => {
      setIsChangingRoute(true);
      setIsAnimating(true); // 开始动画，暂时隐藏内容

      setTimeout(() => {
        setIsChangingRoute(false);
      }, 600); // 动画时间
    };

    window.addEventListener("popstate", handleRouteChange);
    return () => window.removeEventListener("popstate", handleRouteChange);
  }, []);

  useEffect(() => {
    if (isChangingRoute) {
      document.body.classList.add("route-transition");
      setTimeout(() => {
        document.body.classList.remove("route-transition");
        setIsAnimating(false); // 动画完成后再显示内容
      }, 600);
    }
  }, [isChangingRoute]);

  // 让初始动画更流畅
  useEffect(() => {
    setTimeout(() => {
      requestAnimationFrame(() => setVisible(true));
    }, 600);
  }, []);

  return (
    <div className={`basic-layout fade-in ${visible ? "visible" : ""}`}>
      <NavBar />
      <div className={`content ${isChangingRoute ? "content-transition" : ""}`}>
        {/* 先等动画完成后再渲染内容，防止内容提前闪现 */}
        {!isAnimating && <RouterProvider router={routerList} />}
      </div>
    </div>
  );
}
