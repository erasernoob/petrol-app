import { Card } from "@arco-design/web-react"
import ResultPage from "./ResultPage"
import Sider from "../components/Sider"
export default function DrillPage() {
    return (
        <div className="main-content">
            <Card
                title='参数输入'
                style={{
                    width: '35%',
                    height: '100%',
                }}
            >
                <Sider />
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