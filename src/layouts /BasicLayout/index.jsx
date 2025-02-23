import { Layout, Grid } from "@arco-design/web-react"
import "./style.css"
import NavBar from "./components/Navbar";
import { Outlet, RouterProvider } from "react-router-dom";
import routerList from "../../routers";


const Sider = Layout.Sider;
const Content = Layout.Content;
const Header = Layout.Header;

export default function BasicLayout() {

    return (
        <>
        <NavBar />
        <div className="basic-layout">
            <RouterProvider router={routerList}></RouterProvider>
        </div>
        </>
   )

}