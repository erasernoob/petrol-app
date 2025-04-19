import { Menu, Popover } from "@arco-design/web-react";
import { openUrl } from "@tauri-apps/plugin-opener";
import { useState } from "react";
import IconData from "../../../assets/database.svg?react";
import IconDrill from "../../../assets/drill.svg?react";
import IconHydra from "../../../assets/hydra.svg?react";
import IconLimit from "../../../assets/limit.svg?react";
import IconRisk from "../../../assets/risk.svg?react";
import IconTorque from "../../../assets/torque.svg?react";
import { routeList } from "../../../routers";

const MenuItem = Menu.Item;
const myNavigate = (item) => {
  location.hash = item;
};

const icons = [
  <IconData />,
  "",
  <IconHydra />,
  <IconTorque />,
  <IconLimit />,
  <IconDrill />,
  <IconRisk />,
];

export default function NavBar() {
  const [selectedKeys, setSelectedKeys] = useState(["/hydro"]);
  const [popupVisible, setPopupVisible] = useState(false);
  const tabList = routeList.map((route, idx) => {
    if (idx === 1) {
      return <></>;
    }

    // 钻头状态监测菜单（最后一个）
    if (idx === 5) {
      const popoverContent = (
        <div
          style={{
            padding: "10px",
            borderRadius: "4px",
            boxShadow: "0 2px 8px rgba(0, 0, 0, 0.15)",
            backgroundColor: "white",
          }}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "space-between",
              gap: "8px",
            }}
          >
            <div
              style={{
                padding: "10px 10px",
                cursor: "pointer",
                borderRadius: "4px",
                textAlign: "center",
                transition: "all 0.3s",
                border: "1px solid #e5e6eb",
                flex: 1,
              }}
              onClick={() => {
                localStorage.setItem("drillActiveRoute", "1");
                const newPath = `${route.path}?type=1&t=${Date.now()}`;
                myNavigate(newPath);
                setSelectedKeys([route.path]);
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor =
                  "rgba(77, 153, 204, 0.15)";
                e.currentTarget.style.color = "#0066B3";
                e.currentTarget.style.border = "1px solid #0066B3";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = "transparent";
                e.currentTarget.style.color = "inherit";
                e.currentTarget.style.border = "1px solid #e5e6eb";
              }}
            >
              <div style={{ fontWeight: "500", fontSize: "15px" }}>MSE</div>
            </div>

            <div
              style={{
                padding: "10px 10px",
                cursor: "pointer",
                borderRadius: "4px",
                textAlign: "center",
                transition: "all 0.3s",
                border: "1px solid #e5e6eb",
                flex: 1,
                width: "100px"
              }}
              onClick={() => {
                localStorage.setItem("drillActiveRoute", "2");
                const newPath = `${route.path}?type=2&t=${Date.now()}`;
                myNavigate(newPath);
                setSelectedKeys([route.path]);
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor =
                  "rgba(77, 153, 204, 0.15)";
                e.currentTarget.style.color = "#0066B3";
                e.currentTarget.style.border = "1px solid #0066B3";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = "transparent";
                e.currentTarget.style.color = "inherit";
                e.currentTarget.style.border = "1px solid #e5e6eb";
              }}
            >
              <div style={{ fontWeight: "500", fontSize: "15px" }}>
                粘滑振动
              </div>
            </div>
          </div>
        </div>
      );

      return (
        <Popover
          content={popoverContent}
          position="bottom"
          trigger="hover"
          className="submenu-popover"
          popupVisible={popupVisible}
          onVisibleChange={(visible) => setPopupVisible(visible)}
        >
          <MenuItem
            key={route.path}
            onClick={() => {
              const storedValue =
                localStorage.getItem("drillActiveRoute") || "1";
              localStorage.setItem("drillActiveRoute", storedValue);
              const newPath = `${route.path
                }?type=${storedValue}&t=${Date.now()}`;
              myNavigate(newPath);
              setSelectedKeys([route.path]);
            }}
          >
            <span
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              {icons[idx]}
              <span
                style={{
                  whiteSpace: "nowrap",
                  margin: "0px",
                }}
              >
                {route.name}
              </span>
            </span>
          </MenuItem>
        </Popover>
      );
    }

    return idx !== 0 ? (
      <MenuItem
        key={route.path}
        onClick={() => {
          myNavigate(route.path);
          setSelectedKeys([route.path]);
        }}
      >
        <span
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          {icons[idx]}
          <span
            style={{
              whiteSpace: "nowrap",
              margin: "0px",
              marginLeft: idx === 4 ? "2px" : "0px",
            }}
          >
            {route.name}
          </span>
        </span>
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
        <span
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            whiteSpace: "nowrap", // 防止换行
          }}
        >
          {icons[idx]}
          <span style={{ whiteSpace: "nowrap", margin: "0px" }}>
            {route.name}
          </span>
        </span>
      </MenuItem>
    );
  });

  return (
    <>
      <style jsx global>{`
        .submenu-popover .arco-popover-content {
          padding: 0;
          border-radius: 4px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }
      `}</style>
      <Menu mode="horizontal" selectedKeys={selectedKeys}>
        {tabList}
      </Menu>
    </>
  );
}
