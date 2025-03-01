import { Layout, Grid } from "@arco-design/web-react"
import "./style.css"
import NavBar from "./components/Navbar";
import { Outlet, RouterProvider } from "react-router-dom";
import { useEffect, useState }from 'react'
import routerList from "../../routers";

const Sider = Layout.Sider;
const Content = Layout.Content;
const Header = Layout.Header;

export default function BasicLayout() {

    const [visible, setVisible] = useState(false);
    useEffect(() => {
        setTimeout(() => setVisible(true), 100); // 100ms 后触发动画
    }, []);

    return (
        <div className={`basic-layout fade-in ${visible ? "visible" : ""} `}>
            <NavBar />
        <div className="content">
            <RouterProvider router={routerList}></RouterProvider>
        </div>
        </div>
   )

}