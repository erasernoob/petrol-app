import { Card, Message } from "@arco-design/web-react"
import ResultPage from '../components/ResultPage'
import { useState } from 'react'
import Sider from "./Sider"
import MyForm from "./MyForm"
import Option from "../option"
import { torque } from '../../data/Params'
import { post } from "../../components/axios"



const options = ['轴向力', '扭矩']

export default function TorquePage() {
    const [fileList, setFileList] = useState([{ name: '', path: '' }])
    const [loading, setLoading] = useState(false)
    const [waiting, setWaiting] = useState(true)
    const [chartData, setChartData] = useState([])

    const handleSubmit = async (data) => {
        try {
            data.file_path1 = fileList[0].path
            data.file_path2 = fileList[1].path
            console.log(fileList)
            setWaiting(false)
            setLoading(true)
            const response = await post('/torque', JSON.stringify(data))
            const res = Papa.parse(response, { header: true, dynamicTyping: true })
            setChartData(res.data)
            setLoading(false)
            Message.success('数据获取成功！')
        } catch (error) {
            setLoading(false)
            setFileList([{ name: '', path: '' }])
            setWaiting(true)
            Message.error('计算内部出现错误，请检查')
        }

    }
    const option2 = Option(chartData,
        {
            type: 'value',
            name: '井深 (m)',
            inverse: true
        }, [
        {
            name: 'ECD (g/cm³)',
            type: 'value',
            offset: 0,
            alignTicks: true
        }
    ], [
        {
            name: 'ECD',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'ecd', y: 'depth' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1 },
            showSymbol: false
        }
    ],)
    const option1 = Option(
        chartData,
        {
            type: 'value',
            name: '井深 (m)',
            inverse: true
        }, [
        {
            name: '压力 (MPa)',
            type: 'value',
            position: 'top',
            axisLabel: {
                formatter: function (value) {
                    return value == 0 ? '' : value
                }
            }
        },
    ], [
        {
            name: '钻柱压力',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'drillPressure', y: 'depth' },
            sampling: 'lttb', // 采用最佳采样算法
            smooth: true,     // 禁用平滑
            lineStyle: { width: 2 },
            showSymbol: false
        },
        {
            name: '环空压力',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'annularPressure', y: 'depth' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 2 },
            showSymbol: false
        },
    ],
    )
    const chartOptions = [option1, option2]





    return (
        <div className="main-content">
            <Card
                title='参数输入'
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
                <ResultPage options={options} loading={loading} waiting={waiting} />
            </Card>
        </div>
    )
}