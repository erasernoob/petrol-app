import { Card, Message } from "@arco-design/web-react"
import { useState } from "react"
import { post } from "../../components/axios"
import ResultPage from "./ResultPage"
import Sider from "./Sider"
export default function DrillPage() {
    const [loading, setLoading] = useState(false)
    // 等待开始计算
    const [waiting, setWaiting] = useState(true)
    const [historyFile, setHistoryFile] = useState({ name: "", filePath: "" });
    const [predictFile, setpredictFile] = useState({ name: "", filePath: "" });
    const [predictResData, setpredictResData] = useState({});
    const [warningData, setWarningData] = useState({});
    const [extraData, setExtraData] = useState({});


    const handleSubmit = async (e) => {
        try {
            if (e) {
                setLoading(true)
                setWaiting(false)
                e.file_path = historyFile.filePath
                let response = await post("/risk/warning")
                setWarningData(response)
                setExtraData({ MAE: response.MAE, RMSE: response.RMSE, R: response.R })

                response = await post("/risk/predict", e)
                let res = response.data
                // 预测图
                setpredictResData(res)
            } else {

            }

        } catch (error) {
            Message.error("计算内部出现错误，请检查输入参数！")
            console.log(error)
        } finally {
            setWaiting(false)
            setLoading(false)
        }

    }

    return (
        <div className="main-content">
            <Card
                title='参数'
                style={{
                    width: '30%',
                    height: '100%',
                    padding: ""
                }}
                bodyStyle={{
                    height: "100%",
                    flex: 1

                }}
            >
                <Sider
                    handleSubmit={handleSubmit}
                    setHistoryFile={setHistoryFile}
                    extraData={extraData}
                    setpredictFile={setpredictFile}
                />
            </Card>
            <Card
                title="计算结果"
                style={{ flex: '1', marginLeft: '5px' }}
                bodyStyle={{ padding: '10px', height: '100%', flex: 1 }}
            >
                <ResultPage
                    loading={loading}
                    waiting={waiting}
                    warningData={warningData}
                    predictData={predictResData}
                />
            </Card>
        </div>
    )
}