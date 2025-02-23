import { Tabs, Menu, Typography} from '@arco-design/web-react';
import { routeList } from "../../../routers";
import { openUrl } from '@tauri-apps/plugin-opener';

const MenuItem = Menu.Item;
const myNavigate = (item) => {
    location.hash = item
}

export default function NavBar() {
    const tabList = routeList.map((route, idx) => {
        
        return (idx != 0 ?  
        <MenuItem key={route.path} type="" onClick={() => myNavigate(route.path)}>
            {route.name} </MenuItem> : <MenuItem key={route.path} type="" onClick={async () => await openUrl(route.path)}>
            {route.name} </MenuItem>
        )
    })

    return (
        <Menu mode='horizontal' theme="">
            {tabList}
        </Menu>
   )
}