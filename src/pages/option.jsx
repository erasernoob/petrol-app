import { useMemo } from "react"

/**
 * 
 * @param {*} chartData   数据源
 * @param {*} yAxis      y轴数据 {type: '', name: '', inverse ''}
 * @param {*} xAxis      x轴数据 {type: '', name: '', inverse '', offset: 0, alignTicks: true}
 * @param {*} series     
 */

export default function Option(chartData, yAxis, xAxis, series )  {
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
    yAxis: [
    {
      type: 'value',
      name: '井深 (m)',
      inverse: true
    },],
    xAxis: [
      {
        name: 'ECD (g/cm³)',
        type: 'value',
        offset: 0,
        alignTicks: true
      }
    ],
    series: [
      {
        name: 'ECD',
        type: 'line',
        yAxisIndex: 0,
        encode: { x: 'ecd', y: 'depth' },
        sampling: 'lttb',
        smooth: false,
        lineStyle: { width: 1 },
        showSymbol: false
      }
    ],
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    }
  }), [chartData])
}
