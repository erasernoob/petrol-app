import { Card } from "@arco-design/web-react"
import Papa from 'papaparse'
import { useState } from 'react'
import { post } from "../../components/axios"
import { torque } from '../../data/Params'
import { dealWithTheDataUnit, handleTheError } from "../utils/utils"
import MyForm from "./MyForm"
import ResultPage from "./ResultPage"
import Sider from "./Sider"

const options = ['轴向力', '扭矩']
const work_conditions = ['旋转钻进', '滑动钻进', '起钻', '下钻', '倒划眼']

export default function TorquePage() {
    const [fileList, setFileList] = useState({ orbit: { name: '', path: '' }, drill: { name: '', path: '' } })
    const [loading, setLoading] = useState(false)
    const [waiting, setWaiting] = useState(true)
    const [chartData, setChartData] = useState([])
    const [heatData, setHeatData] = useState([])
    const [condition, setCondition] = useState(work_conditions[0])

    const handleSubmit = async (data) => {
        try {
            data.file_path1 = fileList.orbit.path
            data.file_path2 = fileList.drill.path
            // console.log(fileList)
            setWaiting(false)
            setLoading(true)
            // Get rid of the 422 Unprocessable Entity in backend
            if (data.wc != 1 && data.wc != 5) {
                data.v = 0
                data.omega = 0
            }
            dealWithTheDataUnit(data, 2)
            const response = await post('/torque', JSON.stringify(data))
            const res = Papa.parse(response, { header: true, dynamicTyping: true }).data
            // TODO: DEV FIX CHARTDATA

            setChartData(res.map(({ Sk, T, M }) => ({ Sk, T, M })))
            setHeatData(res.map(({ M, T, N, E, TCS }) => ({ M, T, N, E, TCS })))
            setCondition(work_conditions[data.wc - 1])
            setLoading(false)
        } catch (error) {
            console.log(error)
            setLoading(false)
            // setFileList([{ name: '', path: '' }])
            setWaiting(true)
            handleTheError(error)
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
                <Sider datas={torque} fileList={fileList} setFileList={setFileList} form={<MyForm datas={torque} handleSubmit={handleSubmit} fileList={fileList} />} />
            </Card>
            <Card
                title="计算结果"
                style={{ flex: '1', marginLeft: '5px' }}
                bodyStyle={{ padding: '10px', height: '100%', flex: 1 }}
            >
                <ResultPage curCondition={condition} chartData={chartData} heatData={heatData} typeOptions={options} loading={loading} waiting={waiting} />
            </Card>
        </div>
    )
}