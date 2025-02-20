import { Tabs, Typography} from '@arco-design/web-react';
import { routeList } from "../../../routers";

const style = {

};

const myNavigate = (item) => {
    location.hash = item
}

const { TabPane } = Tabs

export default function NavBar() {
    const tabList = routeList.map((route, idx) => {
        return <TabPane key={route.path} title={route.name} style={style}>
        </TabPane>
    })

    return (
        <Tabs className={"nav-bar"} type={"card"} size="large" onChange={(key) => myNavigate(key)}>
            {tabList}
        </Tabs>

   )
}