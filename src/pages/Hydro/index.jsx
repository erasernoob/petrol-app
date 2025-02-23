import { Card } from "@arco-design/web-react"
import { hydro } from '../../data/Params'
import Sider from "../components/Sider"
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
    const { hydroData } = useSelector((state) => state.data)
    const dispatch = useDispatch()

    const [file, setFile] = useState({ name: '', path: '' })

    const handleSubmit = async (data) => {
        // TODO: 
        // if (!file.path) return
        try {
            data.file_path = file.path ? file.path : ''
            const response = await post('/hydro', JSON.stringify(data))
            const res = Papa.parse(response, { header: true, dynamicTyping: true })
            dispatch(setHydro(res.data))
            Message.success('计算成功！')
        } catch (error) {
            Message.error('计算内部出现错误，请检查')
        }
    }
    return (
        <div className="main-content">
            <Card
                title='参数输入'
                style={{
                    width: '35%',
                    height: '100%',
                }}
            >
                <Sider handleSubmit={handleSubmit} setFile={setFile}
                    file={file} form={<DynamicForm handleSubmit={handleSubmit}
                        datas={hydro} tabs={tabsName}></DynamicForm>} />
            </Card>
            <Card
                title="计算结果"
                style={{ flex: '1', marginLeft: '5px', height:'100%' }}
                bodyStyle={{ padding: '10px', height: '100%', flex: 1 }}
            >
                <ResultPage />
            </Card>
        </div>
    )
}