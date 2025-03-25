import { Menu } from '@arco-design/web-react';
import { openUrl } from '@tauri-apps/plugin-opener';
import { useState } from 'react';
import IconHydra from "../../../assets/hydra.svg?react";
import IconTorque from "../../../assets/torque.svg?react";
import IconDrill from "../../../assets/drill.svg?react";
import IconLimit from "../../../assets/limit.svg?react";
import IconData from "../../../assets/database.svg?react";
import styled from "styled-components";
import { routeList } from "../../../routers";


const MenuItem = Menu.Item;
const myNavigate = (item) => {
  location.hash = item
}

const icons = [<IconData />, "", <IconHydra />, <IconTorque />, <IconLimit />, <IconDrill />]

// 自定义样式
const StyledMenu = styled(Menu)`
 }
`;

export default function NavBar() {
  const [selectedKeys, setSelectedKeys] = useState(["/hydro"]);
  const tabList = routeList.map((route, idx) => {
    if (idx === 1) { return <></> }
    return idx !== 0 ? (
      <>
        <MenuItem
          key={route.path}
          onClick={() => {
            myNavigate(route.path);
            setSelectedKeys([route.path]);
          }}
        >
          <span style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}>
            {icons[idx]}
            {route.name}
          </span>
        </MenuItem>

      </>
    ) : (
      <MenuItem
        key={route.path}
        type="line"
        onClick={async () => {
          await openUrl(route.path);
          setSelectedKeys([route.path]);
        }}
      >
        <span style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}>
          {icons[idx]}
          {route.name}
        </span>
      </MenuItem>
    );
  });

  return (
    <>
      <StyledMenu
        mode="horizontal"
        selectedKeys={selectedKeys} // 受控模式，确保选中状态生效
        style={{

        }}
      >
        {tabList}
      </StyledMenu>

    </>
  );
}
