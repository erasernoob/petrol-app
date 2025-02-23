import { Card } from '@arco-design/web-react'
import { LineChart, Line, XAxis, YAxis } from 'recharts'
import { useSelector } from 'react-redux'
import { hydro } from '../../../data/Params';

export default function ResultContent() {
  const { hydroData } = useSelector(state => state.data)
  const chartData = hydroData.map(item => ({
    depth: item["井深 (m)"],
    drillPressure: item["钻柱压力 (Pgn, MPa)"],
    annularPressure: item["环空压力 (Phk, MPa)"],
    ecd: item["ECD (g/cm³)"]
  }));
  console.log(chartData)

  return (
    <Card
      title='计算结果'
      style={{
        width: '100%',
        height: '100%',
        overflow: "hidden",
        maxHeight: 'calc(100% - 1px)',
        borderTop: '0px'
      }}
    >

    {
      hydroData.length > 0 ? (
        <LineChart data={chartData}>
          <XAxis dataKey="depth" />
          <YAxis />
          <Line type="monotone" dataKey="drillPressure" stroke="#8884d8" />
          <Line type="monotone" dataKey="annularPressure" stroke="#82ca9d" />
          <Line type="monotone" dataKey="ecd" stroke="#ff7300" />
        </LineChart>
      ) : (
        <div>数据加载中...</div>
      )
    }

     </Card>

  )

}