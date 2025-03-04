import { Card, Message } from "@arco-design/web-react"
import ResultPage from '../components/ResultPage'
import { useState, useEffect, useMemo } from 'react'
import Sider from "./Sider"
import MyForm from "./MyForm"
import Option from "../option"
import { torque } from '../../data/Params'
import Papa from 'papaparse';
import { post } from "../../components/axios"

const options = ['轴向力', '扭矩']

export default function TorquePage() {
    const [fileList, setFileList] = useState({orbit: {name: '', path: ''}, drill: {name: '', path: ''}})
    const [loading, setLoading] = useState(false)
    const [waiting, setWaiting] = useState(true)
    const [torqueData, setTorqueData]  = useState([])

    const chartData = useMemo(() => {
        return torqueData.map((item) => ({
            Sk: item['Sk'],
            T: item['T'],
            M: item['M'],
        }))
    }, [torqueData])
    console.log(chartData)
    const heatData = useMemo(() => {
        return torqueData.map((item) => ({
            M: item['M'],
            T: item['T'],
            N: item['N'],
            E: item['E'],
            TCS: item['TCS'],
        }))
    }, [torqueData])
    console.log(heatData)
    const handleSubmit = async (data) => {
        try {
            data.file_path1 = fileList.orbit.path
            data.file_path2 = fileList.drill.path
            // console.log(fileList)
            setWaiting(false)
            setLoading(true)
            console.log(data)
            const response = await post('/torque', JSON.stringify(data))
            const res = Papa.parse(response, { header: true, dynamicTyping: true })
            // TODO: DEV FIX CHARTDATA
            setTorqueData(res.data)
            setLoading(false)
            Message.success('数据获取成功！')
        } catch (error) {
            console.log(error)
            setLoading(false)
            // setFileList([{ name: '', path: '' }])
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
            name: '轴向力 (kN)',
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '轴向力 (kN)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'T', y: 'Sk' },
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
            name: '扭矩 (kN·m） ',
            type: 'value',
            position: 'top',
        },
    ], [
        {
            name: '扭矩 (kN·m）',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'M', y: 'Sk' },
            sampling: 'lttb', // 采用最佳采样算法
            smooth: true,     // 禁用平滑
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