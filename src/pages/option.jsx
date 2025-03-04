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

const getOptionT = (dataSet) => {
    const minValue = 4;
    const maxValue = 14;
    console.log(dataSet)

    return {
        title: { text: '轴向力分布云图' },
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
        xAxis3D: { name: '东/西 位置 (m)' },
        yAxis3D: { name: '南/北 位置 (m)' },
        zAxis3D: { name: '垂深 (m)', inverse: false },
        dataset: {
            dimensions: ['E', 'N', 'TCS', 'T'],
            source: dataSet
        },
        series: [
            {
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
    console.log(dataSet)

    return {
        title: { text: '扭矩分布云图' },
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
        xAxis3D: { name: '东/西 位置 (m)' },
        yAxis3D: { name: '南/北 位置 (m)' },
        zAxis3D: { name: '垂深 (m)', inverse: false },
        dataset: {
            dimensions: ['E', 'N', 'TCS', 'M'],
            source: dataSet
        },
        series: [
            {
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




// // 扭矩云图 
// const generateOptionForM = (data) =>  {
//     console.log(data[0])
//     return  {
//     // backgroundColor: '#fff',
//     tooltip: {},
//     visualMap: {
//         show: true,
//         dimension: 3,  // 颜色映射到 M 值 [E, N, Tcs, M]
//         min: 0,
//         max: 15,  // 需要调整 max 以适应你的数据
//         inRange: {
//             color: ['blue', 'green', 'yellow', 'red']
//         }
//     },
//     grid3D: {
//         boxWidth: 100,  // 调整 3D 画布大小
//         boxDepth: 100,
//         viewControl: { alpha: 45, beta: 30 }
//     },
//     xAxis3D: { name: 'E (m)' },
//     yAxis3D: { name: 'N (m)' },
//     zAxis3D: { name: '-Depth (m)' },
//     series: [
//         {
//             name: '扭矩分布',
//             type: 'scatter3D',
//             symbolSize: 8,  // 点的大小
//             data: data
//         },
//         {
//             name: '轨迹线',
//             type: 'line3D',
//             lineStyle: { width: 3, color: 'black' },
//             // data: [
//             //     [10, 20, -50],  // [E, N, -Tcs]
//             //     [15, 25, -55],
//             //     [20, 30, -60],
//             //     // ... (这里填充你的轨迹数据)
//             // ]
//             data: data.map((item) => ({
//                 E: item['E'],
//                 N: item['N'],
//                 TCS: item['TCS'],
//             }))
//         }
//     ]
// };
// }

export { getOptionM }


