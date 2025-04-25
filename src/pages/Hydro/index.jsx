import { Card, Message } from "@arco-design/web-react";
import Papa from 'papaparse';
import { useState } from 'react';
import { post } from '../../components/axios';
import { hydro } from '../../data/Params';
import DynamicForm from "../components/DynamicForm";
import '../style.css';
import { dealWithTheDataUnit } from "../utils/utils";
import ResultPage from "./ResultPage";
import Sider from "./Sider";

const tabsName = ['基本参数', '钻井液', '钻头', '钻杆接头', '地面管汇', '岩屑床']
export default function HydroPage() {
    const [file, setFile] = useState({ name: '', path: '' })
    const [loading, setLoading] = useState(false)
    // 等待开始计算
    const [waiting, setWaiting] = useState(true)
    const [chartData, setChartData] = useState([])
    const [extraData, setExtraData] = useState({})
    const handleSubmit = async (data) => {
        if (!file.path) return
        try {
            data.file_path = file.path ? file.path : ''
            setWaiting(false)
            setLoading(true)
            // 单位换算
            dealWithTheDataUnit(data, 1)

            const response = await post('/hydro', JSON.stringify(data))
            const res = Papa.parse(response, { header: true, dynamicTyping: true })

            setChartData(res.data.map(item => ({
                depth: item["井深 (m)"],
                // TODO: for test 
                drillPressure: item['钻柱压力 (Pgn, MPa)'],
                annularPressure: item["环空压力 (Phk, MPa)"],
                ecd: item["ECD (g/cm³)"]
            })))

            // 第二次请求
            const values = await post('/hydro/data')
            setExtraData(values)
            setLoading(false)
        } catch (error) {
            setLoading(false)
            setWaiting(true)
            Message.error(error?.message)
            Message.error('计算内部出现错误，请检查输入参数！')
        }
    }
    return (
        <div className="main-content">
            <Card
                title='参数'
                style={{
                    width: '30%',
                    height: '100%',
                }}
            >
                <Sider handleSubmit={handleSubmit} setFile={setFile}
                    file={file} form={<DynamicForm file={file} handleSubmit={handleSubmit}
                        datas={hydro} tabs={tabsName}></DynamicForm>} />
            </Card>
            <Card
                title="计算结果"
                style={{ flex: '1', marginLeft: '5px', height: '100%' }}
                bodyStyle={{ padding: '10px', height: '100%', flex: 1 }}
            >
                <ResultPage waiting={waiting} data={extraData} loading={loading} chartData={chartData} />
            </Card>
        </div>
    )
}