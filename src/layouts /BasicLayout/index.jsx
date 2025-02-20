import { Layout, Grid } from "@arco-design/web-react"
import "./style.css"
import NavBar from "./components/Navbar";
import InputPage from "./components/InputPage"
import ResultPage from "./components/ResultPage";
import { Outlet } from "react-router-dom";


const Sider = Layout.Sider;
const Content = Layout.Content;
const Header = Layout.Header;

export default function BasicLayout() {

    
    return (
        <div className="basic-layout">
            <Layout style={{ height: '100%' }}>
                    <NavBar />
                <Layout>
                    <Sider className={"input-sider"} style={{width: '30%', marginRight:'5px'}}>
                    <InputPage />
                    </Sider>
                    <Content style={{height: '100%', width: 'calc(70%)'}}>
                        <ResultPage />
                    </Content>
               </Layout>
            </Layout>
        </div>
    )

}