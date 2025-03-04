import { Card } from "@arco-design/web-react";
import { useState } from "react";
import ResultPage from "./ResultPage";
import Sider from "./Sider";
import DynamicForm from "../components/DynamicForm";
import {
  limit_curve,
  limit_eye,
  limit_hydro,
  limit_mechanism,
} from "../../data/Params";
import MyForm from "../Torque/MyForm";

const tabs = [
  ["基本参数", "钻井液"],
  ["基本参数", "钻井液", "钻头", "钻杆接头", "地面管汇", "岩屑床"],
];
const subRoutesOptions = [
  { label: "裸眼延伸极限", value: 1 },
  { label: "水力延伸极限", value: 2 },
  { label: "机械延伸极限", value: 3 },
  { label: "屈曲临界载荷", value: 4 },
];

export const defaultFileList = {orbit: {name: '', path: ''}, drill: {name: '', path: ''}}



export default function LimitPage() {
  const [activeRoute, setActiveRoute] = useState(1);
  const [fileList, setFileList] = useState(defaultFileList);
  const [file, setFile] = useState({name: '', path: ''})
  const formList = [
  <DynamicForm datas={limit_eye} tabs={tabs[0]} file={file}></DynamicForm>,
  <DynamicForm datas={limit_hydro} tabs={tabs[1]} file={file}></DynamicForm>,
  <MyForm datas={limit_mechanism} fileList={fileList} />,
  <MyForm datas={limit_curve} fileList={fileList} />,
];


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
          fileList={fileList}
          setFile={setFile}
          setFileList={setFileList}
          subRouteOptions={subRoutesOptions}
          activeRoute={activeRoute}
          setActiveRoute={setActiveRoute}
          form={formList[activeRoute - 1]}
        />
      </Card>
      <Card
        title="计算结果"
        style={{ flex: "1", marginLeft: "5px" }}
        bodyStyle={{ padding: "10px", height: "100%", flex: 1 }}
      >
        <ResultPage />
      </Card>
    </div>
  );
}
