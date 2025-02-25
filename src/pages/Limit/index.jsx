import { Card } from "@arco-design/web-react"
import { useState } from 'react'
import ResultPage from "./ResultPage"
import Sider from "./Sider"
import DynamicForm from "../components/DynamicForm"
import { limit_curve, limit_eye, limit_hydro, limit_mechanism } from "../../data/Params"
import MyForm from "../Torque/MyForm"

const tabs = [['基本参数', '钻井液'], ['基本参数', '钻井液', '钻头', '钻杆接头', '地面管汇', '岩屑床']]

const formList = 
[
    <DynamicForm datas={limit_eye} tabs={tabs[0]} file={''}>
    </DynamicForm>,
    <DynamicForm datas={limit_hydro} tabs={tabs[1]} file={''}>
    </DynamicForm>,
    <MyForm datas={limit_mechanism} fileList={[]} />,
    <MyForm datas={limit_curve} fileList={[]} />
]


export default function DrillPage() {
    const [activeRoute, setActiveRoute] = useState(1)
    const form = formList[activeRoute - 1]
    return (
        <div className="main-content">
            <Card
                title='参数输入'
                style={{
                    width: '30%',
                    height: '100%',
                }}
            >
                <Sider activeRoute={activeRoute} setActiveRoute={setActiveRoute} form={form}  />
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