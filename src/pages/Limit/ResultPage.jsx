import { Radio, Button, Message } from '@arco-design/web-react'
import ReactECharts from 'echarts-for-react'
import { useSelector } from 'react-redux'
import { useEffect, useMemo, useState } from 'react'
import { Tag } from '@arco-design/web-react'
import 'echarts-gl';
import { Spin } from '@arco-design/web-react'
import Option from '../option'
import { save2Data, saveData } from '../utils/utils'

const RadioGroup = Radio.Group

export default function ResultPage({ handleExport, activeRoute, typeOptions = [], chartOptions = [], chartData = [], extraData = {}, loading, waiting }) {

    const exportButton = <Button type='primary' onClick={save2Data} style={{ marginLeft: '22px' }}>导出数据</Button>
    console.log(chartData)
    const option1 = Option(chartData,
        {
            type: 'value',
            name: '井深 (m）',
            axisLine: {
                onZero: false
            },
            position: 'left',
            inverse: true
        }, [
        {
            name: 'ECD（g/cm3）',
            type: 'value',
            min: 'dataMin',
            axisLabel: {
                formatter: (value) => value.toFixed(2), // 保留一位小数
            },
            // max: 1.35,
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: 'ECD（g/cm3）',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'ECD', y: 'Sk' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: false
        }
    ],)
    const option4 = Option(chartData,
        {
            type: 'value',
            name: '井口轴向力（kN）',
            axisLine: {
                onZero: false
            },
            axisLabel: {
                formatter: (value) => value.toFixed(1), // 保留一位小数
            },
            min: 'dataMin',
            position: 'left',
            inverse: false
        }, [
        {
            name: '井深（m）',
            type: 'value',
            offset: 0,
            alignTicks: true,
            axisLine: {
                onZero: false
            },
            // position: 'top',
        }
    ], [
        {
            name: '井口轴向力（kN）',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'Sk', y: 'T' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: true
        }
    ],)
    const option5 = Option(chartData,
        {
            type: 'value',
            name: '井口扭矩（kN·m）',
            axisLine: {
                onZero: false
            },
            min: Math.min(...chartData.map(item => item.M ? item.M : 0)) === Math.max(...chartData.map(item => item.M ? item.M : 0)) ? -1 : 'dataMin', // 如果所有数据为 0，最小值设置为 -1
            max: Math.min(...chartData.map(item => item.M ? item.M : 0)) === Math.max(...chartData.map(item => item.M ? item.M : 0)) ? 1 : 'dataMax', // 如果所有数据为 0，最大值设置为 1
            axisLabel: {
                formatter: (value) => value.toFixed(1), // 保留一位小数
            },
            position: 'left',
            inverse: false
        }, [
        {
            name: '井深（m）',
            type: 'value',
            offset: 0,
            axisLine: {
                onZero: false
            },
            alignTicks: true,
            // position: 'top',
        }
    ], [
        {
            name: '立管压力（MPa）',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'Sk', y: 'M' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: true
        }
    ],)
    const option6 = Option(chartData,
        {
            type: 'value',
            name: '安全系数',
            axisLabel: {
                formatter: (value) => value.toFixed(1), // 保留一位小数
            },
            axisLine: {
                onZero: false
            },
            position: 'left',
            inverse: false,
            min: 'dataMin',
            max: 'dataMax',
        }, [
        {
            name: '井深（m）',
            type: 'value',
            axisLine: {
                onZero: false
            },
            offset: 0,
            alignTicks: true,
            // position: 'top',
        }
    ], [
        {
            name: '安全系数',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'Sk', y: 'aq' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: true
        }
    ],)
    const option7 = Option(chartData,
        {
            type: 'value',
            name: '正弦屈曲临界载荷（kN）',
            axisLine: {
                onZero: false
            },
            position: 'left',
            inverse: false
        }, [
        {
            name: '井深（m）',
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '正弦屈曲临界载荷（kN）',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'Sk', y: 'fs' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: false
        }
    ],)
    const option8 = Option(chartData,
        {
            type: 'value',
            name: '螺旋屈曲临界载荷（kN）',
            axisLine: {
                onZero: false
            },
            position: 'left',
            inverse: false
        }, [
        {
            name: '井深（m）',
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '螺旋屈曲临界载荷（kN）',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'Sk', y: 'fh' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: false
        }
    ],)
    const option3 = Option(chartData,
        {
            type: 'value',
            name: '立管压力（MPa）',
            axisLine: {
                onZero: false
            },
            // nameLocation: 'start', // 将轴名称放在轴的下方
            position: 'left',
        }, [
        {
            name: '井深（m）',
            type: 'value',
            offset: 0,
            alignTicks: true,
            axisLine: {
                onZero: false
            },
            // position: 'top',
        }
    ], [
        {
            name: '立管压力（MPa）',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'Sk', y: 'Plg' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: true
        }
    ],)
    const option2 = Option(chartData,
        {
            type: 'value',
            name: '总循环压耗（MPa）',
            axisLine: {
                onZero: false
            },
            // nameLocation: 'start', // 将轴名称放在轴的下方
            position: 'left',
        }, [
        {
            name: '井深（m）',
            type: 'value',
            offset: 0,
            alignTicks: true,
            axisLine: {
                onZero: false
            },
            // position: 'top',
        }
    ], [
        {
            name: '总循环压耗（MPa）',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'Sk', y: 'P' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: true
        }
    ],)

    const [option, setOption] = useState(option1)
    const [curType, setCurType] = useState(typeOptions[0])

    useEffect(() => {
        setCurType(typeOptions[0]) 
    }, [activeRoute])

    useEffect(() => {
        const index = typeOptions.findIndex((item) => curType === item)
        if (activeRoute === 2) {
            if (index === 0) {
                setOption(option2);
            } else if (index === 1) {
                setOption(option3);
            }
        } else if (activeRoute === 3) {
            if (index === 0) {
                setOption(option4);
            } else if (index === 1) {
                setOption(option5);
            } else if (index === 2) {
                setOption(option6);
            }
        } else if (activeRoute === 4) {
            if (index === 0) {
                setOption(option7);
            } else if (index === 1) {
                setOption(option8);
            }
        }
        if (typeOptions.length === 0) setOption(option1)
    }, [chartData, curType, activeRoute])

    const tagList = (Object.entries({}).map(([key, value]) => {
        return (
            <>
                <span>{key}</span>
                <Tag size='large'>{value.toFixed(3)}</Tag>
            </>
        )
    }))
    console.log(curType)
    return (
        <>
            <RadioGroup
                type='button'
                size='large'
                name='chart'
                value={curType}
                defaultValue={curType}
                onChange={(value) => {
                    setCurType(value)
                }}
                options={typeOptions}
            >
            </RadioGroup>
            {chartData.length > 0 && loading === false && waiting === false ? (
                <>
                    <ReactECharts
                        option={option}
                        style={{ height: '78%', width: '100%' }}
                        opts={{ renderer: 'canvas' }} // 强制使用Canvas
                        notMerge={true}
                    />
                    <div className="extra-value" style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '20px',
                        // marginTop: '7px',
                        marginLeft: '0px'
                    }}>
                        {tagList}
                        {exportButton}
                    </div>
                </>
            ) : (
                <div style={{ height: '70%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {waiting == true ? '输入参数开始计算' : <Spin size="30" tip='正在计算中......' />}
                </div>
            )}
        </>
    )

}