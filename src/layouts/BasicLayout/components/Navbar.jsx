import { Menu } from '@arco-design/web-react';
import { openUrl } from '@tauri-apps/plugin-opener';
import { useState } from 'react';
import IconData from "../../../assets/database.svg?react";
import IconDrill from "../../../assets/drill.svg?react";
import IconHydra from "../../../assets/hydra.svg?react";
import IconLimit from "../../../assets/limit.svg?react";
import IconTorque from "../../../assets/torque.svg?react";
import { routeList } from "../../../routers";


const MenuItem = Menu.Item;
const myNavigate = (item) => {
  location.hash = item
}

const icons = [<IconData />, "", <IconHydra />, <IconTorque />, <IconLimit />, <IconDrill />]

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
          justifyContent: "space-between",
          alignItems: "center",
        }}>
          {icons[idx]}
          {`${route.name}`}
        </span>
      </MenuItem>
    );
  });

  return (
    <>
      <Menu
        mode="horizontal"
        selectedKeys={selectedKeys} // 受控模式，确保选中状态生效
        style={{

        }}
      >
        {tabList}
      </Menu>

    </>
  );
}
