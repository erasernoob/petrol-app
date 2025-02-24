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
  .arco-menu-item {
    transition: all 0.2s ease-in-out;
    padding: 10px 20px;
    border-radius: 6px;
  }

  /* 选中状态的 MenuItem */
  .arco-menu-item-selected {
    background-color: #e6f7ff !important; /* 选中时背景颜色 */
    box-shadow: inset 0px 3px 6px rgba(0, 0, 0, 0.1); /* 内阴影，形成按下的感觉 */
    border: 2px solid #1890ff !important; /* 选中时添加边框 */
    font-weight: bold;
  }

  /* 悬停效果 */
  .arco-menu-item:hover {
    background-color: rgba(24, 144, 255, 0.1);
    transition: all 0.2s;
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
    >
      {tabList}
    </StyledMenu>
  );
}
