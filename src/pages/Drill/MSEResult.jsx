import { Button, Grid, Radio, Spin, Tag } from '@arco-design/web-react'
import ReactECharts from 'echarts-for-react'
import 'echarts-gl'
import Option from '../option'
import { saveAtFrontend } from '../utils/utils'

const RadioGroup = Radio.Group
const { Row, Col } = Grid
export default function MSEResult({ chartOptions = [], options = [], chartData = [], extraData = {}, loading, waiting }) {

    const handleExport = async () => {
        await saveAtFrontend(chartData.map(value => value.MSE), `MSE`)
    }

    const exportButton = <Button type='primary' onClick={handleExport} style={{ marginLeft: '22px' }}>导出MSE数据</Button>

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
            axisLabel: {
                formatter: (value) => value.toFixed(0), // 保留一位小数
            },
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: 'MSE (MPa)',
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
            name: '机械钻速 (m/h)',
            nameLocation: 'center',
            nameGap: 25, // 轴名称与坐标轴的距离
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '机械钻速 (m/h)',
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
    const option5 = Option(chartData,
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
            name: '岩石抗压强度(MPa)',
            nameLocation: 'center',
            nameGap: 25, // 轴名称与坐标轴的距离
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '岩石抗压强度(MPa)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'UCS', y: 'Sk' },
            sampling: 'none',
            smooth: false,
            lineStyle: { width: 1, color: 'rgb(127, 162, 50)' },
            showSymbol: false
        }
    ],
        {
            show: false,
        })

    chartOptions = [option1, option2, option3, option4]
    if (Object.keys(extraData).length != 0) {
        chartOptions = [option5, option1, option2, option3, option4]
    }

    return (
        <>

            {chartData.length > 0 && loading === false && waiting === false ? (
                <>
                    <div style={{ height: '71vh', width: '100%', display: 'flex', alignItems: 'center', gap: "0px", justifyContent: 'space-between' }}>
                        {
                            chartOptions.map((option, index) => {
                                return (
                                    <>
                                        <ReactECharts
                                            key={index}
                                            option={option}
                                            style={{ height: '100%', width: '220%' }}
                                            opts={{ renderer: 'svg' }} // 强制使用Canvas
                                        />
                                    </>)
                            })
                        }
                    </div>
                    <div style={{
                        marginBottom: "10px",
                        width: '100%'
                    }}>
                        {Object.keys(extraData).length === 0 ? exportButton : (
                            <Row gutter={16} style={{ width: '100%' }}>
                                <Col span={5}>
                                    {/* 空列，用于左侧占位 */}
                                </Col>
                                <Col span={4} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                                    {exportButton}
                                </Col>


                                <Col span={5} style={{ display: 'flex', justifyContent: 'center' }}>
                                    <div style={{ display: 'flex', alignItems: 'center' }}>
                                        <span style={{ marginRight: "10px" }}>钻压推荐值：</span>
                                        <Tag size="large" style={{ minWidth: '60px', textAlign: 'center' }}>
                                            {extraData.wob_res}
                                        </Tag>
                                    </div>
                                </Col>

                                <Col span={5} style={{ display: 'flex', justifyContent: 'center' }}>
                                    <div style={{ display: 'flex', alignItems: 'center' }}>
                                        <span style={{ marginRight: "10px" }}>转速推荐值：</span>
                                        <Tag size="large" style={{ minWidth: '60px', textAlign: 'center' }}>
                                            {extraData.rpm_res}
                                        </Tag>
                                    </div>
                                </Col>

                                <Col span={5} style={{ display: 'flex', justifyContent: 'center' }}>
                                    <div style={{ display: 'flex', alignItems: 'center' }}>
                                        <span style={{ marginRight: "10px" }}>机械钻速推荐值：</span>
                                        <Tag size="large" style={{ minWidth: '60px', textAlign: 'center' }}>
                                            {extraData.rop_res}
                                        </Tag>
                                    </div>
                                </Col>

                            </Row>
                        )}
                    </div>
                </>
            )
                :
                <div className="mse-waiting-page" style={{ height: '83vh', display: 'flex', alignItems: 'center', margin: '0px 0px', justifyContent: 'center' }}>

                    {waiting == true ?
                        // <Empty description="输入参数开始计算"></Empty> 
                        "输入参数开始计算"
                        :
                        <Spin size="30" tip='正在计算中......' />
                    }
                </div>
            }

        </>
    )
}