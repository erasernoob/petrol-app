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

  // 监听路由变化
  useEffect(() => {
    const handleRouteChange = () => {
      // 1. 首先标记不应该渲染新内容
      setShouldRenderNewContent(false);

      // 2. 添加淡出效果
      if (contentRef.current) {
        contentRef.current.classList.add("content-fade-out");
      }

      // 3. 等待淡出完成
      setTimeout(() => {
        // 4. 动画结束后，允许渲染新内容，但保持隐藏状态
        setShouldRenderNewContent(true);

        // 5. 确保新内容先处于隐藏状态
        if (contentRef.current) {
          contentRef.current.classList.remove("content-fade-out");
          contentRef.current.classList.add("content-hidden");

          // 6. 在下一帧应用淡入动画
          requestAnimationFrame(() => {
            if (contentRef.current) {
              contentRef.current.classList.remove("content-hidden");
              contentRef.current.classList.add("content-fade-in");

              // 7. 动画结束后清理类
              setTimeout(() => {
                if (contentRef.current) {
                  contentRef.current.classList.remove("content-fade-in");
                }
              }, 800); // 与CSS动画时间匹配
            }
          });
        }
      }, 400); // 淡出时间
    };

    window.addEventListener("popstate", handleRouteChange);
    window.addEventListener("pre-route-change", handleRouteChange);

    return () => {
      window.removeEventListener("popstate", handleRouteChange);
      window.removeEventListener("pre-route-change", handleRouteChange);
    };
  }, []);

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
