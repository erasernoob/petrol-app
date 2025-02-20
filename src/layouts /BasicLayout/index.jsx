import { Layout, Grid } from "@arco-design/web-react"
import "./style.css"
import NavBar from "./components/Navbar";
import InputSider from "./components/InputSider"
import ResultContent from "./components/ResultContent";


const Sider = Layout.Sider;
const Footer = Layout.Footer;
const Content = Layout.Content;
const Row = Grid.Row
const Col = Grid.Col


export default function BasicLayout() {

    
    return (
        <div className="basic-layout">
            <Layout style={{ height: '100%' }}>
                <NavBar />
                <Layout>
                    <Sider className={"input-sider"} style={{width: '30%', marginRight:'5px'}}>
                    <InputSider />
                    </Sider>
                    <Content style={{height: '100%', width: 'calc(70%)'}}>
                        <ResultContent>

                        </ResultContent>
                    </Content>
               </Layout>
            </Layout>
        </div>
    )

}