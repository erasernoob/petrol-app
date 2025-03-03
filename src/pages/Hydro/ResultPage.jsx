import { Radio, Button, Message } from '@arco-design/web-react'
import ReactECharts from 'echarts-for-react'
import { useSelector } from 'react-redux'
import { useEffect, useMemo, useState } from 'react'
import { Tag } from '@arco-design/web-react'
import Option from '../option'
import { Spin } from '@arco-design/web-react'
import { saveData } from '../utils/utils'

const RadioGroup = Radio.Group

export default function ResultPage({ data, loading, waiting}) {
  const { hydroData } = useSelector(state => state.data)
  // 数据处理（含性能优化）
  const chartData = useMemo(() => {
    return hydroData
      .map(item => ({
        depth: item["井深 (m)"],
        // TODO: for test 
        drillPressure: item["钻柱压力 (Pgn, MPa)"] < 0 ? 0 : item['钻柱压力 (Pgn, MPa)'],
        annularPressure: item["环空压力 (Phk, MPa)"] < 0 ? 0 : item["环空压力 (Phk, MPa)"],
        ecd: item["ECD (g/cm³)"]
      }))
    // 数据抽样（每5个点取1个）
  }, [hydroData])
  // 导出数据函数
  const handleExport = async () => {
    const drillData = chartData.map((value) => {
      return value.drillPressure
    })
    const annularData = chartData.map(value => {
      return value.annularPressure
    })
    await saveData(drillData, '钻柱循环压力表.xlsx')
    saveData(annularData, '环空循环压力表.xlsx')
  }
  const exportButton = <Button type='primary' onClick={handleExport} style={{marginLeft: '22px'}}>导出数据</Button>


  const option2 = Option(chartData,
    {
      type: 'value',
      name: '井深 (m)',
      inverse: true
    }, [
    {
      name: 'ECD (g/cm³)',
      type: 'value',
      offset: 0,
      alignTicks: true
    }
  ], [
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
  ],)

  const option1 = Option(
    chartData,
    {
      type: 'value',
      name: '井深 (m)',
      inverse: true
    }, [
    {
      name: '压力 (MPa)',
      type: 'value',
      position: 'top',
      axisLabel: {
        formatter: function(value) {
          return value == 0 ? '' : value
        }
      }
    },
  ], [
    {
      name: '钻柱压力',
      type: 'line',
      yAxisIndex: 0,
      encode: { x: 'drillPressure', y: 'depth' },
      sampling: 'lttb', // 采用最佳采样算法
      smooth: true,     // 禁用平滑
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
  ],
  )

  const [option, setOption] = useState(option1)
  const [curValue, setCurValue] = useState('循环压力')

  useEffect(() => {
    if (curValue === '循环压力') {
      setOption(option1)
    } else {
      setOption(option2)
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