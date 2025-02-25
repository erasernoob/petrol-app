import { Card } from "@arco-design/web-react"
import ResultPage from "./ResultPage"
import { useState } from 'react'
import Sider from "./Sider"
import MyForm from "./MyForm"
import { torque  } from '../../data/Params'
export default function TorquePage() {
    const [fileList, setFileList] = useState([{ name: '', path: '' }])
    const [loading, setLoading] = useState(false)

    const datas = torque

    const handleSubmit = async () => {
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
                <Sider datas={datas} fileList={fileList} setFileList={setFileList} form={<MyForm handleSubmit={handleSubmit} fileList={fileList} />} />
            </Card>
            <Card
                title="计算结果"
                style={{ flex: '1', marginLeft: '5px'}}
                bodyStyle={{ padding: '10px', height: '100%', flex: 1 }}
            >
                <ResultPage />
            </Card>
        </div>
    )
}