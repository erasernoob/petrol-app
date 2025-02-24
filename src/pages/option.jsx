import { useMemo } from "react"

/**
 * 
 * @param {*} chartData   数据源
 * @param {*} yAxis      y轴数据 {type: '', name: '', inverse ''}
 * @param {*} xAxis      x轴数据 {type: '', name: '', inverse '', offset: 0, alignTicks: true}
 * @param {*} series     
 */

export default function Option(chartData, yAxis, xAxis, series)  {
    return useMemo(() => ({
    animation: true, // 禁用动画
    large: true,      // 开启大数据模式
    largeThreshold: 500, // 超过500点时启用优化
    dataset: { source: chartData },
    dataZoom: [{
      type: 'inside', // 内置型数据缩放
      start: 0,
      end: 100
    }],
    yAxis: yAxis,
    xAxis: xAxis,
    series: series,
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    }
  }), [chartData])
}
