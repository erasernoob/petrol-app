import { Card } from '@arco-design/web-react'
import ReactECharts from 'echarts-for-react'
import { useSelector } from 'react-redux'
import { useMemo } from 'react'

export default function ResultContent() {
  const { hydroData } = useSelector(state => state.data)

  // 数据处理（含性能优化）
  const chartData = useMemo(() => {
    return hydroData
      .map(item => ({
        depth: item["井深 (m)"],
        // TODO: for test 
        drillPressure: item["钻柱压力 (Pgn, MPa)"] < 0 ? 0 : item['钻柱压力 (Pgn, MPa)'],
        annularPressure: item["环空压力 (Phk, MPa)"] < 0 ?  0 : item["环空压力 (Phk, MPa)"],
        ecd: item["ECD (g/cm³)"]
      }))
      // 数据抽样（每5个点取1个）
  }, [hydroData])

  // ECharts 配置
  const option = useMemo(() => ({
    animation: true, // 禁用动画
    large: true,      // 开启大数据模式
    largeThreshold: 500, // 超过500点时启用优化
    dataset: { source: chartData },
    dataZoom: [{
      type: 'inside', // 内置型数据缩放
      start: 0,
      end: 100
    }],
    yAxis: {
      type: 'value',
      name: '井深 (m)',
      inverse: true
    },
    xAxis: [
     {
        name: '压力 (MPa)',
        type: 'value'
      },
      // {
      //   name: 'ECD (g/cm³)',
      //   type: 'value',
      //   offset: 0,
      //   alignTicks: true
      // }
    ],
    series: [
      {
        name: '钻柱压力',
        type: 'line',
        yAxisIndex: 0,
        encode: { x: 'drillPressure', y: 'depth' },
        sampling: 'lttb', // 采用最佳采样算法
        smooth: true,     // 禁用平滑
        lineStyle: { width: 2 },
        showSymbol: false
      },
      {
        name: '环空压力',
        type: 'line',
        yAxisIndex: 0,
        encode: { x: 'annularPressure', y: 'depth' },
        sampling: 'lttb',
        smooth: false,
        lineStyle: { width: 2 },
        showSymbol: false
      },
      // {
      //   name: 'ECD',
      //   type: 'line',
      //   yAxisIndex: 1,
      //   encode: { x: 'depth', y: 'ecd' },
      //   sampling: 'lttb',
      //   smooth: false,
      //   lineStyle: { width: 1 },
      //   showSymbol: false
      // }
    ],
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    }
  }), [chartData])

  return (
    <Card
      title="计算结果"
      style={{ width: '100%', height: '100%' }}
      bodyStyle={{ padding: '10px', height: '95%' }}
    >
      {chartData.length > 0 ? (
        <ReactECharts
          option={option}
          style={{ height: '100%', width: '100%' }}
          opts={{ renderer: 'canvas' }} // 强制使用Canvas
          notMerge={true}
        />
      ) : (
        <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          数据加载中...
        </div>
      )}
    </Card>
  )
}