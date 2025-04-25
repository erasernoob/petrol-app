import { Card, Message } from "@arco-design/web-react";
import Papa from 'papaparse';
import { useEffect, useState } from "react";
import { post } from "../../components/axios";
import {
  limit_curve,
  limit_eye,
  limit_hydro,
  limit_mechanism,
} from "../../data/Params";
import DynamicForm from "../components/DynamicForm";
import MyForm from "../Torque/MyForm";
import { dealWithTheDataUnit } from "../utils/utils";
import ResultPage from "./ResultPage";
import Sider from "./Sider";

const tabs = [
  ["基本参数", "钻井液", "岩屑床"],
  ["基本参数", "钻井液", "钻头", "钻杆接头", "地面管汇", "岩屑床"],
];
const workConditions = ['旋转钻进', '滑动钻进', '起钻', '下钻', '倒划眼']
const subRoutesOptions = [
  { label: "裸眼延伸极限", value: 1 },
  { label: "水力延伸极限", value: 2 },
  { label: "机械延伸极限", value: 3 },
  // { label: "屈曲临界载荷", value: 4 },
];

export const defaultFileList = { orbit: { name: '', path: '' }, drill: { name: '', path: '' } }
const postPath = ['/limit/eye', '/limit/hydro', '/limit/mechanism', '/limit/curve']
const typeOptions = [
  [],
  // ['总循环压耗', '立管压力'],
  ['总循环压耗'],
  ['井口轴向力', '井口扭矩', '安全系数'],
  ['井口轴向力', '井口扭矩', '安全系数', '屈曲临界载荷'],
]

export default function LimitPage() {
  const [loading, setLoading] = useState(false)
  const [waiting, setWaiting] = useState(true)
  const [chartData, setChartData] = useState([])
  const [condition, setCondition] = useState(workConditions[0])

  // 是否计算屈曲
  const [calcCurve, setCalcCurve] = useState(false)
  const [curveData, setCurveData] = useState([])
  const [curveFile, setCurveFile] = useState(null)

  const [activeRoute, setActiveRoute] = useState(1);
  const [fileList, setFileList] = useState(defaultFileList);
  const [file, setFile] = useState({ name: '', path: '' })

  useEffect(() => {
    setWaiting(true)
    setLoading(false)
    setChartData([])
    setFile({ name: '', path: '' })
    setFileList(defaultFileList)
  }, [activeRoute])

  // 还原之前的计算
  useEffect(() => {
    setCalcCurve(false)
    setCurveData([])
    setCurveFile(null)
  }, [])


  const handleSubmit = async (data) => {
    try {

      if (activeRoute <= 2) {
        data.file_path = file.path
        dealWithTheDataUnit(data, 1)
      } else {
        data.file_path1 = fileList.orbit.path
        data.file_path2 = fileList.drill.path
      }
      setWaiting(false)
      setLoading(true)

      if (activeRoute == 3 && data.wc != 1 && data.wc != 5) {
        data.v = 0
        data.omega = 0
      }

      // 处理单位换算
      if (activeRoute == 3) {
        dealWithTheDataUnit(data, 2)
      } else if (activeRoute == 4) {
        dealWithTheDataUnit(data, 3)
      }

      const response = await post(postPath[activeRoute - 1], JSON.stringify(data))
      const res = Papa.parse(response, { header: true, dynamicTyping: true }).data


      if (activeRoute === 3 && data.calcCurve === 1) {
        setCalcCurve(true)

        console.log("进入计算curve逻辑")
        const response2 = await post('/limit/mechanism/curve', JSON.stringify(data))
        setCurveFile(response2)
        const res2 = Papa.parse(response2, { header: true, dynamicTyping: true }).data
        setCurveData(res2)
      } else {
        setCalcCurve(false)
      }

      setChartData(res)
      setLoading(false)
      setCondition(workConditions[data.wc - 1])
    } catch (error) {
      console.log(error)
      setLoading(false)
      setWaiting(true)
      Message.error(error?.message);
      Message.error('计算内部出现错误，请检查输入参数！')
    }
  }

  const formList = [
    <DynamicForm key={1} handleSubmit={handleSubmit} datas={limit_eye} tabs={tabs[0]} file={file} limit={true}></DynamicForm>,
    <DynamicForm key={2} handleSubmit={handleSubmit} datas={limit_hydro} tabs={tabs[1]} file={file} limit={true}></DynamicForm>,
    <MyForm key={3} handleSubmit={handleSubmit} datas={limit_mechanism} fileList={fileList} limit={true} />,
    <MyForm key={4} handleSubmit={handleSubmit} datas={limit_curve} fileList={fileList} limit={true} />,
  ];



  return (
    <div className="main-content">
      <Card
        title="参数"
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
        <ResultPage curCondition={condition} curveFile={curveFile} curveData={curveData} activeRoute={activeRoute} chartData={chartData} typeOptions={calcCurve ? typeOptions[typeOptions.length - 1] : typeOptions[activeRoute - 1]} loading={loading} waiting={waiting} />
      </Card>
    </div>
  );
}
