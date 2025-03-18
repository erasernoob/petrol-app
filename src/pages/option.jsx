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
    animationThreshold: 20000, // ✅ 调高动画适用的数据量
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
    // 计算 M 值的范围
    const TValues = dataSet.map(item => item.T || 0);
    const minT = Math.min(...TValues);
    const maxT = Math.max(...TValues);

    // 计算 E、N 和 TCS 的最小值和最大值
    const EValues = dataSet.map(item => item.E ? item.E.toFixed(2) : 0);
    const NValues = dataSet.map(item => item.N ? item.N.toFixed(2) : 0);
    const TCSValues = dataSet.map(item => item.TCS ? item.TCS.toFixed(2) : 0);

    const minE = Math.min(...EValues), maxE = Math.max(...EValues);
    const minN = Math.min(...NValues), maxN = Math.max(...NValues);
    const minTCS = Math.min(...TCSValues), maxTCS = Math.max(...TCSValues);

    // 计算各个维度的范围
    const rangeE = maxE - minE;
    const rangeN = maxN - minN;
    const rangeTCS = maxTCS - minTCS;

    // 为了模拟 MATLAB 中 axis equal 的效果，
    // 这里将最长边设为常数（例如 200），其他边按比例缩放
    const maxRange = Math.max(rangeE, rangeN, rangeTCS);
    const boxWidth  = (rangeE / maxRange) * 200;
    const boxHeight = (rangeN / maxRange) * 500;
    const boxDepth  = (rangeTCS / maxRange) * 200;

    return {
        title: { text: '轴向力分布云图' },
        animation: true,
        // 自定义 tooltip
        tooltip: {
        },
        visualMap: {
            show: true,
            dimension: 3, // 第四个维度 (M) 决定颜色
            min: minT,
            max: maxT,
            inRange: {
                color: ['blue', 'cyan', 'yellow', 'red']
            },
            type: 'continuous', // 连续映射
            // 显示数值范围
            calculable: true
        },
        grid3D: {
                boxWidth: boxWidth,   // x 轴可视长度
                boxHeight: boxHeight,   // y 轴可视长度 (数值跨度大，就让它小一点)
                boxDepth: boxDepth,   //  轴可视长度，可根据垂深范围自行调整
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
    if (dataSet.length === 0) return {};

    // 计算 M 值的范围
    const MValues = dataSet.map(item => item.M || 0);
    const minM = Math.min(...MValues);
    const maxM = Math.max(...MValues);

    // 计算 E、N 和 TCS 的最小值和最大值
    const EValues = dataSet.map(item => item.E ? item.E.toFixed(2) : 0);
    const NValues = dataSet.map(item => item.N ? item.N.toFixed(2) : 0);
    const TCSValues = dataSet.map(item => item.TCS ? item.TCS.toFixed(2) : 0);

    const minE = Math.min(...EValues), maxE = Math.max(...EValues);
    const minN = Math.min(...NValues), maxN = Math.max(...NValues);
    const minTCS = Math.min(...TCSValues), maxTCS = Math.max(...TCSValues);

    // 计算各个维度的范围
    const rangeE = maxE - minE;
    const rangeN = maxN - minN;
    const rangeTCS = maxTCS - minTCS;

    // 为了模拟 MATLAB 中 axis equal 的效果，
    // 这里将最长边设为常数（例如 200），其他边按比例缩放
    const maxRange = Math.max(rangeE, rangeN, rangeTCS);
    const boxWidth  = (rangeE / maxRange) * 200;
    const boxHeight = (rangeN / maxRange) * 500;
    const boxDepth  = (rangeTCS / maxRange) * 200;

    // 如果 MATLAB 中使用 -TCS 来绘制（z 轴取反），
    // 可通过设置 zAxis3D 的 inverse 或者在数据预处理时取负值
    return {
        title: { text: '扭矩分布云图' },
        animation: true,
        tooltip: {},
        visualMap: {
            show: true,
            dimension: 3,   // 第四个维度 (M) 决定颜色
            min: minM,
            max: maxM,
            inRange: {
                color: ['blue', 'cyan', 'yellow', 'red']
            },
            type: 'continuous',
            calculable: true
        },
        grid3D: {
            boxWidth: boxWidth,   // 根据数据动态计算 x 轴比例
            boxHeight: boxHeight, // 根据数据动态计算 y 轴比例
            boxDepth: boxDepth,   // 根据数据动态计算 z 轴比例
            viewControl: { alpha: 10, beta: 10 }
        },
        xAxis3D: { name: '东/西 (m)'},
        yAxis3D: { name: '南/北 (m)'},
        // 如果数据的 TCS 与 MATLAB 中的 -Tcs 对应，可将 inverse 设置为 true，
        // 或者在数据预处理时取反，这里采用 inverse 的方式
        zAxis3D: { name: '垂深 (m)'},
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
                    tooltip: 'M'
                }
            }
        ]
    };
};



const getOptionm = (dataSet) => {
    // 设置 visualMap 的 M 值范围（这里使用硬编码的 0 到 14）

    const MValue = (
        dataSet.length === 0 ? [0] : 
        (dataSet.map(item => item.M ? item.M : 0))
    )
    const min = Math.min(...MValue)
    const max = Math.max(...MValue)
    return {
        title: { text: '扭矩分布云图' },
        animation: true,
        // 自定义 tooltip
        tooltip: {

        },
        visualMap: {
            show: true,
            dimension: 3, // 第四个维度 (M) 决定颜色
            min: min, // 自动获取数据的最小值
            max: max, // 自动获取数据的最大值
            inRange: {
                color: ['blue', 'cyan', 'yellow', 'red']
            },
            type: 'continuous', // 连续映射
            // 显示数值范围
            calculable: true
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


