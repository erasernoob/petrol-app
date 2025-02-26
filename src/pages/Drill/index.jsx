import { Card } from "@arco-design/web-react";
import ResultPage from "./ResultPage";
import Sider from "../Limit/Sider";
import { useState } from "react";
import { Message } from "@arco-design/web-react";

const subRoutesOptions = [
  { label: "MSE", value: 1 },
  { label: "黏滑振动", value: 2 },
];

export default function DrillPage() {
    const [activeRoute, setActiveRoute] = useState(1);
    const [fileList, setFileList] = useState([{ name: '', path: '' }])
    const handleCalculate =  async () => {
        Message.success('计算成功')
    }

  return (
    <div className="main-content">
      <Card
        title="参数输入"
        style={{
          width: "30%",
          height: "100%",
        }}
      >
        <Sider
          subRouteOptions={subRoutesOptions}
          setActiveRoute={setActiveRoute}
          activeRoute={activeRoute}
          fileList={fileList}
          setFileList={setFileList}
        />
      </Card>
      {activeRoute === 2 ? (
        <Card
          title="计算结果"
          style={{ flex: "1", marginLeft: "5px" }}
          bodyStyle={{ padding: "10px", height: "100%", flex: 1 }}
        >
          <ResultPage />
        </Card>
      ) : (
        <></>
      )}
    </div>
  );
}
