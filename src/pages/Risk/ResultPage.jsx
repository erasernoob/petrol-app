import { Button, Grid, Radio, Spin, Tag } from '@arco-design/web-react';
import ReactECharts from 'echarts-for-react';
import { useEffect, useMemo, useState } from 'react';
import Option from '../option';
import { saveAtFrontend } from '../utils/utils';

const RadioGroup = Radio.Group
const { Row, Col } = Grid;

export default function ResultPage({ chartData = [], data = {}, loading = false, waiting = true }) {


  const ecd = chartData.map((item) => item.ecd ? item.ecd : 10000)
  const ecdMinVal = (Math.min(...ecd) * 0.99).toFixed(2)

  // 使用 useMemo 让 option1 和 option2 在 chartData 变化时重新计算
  const option1 = useMemo(() => Option(
    chartData,
    {
      type: 'value', name: '井深 (m)', inverse: true,
      axisLine: { onZero: false },
      position: 'left',
    },
    [
      {
        name: '压力 (MPa)',
        type: 'value',
        position: 'top',
        axisLabel: {
          formatter: (value) => (value === 0 ? '' : value)
        }
      },
    ],
    [
      {
        name: '钻柱压力(MPa)',
        type: 'line',
        yAxisIndex: 0,
        encode: { x: 'drillPressure', y: 'depth' },
        sampling: 'lttb',
        smooth: true,
        lineStyle: { width: 2 },
        showSymbol: false
      },
      {
        name: '环空压力(MPa)',
        type: 'line',
        yAxisIndex: 0,
        encode: { x: 'annularPressure', y: 'depth' },
        sampling: 'lttb',
        smooth: false,
        lineStyle: { width: 2 },
        showSymbol: false
      },
    ]
  ), [chartData]); // 依赖于 chartData

  const option2 = useMemo(() => Option(
    chartData,
    {
      type: 'value',
      name: '井深 (m)',
      axisLine: { onZero: false },
      position: 'left',
      inverse: true
    },
    [
      {
        name: 'ECD (g/cm³)',
        type: 'value',
        axisLine: {
          onZero: false
        },
        axisLabel: {
          formatter: (value) => value.toFixed(2), // 保留一位小数
        },
        min: ecdMinVal,
        offset: 0,
        alignTicks: true,
        position: 'top'
      }
    ],
    [
      {
        name: 'ECD (g/cm³)',
        type: 'line',
        yAxisIndex: 0,
        encode: { x: 'ecd', y: 'depth' },
        sampling: 'lttb',
        smooth: false,
        lineStyle: { width: 1 },
        showSymbol: false
      }
    ]
  ), [chartData]); // 依赖于 chartData

  const [option, setOption] = useState({})
  const [curValue, setCurValue] = useState('循环压力')

  const handleExport = async () => {
    const drillData = chartData.map((value) => {
      return value.drillPressure
    })
    const annularData = chartData.map(value => {
      return value.annularPressure
    })
    if (option === option1) {
      await saveAtFrontend(drillData, '钻柱循环压力表')
      await saveAtFrontend(annularData, '环空循环压力表')
    } else {
      await saveAtFrontend(chartData.map((value) => value.ecd), "ECD")
    }
  }

  const exportButton = <Button type='primary' onClick={handleExport} style={{ marginLeft: '22px' }}>导出数据</Button>


  useEffect(() => {
    const newOption = curValue === '循环压力' ? option1 : option2
    // 只有 option 真正发生变化时才更新
    if (JSON.stringify(option) !== JSON.stringify(newOption)) {
      setOption(newOption)
    }

  }, [chartData, curValue])

  const tagList = (Object.entries(data).map(([key, value]) => {
    return (
      <span>
        <span>{key}</span>
        <Tag size='large'>{value.toFixed(3)}</Tag>
      </span>
    )
  }))

  return (
    <>
      {chartData.length > 0 && loading === false && waiting === false ? (
        <>
          <Row justify="center" align="start" style={{ height: '2vh' }}>
            <Col span={4}>
              <RadioGroup
                type='button'
                size='large'
                name='chart'
                defaultValue={curValue}
                onChange={(value) => {
                  setCurValue(value)
                }}
                style={{
                  marginLeft: '20px'
                }}
                options={['循环压力', 'ECD']}
              >
              </RadioGroup>
            </Col>
            {/* <Col span={6} style={{ height: 48, lineHeight: '48px' }}> */}
            <Col span={20}>
              <div style={{
                display: 'flex',
                marginLeft: "30px",
                justifyContent: 'center',
                alignItems: 'center',
                gap: "20px",
              }}>
                {tagList}
              </div>
            </Col>
          </Row>
          <ReactECharts
            option={option}
            style={{ height: '81%', width: '100%' }}
            opts={{ renderer: 'canvas' }} // 强制使用Canvas
            notMerge={true}
          />
          <div className="extra-value" style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            // marginTop: '7px',
            marginLeft: '0px'
          }}>
            {exportButton}
          </div>
        </>
      ) : (
        <div style={{ height: '80%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {waiting == true ?
            // <Empty description="输入参数开始计算"></Empty> 
            "输入参数开始计算"
            : <Spin size="30" tip='正在计算中......' />}
        </div>
      )}

    </>
  )
}