import { Card } from "@arco-design/web-react";
import MyForm  from '../Torque/MyForm'
import DynamicForm from '../components/DynamicForm'
import ResultPage from "./ResultPage";
import { drill_vibration } from "../../data/Params";

import Sider from "../Limit/Sider";
import { useState } from "react";
import { Message } from "@arco-design/web-react";

const subRoutesOptions = [
  { label: "MSE", value: 1 },
  { label: "黏滑振动", value: 2 },
];
const tabs = [
    '基本钻具参数',
    '钻井液',
    '计算参数',
]

export default function DrillPage() {
    const [activeRoute, setActiveRoute] = useState(1);
    const [fileList, setFileList] = useState([{ name: '', path: '' }])
    const handleCalculate =  async () => {
        Message.success('计算成功')
    }

    const handleSubmit = async () => {
    }

  return (
    <div className="main-content">
      <Card
        title="参数输入"
        style={{
          width: activeRoute === 1 ? '100%' : '30%',
          height: "100%",
        }}
      >
        <Sider
          subRouteOptions={subRoutesOptions}
          setActiveRoute={setActiveRoute}
          activeRoute={activeRoute}
          fileList={fileList}
          form={activeRoute === 2 ? <DynamicForm datas={drill_vibration} handleSubmit={handleSubmit} tabs={tabs} file={{name: '', path: ''}}/> : 'default'}
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
