import { Radio, Button, Message } from '@arco-design/web-react'
import ReactECharts from 'echarts-for-react'
import { useSelector } from 'react-redux'
import { useEffect, useMemo, useState } from 'react'
import { Tag } from '@arco-design/web-react'
import Option from '../option'
import { Spin } from '@arco-design/web-react'
import { save2Data, saveData } from '../utils/utils'

const RadioGroup = Radio.Group

export default function ResultPage({chartData=[], data, loading, waiting}) {

  const handleExport = save2Data

  const exportButton = <Button type='primary' onClick={handleExport} style={{marginLeft: '22px'}}>导出数据</Button>

    // 使用 useMemo 让 option1 和 option2 在 chartData 变化时重新计算
  const option1 = useMemo(() => Option(
    chartData,
    { type: 'value', name: '井深 (m)', inverse: true, 
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
        name: '钻柱压力',
        type: 'line',
        yAxisIndex: 0,
        encode: { x: 'drillPressure', y: 'depth' },
        sampling: 'lttb',
        smooth: true,
        lineStyle: { width: 2 },
        showSymbol: false
      },
      {
        name: '环空压力',
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
          formatter: (value) => value.toFixed(1), // 保留一位小数
        },
        min: 'dataMin',
        offset: 0,
        alignTicks: true,
        position: 'top'
      }
    ],
    [
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
    ]
  ), [chartData]); // 依赖于 chartData
  console.log(chartData)



  const [option, setOption] = useState({})
  const [curValue, setCurValue] = useState('循环压力')

  useEffect(() => {
  const newOption = curValue === '循环压力' ? option1 : option2
  // 只有 option 真正发生变化时才更新
  if (JSON.stringify(option) !== JSON.stringify(newOption)) {
    setOption(newOption)
  }

  }, [chartData, curValue])

  const tagList = (Object.entries(data).map(([key, value]) => {
    return (
      <>
        <span>{key}</span>
        <Tag size='large'>{value.toFixed(3)}</Tag>
      </>
    )
  }))

  return (
    <>
      <RadioGroup
        type='button'
        size='large'
        name='chart'
        defaultValue={curValue}
        onChange={(value) => {
          setCurValue(value)
        }}
        options={['循环压力', 'ECD']}
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
        <div style={{ height: '70%', display: 'flex', alignItems:'center' ,justifyContent: 'center' }}>
          {waiting == true ? '输入参数开始计算' :  <Spin size="30" tip='正在计算中......' /> }
        </div>
      )}

    </>
  )
}