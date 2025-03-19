import { Radio, Button, Message } from '@arco-design/web-react'
import ReactECharts from 'echarts-for-react'
import { useSelector } from 'react-redux'
import { useEffect, useMemo, useState } from 'react'
import { Tag } from '@arco-design/web-react'
import 'echarts-gl';
import { Spin } from '@arco-design/web-react'
import { saveData, save2Data } from '../utils/utils'
import Option from '../option'
import { saveAtFrontend } from '../utils/utils'
import { color } from 'echarts'

const RadioGroup = Radio.Group

export default function MSEResult({ chartOptions = [], options = [], chartData = [], extraData = {}, loading, waiting }) {

    const handleExport = async () => {
        await saveAtFrontend(chartData.map(value => value.MSE), `MSE`)
    }
    
    const exportButton = <Button type='primary' onClick={handleExport} style={{ marginLeft: '22px' }}>导出数据</Button>
    
    const option1 = Option(chartData,
        {
            type: 'value',
            min: 'dataMin',
            name: '井深 (m)',
            axisLine: {
              onZero: false
            },
            axisLabel: {
                formatter: (value) => value.toFixed(0), // 保留一位小数
            },
            position: 'left',
            inverse: true
        }, [
            {
            name: 'MSE (MPa)',
            nameLocation: 'center',
            nameGap: 25, // 轴名称与坐标轴的距离
            min: 'dataMin',
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: 'MSE (kN)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'MSE', y: 'Sk' },
            sampling: 'none',
            smooth: false,
            lineStyle: { width: 1 },
            showSymbol: false
        }
    ],
    {
      show: false,
    })
    const option2 = Option(chartData,
        {
            type: 'value',
            name: '井深 (m)',
            min: 'dataMin',
            axisLine: {
              onZero: false
            },
            axisLabel: {
                formatter: (value) => value.toFixed(0), // 保留一位小数
            },
            position: 'left',
            inverse: true
        }, [
            {
            name: '钻压 (kN)',
            nameLocation: 'center',
            nameGap: 25, // 轴名称与坐标轴的距离
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '钻压 (kN)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'wob', y: 'Sk' },
            sampling: 'none',
            smooth: false,
            lineStyle: { width: 1, color: 'rgb(255,0,0)' },
            showSymbol: false
        }
    ],
    {
      show: false,
    })
    const option3 = Option(chartData,
        {
            type: 'value',
            name: '井深 (m)',
            min: 'dataMin',
            axisLine: {
              onZero: false
            },
            axisLabel: {
                formatter: (value) => value.toFixed(0), // 保留一位小数
            },
            position: 'left',
            inverse: true
        }, [
            {
            name: '转速 (RPM)',
            nameLocation: 'center',
            nameGap: 25, // 轴名称与坐标轴的距离
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '转速 (RPM)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'rpm', y: 'Sk' },
            sampling: 'none',
            smooth: false,
            lineStyle: { width: 1, color: 'rgb(255,0,0)' },
            showSymbol: false
        }
    ],
    {
      show: false,
    })
    const option4 = Option(chartData,
        {
            type: 'value',
            name: '井深 (m)',
            min: 'dataMin',
            axisLine: {
              onZero: false
            },
            axisLabel: {
                formatter: (value) => value.toFixed(0), // 保留一位小数
            },
            position: 'left',
            inverse: true
        }, [
            {
            name: '机械转速 (m/h)',
            nameLocation: 'center',
            nameGap: 25, // 轴名称与坐标轴的距离
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '机械转速 (m/h)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'rop', y: 'Sk' },
            sampling: 'none',
            smooth: false,
            lineStyle: { width: 1, color: 'rgb(255,0,0)' },
            showSymbol: false
        }
    ],
    {
      show: false,
    })

   chartOptions = [option1, option2, option3, option4]
    return (
        <>

            {chartData.length > 0 && loading === false && waiting === false ? (
                <>
                <div style={{ height: '80vh', width: '100%', display: 'flex', alignItems: 'center', gap: "5px", justifyContent: 'space-between' }}>
                    {
                        chartOptions.map((option, index) => {
                            return (
                                <>
                                    <ReactECharts
                                        key={index}
                                        option={option}
                                        style={{ height: '100%', width: '40%' }}
                                        opts={{ renderer: 'canvas' }} // 强制使用Canvas
                                    />
                                </>)
                        })
                    }
                </div>
                <div style={{ display: 'flex', marginBottom: '1px' , alignItems: 'center', justifyContent: 'center' }}>
                    {exportButton}
                </div>

                </>
                )
                 :
                <div className="mse-waiting-page" style={{ height: '83vh', display: 'flex', alignItems: 'center', margin: '0px 0px' , justifyContent: 'center' }}>
                    
                    {waiting == true ? '输入参数开始计算' : <Spin size="30" tip='正在计算中......' />}
                </div>
            }

        </>
    )
}