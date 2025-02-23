import { Card } from "@arco-design/web-react"
import Sider from "./Sider"
export default function HydroPage() {
    return (
        <div className="main-content">
            <Card
                title='参数输入'
                style={{
                    width: '100%',
                    height: '100%',
                    maxWidth: 'calc(100% - 1.7px)',
                    // fontSize: '10px',
                    height: 'calc(100% - 2px)'
                }}
            >
                <Sider />
            </Card>
            <Card>
                {/* <Resultpage  */}
            </Card>
        </div>
    )
}