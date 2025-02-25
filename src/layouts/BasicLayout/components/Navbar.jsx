import { Tabs, Menu, Typography} from '@arco-design/web-react';
import { routeList } from "../../../routers";
import { openUrl } from '@tauri-apps/plugin-opener';
import { useState } from 'react';

const MenuItem = Menu.Item;
const myNavigate = (item) => {
    location.hash = item
}
import styled from "styled-components";

// 自定义样式
const StyledMenu = styled(Menu)`
 }
`;

export default function NavBar() {
  const [selectedKeys, setSelectedKeys] = useState(["/"]);

  const tabList = routeList.map((route, idx) => {
    return idx !== 0 ? (
      <MenuItem
        key={route.path}
        onClick={() => {
          myNavigate(route.path);
          setSelectedKeys([route.path]);
        }}
      >
        {route.name}
      </MenuItem>
    ) : (
      <MenuItem
        key={route.path}
        type="line"
        onClick={async () => {
          await openUrl(route.path);
          setSelectedKeys([route.path]);
        }}
      >
        {route.name}
      </MenuItem>
    );
  });

  return (
    <StyledMenu
      mode="horizontal"
      selectedKeys={selectedKeys} // 受控模式，确保选中状态生效
      style={{
  }}     
    >
      {tabList}
    </StyledMenu>
  );
}
