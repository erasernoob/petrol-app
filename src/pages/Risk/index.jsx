import { Card, Message } from "@arco-design/web-react"
import { useState } from "react"
import { post } from "../../components/axios"
import ResultPage from "./ResultPage"
import Sider from "./Sider"
export default function DrillPage() {
    const [loading, setLoading] = useState(false)
    // 等待开始计算
    const [waiting, setWaiting] = useState(true)
    const [training, setTraning] = useState(false)
    const [historyFile, setHistoryFile] = useState({ name: "", path: "" });
    const [predictFile, setpredictFile] = useState({ name: "", path: "" });
    const [predictResData, setpredictResData] = useState({});
    const [warningData, setWarningData] = useState({});
    const [extraData, setExtraData] = useState({});

    const totalTrainingTime = 10


    const handleSubmit = async (e) => {
        try {
            if (e) {
                setLoading(true)
                setWaiting(false)
                e.file_path = historyFile.path
                let response = await post("/risk/warning")
                setWarningData(response)
                setExtraData({ MAE: response.MAE, RMSE: response.RMSE, R: response.R })

                e.file_path = predictFile.path
                console.log(predictFile)
                response = await post("/risk/predict", e)
                let res = response.data
                // 预测图
                setpredictResData(res)
            } else {
                // 训练
                setLoading(true)
                setWaiting(false)
                setTraning(true)
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
                    training={training}
                    setTraining={setTraning}
                    setWaiting={setWaiting}
                    waiting={waiting}
                    totalTrainingTime={totalTrainingTime}
                    warningData={warningData}
                    predictData={predictResData}
                />
            </Card>
        </div>
    )
}