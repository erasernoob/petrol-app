import { Radio, Button, Message } from '@arco-design/web-react'
import ReactECharts from 'echarts-for-react'
import { useSelector } from 'react-redux'
import { useEffect, useMemo, useState } from 'react'
import Option, { getOptionM, getOptionT } from '../option'
import { Tag } from '@arco-design/web-react'
import 'echarts-gl';
import { Spin } from '@arco-design/web-react'
import { saveData } from '../utils/utils'

const RadioGroup = Radio.Group
const chartOptions = ['数据图', '云图']

export default function ResultPage({handleExport, typeOptions=[], chartData=[], heatData={}, extraData={}, loading, waiting}) {

  // const handleExport = async () => {
  //   const drillData = chartData.map((value) => {
  //     return value.drillPressure
  //   })
  //   const annularData = chartData.map(value => {
  //     return value.annularPressure
  //   })
  //   await saveData(drillData, '钻柱循环压力表.xlsx')
  //   saveData(annularData, '环空循环压力表.xlsx')
  // }

  const exportButton = <Button type='primary' onClick={handleExport} style={{marginLeft: '22px'}}>导出数据</Button>

    const optionM  = getOptionM(heatData.map(({E, N, TCS, M}) => ({E, N, TCS: -TCS, M})))
    const optionT  = getOptionT(heatData.map(({E, N, TCS, T}) => ({E, N, TCS: -TCS, T})))
    const option1 = Option(chartData,
        {
            type: 'value',
            name: '井深 (m)',
            axisLine: {
              onZero: false
            },
            position: 'left',
            inverse: true
        }, [
            {
            name: '轴向力 (kN)',
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '轴向力 (kN)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'T', y: 'Sk' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 2 },
            showSymbol: false
        }
    ],)
    const option2 = Option(
        chartData,
        {
            type: 'value',
            position: 'left',
            name: '井深 (m)',
            inverse: true
        }, [
        {
            name: '扭矩 (kN·m） ',
            type: 'value',
            position: 'top',
        },
    ], [
        {
            name: '扭矩 (kN·m）',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'M', y: 'Sk' },
            sampling: 'lttb', // 采用最佳采样算法
            smooth: true,     // 禁用平滑
            lineStyle: { width: 2 },
            showSymbol: false
        },
    ],
    )
  const [option, setOption] = useState(option1)
  const [curType, setCurType] = useState(typeOptions[0])
  const [curChart, setCurChart] = useState(chartOptions[0])
  const [curValue, setCurValue] = useState(typeOptions[0])

  useEffect(() => {
    if (curValue === typeOptions[0]) {
      setOption(option1)
    } else {
      setOption(option2)
    }
    setCurChart(chartOptions[0])
  }, [chartData, heatData, curValue])

  return (
    <>
    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center' , gap: '0px'}}>
      <RadioGroup
        type='button'
        size='large'
        name='chart'
        value={curType}
        onChange={(value) => {
          setCurValue(value)
          setCurChart(chartOptions[0])
          setCurType(value)
          setOption(value === '轴向力' ? option1 : option2)
        }}
        options={typeOptions}
        >
        </RadioGroup>
      {chartData.length != 0 &&  <RadioGroup
          name='chart'
          // direction='vertical'
          value={curChart}
          onChange={(value) => {
            setCurChart(value)
            if (value === chartOptions[0]) {
                setOption(curType === typeOptions[0] ? option1 : option2)
            } else {
                setOption(curType === typeOptions[0] ? optionT : optionM)
            }
          }}
          options={chartOptions}
          >
        </RadioGroup>}
    </div>
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
            {(curChart !== chartOptions[1] && exportButton)}
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