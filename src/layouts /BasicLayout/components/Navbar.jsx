import { Layout } from "@arco-design/web-react"
import { Tabs, Typography} from '@arco-design/web-react';
import { modules } from "../../../store/module"

const style = {
//   textAlign: 'center',
//   marginTop: 20,
//   padding: "20px"

};

const TabPane = Tabs.TabPane
const Header = Layout.Header

export default function NavBar() {
    const tabList = modules.map((module, idx) => {
        return <TabPane key={idx} title={module.title} style={style} disabled={idx == 0} ></TabPane>
    })
    return (
        <>
        <Tabs className={"nav-bar"} type={"card"} size="large">
            {tabList}
        </Tabs>
        </>

   )
   
}