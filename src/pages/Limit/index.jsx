import { Card, Message } from "@arco-design/web-react";
import { useState, useEffect } from "react";
import ResultPage from "./ResultPage";
import Sider from "./Sider";
import Papa from 'papaparse';
import { post } from "../../components/axios"
import DynamicForm from "../components/DynamicForm";
import {
  limit_curve,
  limit_eye,
  limit_hydro,
  limit_mechanism,
} from "../../data/Params";
import MyForm from "../Torque/MyForm";

const tabs = [
  ["基本参数", "钻井液", "岩屑床"],
  ["基本参数", "钻井液", "钻头", "钻杆接头", "地面管汇", "岩屑床"],
];
const subRoutesOptions = [
  { label: "裸眼延伸极限", value: 1 },
  { label: "水力延伸极限", value: 2 },
  { label: "机械延伸极限", value: 3 },
  { label: "屈曲临界载荷", value: 4 },
];

export const defaultFileList = { orbit: { name: '', path: '' }, drill: { name: '', path: '' } }
const postPath = ['/limit/eye', '/limit/hydro', '/limit/mechanism', '/limit/curve']
const typeOptions = [
  [],
  ['总循环压耗', '立管压力'],
  ['井口轴向力', '井口扭矩', '安全系数'],
  ['正弦屈曲临界载荷', '螺旋屈曲临界载荷'],
]

export default function LimitPage() {
  const [loading, setLoading] = useState(false)
  const [waiting, setWaiting] = useState(true)
  const [chartData, setChartData] = useState([])
  const [activeRoute, setActiveRoute] = useState(1);
  const [fileList, setFileList] = useState(defaultFileList);
  const [file, setFile] = useState({ name: '', path: '' })

  useEffect(() => {
      console.log(activeRoute)
      setWaiting(true)
      setLoading(false)
      setChartData([])
      setFile({name: '', path: ''})
      setFileList(defaultFileList)
    }, [activeRoute])
  

  const handleSubmit = async (data) => {
    try {
      if (activeRoute <= 2) {
        data.file_path = file.path
      } else {
        data.file_path1 = fileList.orbit.path
        data.file_path2 = fileList.drill.path
      }
      setWaiting(false)
      setLoading(true)
      const response = await post(postPath[activeRoute - 1], JSON.stringify(data))
      console.log(data)
      const res = Papa.parse(response, { header: true, dynamicTyping: true }).data
      console.log(res)
      setChartData(res)
      setLoading(false)
      Message.success('数据获取成功！')
    } catch (error) {
      console.log(error)
      setLoading(false)
      setWaiting(true)
      Message.error('计算内部出现错误，请检查')
    }
  }
  
  const formList = [
    <DynamicForm handleSubmit={handleSubmit} datas={limit_eye} tabs={tabs[0]} file={file}></DynamicForm>,
    <DynamicForm handleSubmit={handleSubmit} datas={limit_hydro} tabs={tabs[1]} file={file}></DynamicForm>,
    <MyForm  handleSubmit={handleSubmit} datas={limit_mechanism} fileList={fileList} />,
    <MyForm handleSubmit={handleSubmit} datas={limit_curve} fileList={fileList} />,
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
          setWaiting={setWaiting}
          setLoading={setLoading}
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
        <ResultPage activeRoute={activeRoute} chartData={chartData} typeOptions={typeOptions[activeRoute - 1]} loading={loading} waiting={waiting} />
      </Card>
    </div>
  );
}
