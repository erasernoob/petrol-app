import { Card, Watermark } from "@arco-design/web-react"
import { hydro } from '../../data/Params'
import Sider from "./Sider"
import ResultPage from "./ResultPage"
import { post } from '../../components/axios';
import '../style.css'
import { useSelector, useDispatch } from 'react-redux';
import { useState } from 'react';
import Papa from 'papaparse';
import { setHydro } from '../../store/dataSlice';
import DynamicForm from "../components/DynamicForm"
import { Message } from "@arco-design/web-react";

const tabsName = ['基本参数', '钻井液', '钻头', '钻杆接头', '地面管汇', '岩屑床']
export default function HydroPage() {
    const dispatch = useDispatch()
    const [file, setFile] = useState({ name: '', path: '' })
    const [loading, setLoading] = useState(false)
    // 等待开始计算
    const [waiting, setWaiting] = useState(true)
    const [extraData, setExtraData] = useState({})
    const handleSubmit = async (data) => {
        if (!file.path) return
        try {
            data.file_path = file.path ? file.path : ''
            setWaiting(false)
            setLoading(true)
            const response = await post('/hydro', JSON.stringify(data))
            const res = Papa.parse(response, { header: true, dynamicTyping: true })
            dispatch(setHydro(res.data))
            // 第二次请求
            const values = await post('/hydro/data')
            setExtraData(values)
            setLoading(false)
            Message.success('数据获取成功！')
        } catch (error) {
            setLoading(false)
            setWaiting(true)
            Message.error('计算内部出现错误，请检查')
        }
    }
    return (
        <div className="main-content">
            <Card
                title='参数输入'
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
                style={{ flex: '1', marginLeft: '5px', height:'100%' }}
                bodyStyle={{ padding: '10px', height: '100%', flex: 1 }}
            >
                <ResultPage waiting={waiting} data={extraData} loading={loading} />
            </Card>
        </div>
    )
}