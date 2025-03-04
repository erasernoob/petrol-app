import { Card } from "@arco-design/web-react";
import MyForm  from '../Torque/MyForm'
import DynamicForm from '../components/DynamicForm'
import Papa from 'papaparse';
import ResultPage from "./ResultPage";
import { drill_vibration } from "../../data/Params";
import Sider from "../Limit/Sider";
import { useState } from "react";
import { post } from "../../components/axios"
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
    const [loading, setLoading] = useState(false)
    const [waiting, setWaiting] = useState(true)
    const [chartData, setChartData] = useState([])
    const [fileList, setFileList] = useState([{ name: '', path: '' }])
    const [file, setFile] = useState({ name: '', path: '' })

    const handleCalculate =  async () => {
        if (!file.path) return
        try {
            setWaiting(false)
            setLoading(true)
            const response = await post('/drill/mse', JSON.stringify({file_path: file.path}))
            const res = Papa.parse(response, { header: true, dynamicTyping: true }).data
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

    const handleExport = () => {

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
          loading={loading}
          waiting={waiting}
          handleExport={handleExport}
          chartData={chartData}
          setActiveRoute={setActiveRoute}
          activeRoute={activeRoute}
          handleCalculate={handleCalculate}
          file={file}
          setFile={setFile}
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
          <ResultPage loading={loading} chartData={chartData} waiting={waiting} />
        </Card>
      ) : (
        <></>
      )}
    </div>
  );
}
