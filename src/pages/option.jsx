import { useMemo } from "react"

/**
 * 
 * @param {*} chartData   数据源
 * @param {*} yAxis      y轴数据 {type: '', name: '', inverse ''}
 * @param {*} xAxis      x轴数据 {type: '', name: '', inverse '', offset: 0, alignTicks: true}
 * @param {*} series     
 */


export default function Option(chartData, yAxis, xAxis, series) {
  return {
    animation: true,
    large: true,
    largeThreshold: 500,
    dataset: { source: chartData },
    dataZoom: [{
      type: 'inside',
      start: 0,
      end: 100
    }],
    yAxis,
    xAxis,
    series,
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      show: true,
      orient: 'vertical',
      left: 'left',
      top: 'bottom',
      textStyle: {
        fontSize: 12,
        color: '#333'
      }
    }
  };
}



export const getOptionT = (dataSet) => {
    const minValue = -50;
    const maxValue = 150;

    return {
        title: { text: '轴向力分布云图' },
        animation: true,
        // 自定义 tooltip
        tooltip: {
        },
        visualMap: {
            show: true,
            dimension: 3, // 第四个维度 (M) 决定颜色
            min: minValue,
            max: maxValue,
            inRange: {
                color: ['blue', 'cyan', 'yellow', 'red']
            }
        },
        grid3D: {
            // 如需调整 3D 画布大小，可增加 boxWidth、boxDepth 等配置
                boxWidth: 200,   // x 轴可视长度
                boxHeight: 80,   // y 轴可视长度 (数值跨度大，就让它小一点)
                boxDepth: 50,   //  轴可视长度，可根据垂深范围自行调整
                viewControl: { alpha: 10, beta: 10 }
        },
        xAxis3D: { name: '东/西  (m)' },
        yAxis3D: { name: '南/北  (m)' },
        zAxis3D: { name: '垂深 (m)', inverse: false },
        dataset: {
            dimensions: ['E', 'N', 'TCS', 'T'],
            source: dataSet
        },
        series: [
            {
                name: '轴向力分布',
                type: 'scatter3D',
                symbolSize: 6,
                encode: {
                    x: 'E',
                    y: 'N',
                    z: 'TCS',
                    tooltip: 'T'  // 显示 M 值用于 tooltip 和 visualMap
                }
            }
        ]
        }
    };



const getOptionM = (dataSet) => {
    // 设置 visualMap 的 M 值范围（这里使用硬编码的 0 到 14）
    const minValue = 4;
    const maxValue = 14;
    return {
        title: { text: '扭矩分布云图' },
        animation: true,
        // 自定义 tooltip
        tooltip: {

        },
        visualMap: {
            show: true,
            dimension: 3, // 第四个维度 (M) 决定颜色
            min: minValue,
            max: maxValue,
            inRange: {
                color: ['blue', 'cyan', 'yellow', 'red']
            }
        },
        grid3D: {
            // 如需调整 3D 画布大小，可增加 boxWidth、boxDepth 等配置
                boxWidth: 200,   // x 轴可视长度
                boxHeight: 80,   // y 轴可视长度 (数值跨度大，就让它小一点)
                boxDepth: 50,   //  轴可视长度，可根据垂深范围自行调整
                viewControl: { alpha: 10, beta: 10 }
        },
        xAxis3D: { name: '东/西 (m)' },
        yAxis3D: { name: '南/北 (m)' },
        zAxis3D: { name: '垂深 (m)', inverse: false },
        dataset: {
            dimensions: ['E', 'N', 'TCS', 'M'],
            source: dataSet
        },
        series: [
            {
                name: '扭矩分布',
                type: 'scatter3D',
                symbolSize: 6,
                encode: {
                    x: 'E',
                    y: 'N',
                    z: 'TCS',
                    tooltip: 'M'  // 显示 M 值用于 tooltip 和 visualMap
                }
            }
        ]
        }
    };


export { getOptionM }


