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

const Option3D = {
    backgroundColor: '#fff',
    tooltip: {},
    visualMap: {
        show: true,
        dimension: 3,  // 颜色映射到 M 值
        min: 0,
        max: 100,  // 需要调整 max 以适应你的数据
        inRange: {
            color: ['blue', 'green', 'yellow', 'red']
        }
    },
    grid3D: {
        boxWidth: 100,  // 调整 3D 画布大小
        boxDepth: 100,
        viewControl: { alpha: 45, beta: 30 }
    },
    xAxis3D: { name: 'E (m)' },
    yAxis3D: { name: 'N (m)' },
    zAxis3D: { name: '-Depth (m)' },
    series: [
        {
            name: '扭矩分布',
            type: 'scatter3D',
            symbolSize: 8,  // 点的大小
            data: [
                [10, 20, -50, 10],  // [E, N, -Tcs, M]
                [15, 25, -55, 20],
                [20, 30, -60, 30],
                // ... (这里填充你的数据)
            ]
        },
        {
            name: '轨迹线',
            type: 'line3D',
            lineStyle: { width: 3, color: 'black' },
            data: [
                [10, 20, -50],  // [E, N, -Tcs]
                [15, 25, -55],
                [20, 30, -60],
                // ... (这里填充你的轨迹数据)
            ]
        }
    ]
};

