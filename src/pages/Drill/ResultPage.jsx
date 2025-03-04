import { Radio, Button, Message } from '@arco-design/web-react'
import ReactECharts from 'echarts-for-react'
import { useSelector } from 'react-redux'
import { useEffect, useMemo, useState } from 'react'
import { Tag } from '@arco-design/web-react'
import 'echarts-gl';
import { Spin } from '@arco-design/web-react'
import Option from '../option'
import { saveData } from '../utils/utils'

const RadioGroup = Radio.Group

export default function ResultPage({ handleExport, typeOptions = [], chartOptions = [], chartData = [], extraData = {}, loading, waiting }) {

    // 导出数据函数
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
    const exportButton = <Button type='primary' onClick={handleExport} style={{ marginLeft: '22px' }}>导出数据</Button>
    const option1 = Option(chartData,
        {
            type: 'value',
            name: '角位移 (rad)',
            axisLine: {
              onZero: false
            },
            position: 'left',
            inverse: true
        }, [
            {
            name: '时间 (s)',
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '角位移',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'time', y: 'angle_x' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: false
        }
    ],)
    const option3 = Option(chartData,
        {
            type: 'value',
            name: '角加速度 (rad/s^2)',
            axisLine: {
              onZero: false
            },
            position: 'left',
            inverse: true
        }, [
            {
            name: '时间 (s)',
            type: 'value',
            axisLine: {
              onZero: false
            },
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '角加速度 (rad/s^2)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'time', y: 'angle_a' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: false
        }
    ],)
    const option4 = Option(chartData,
        {
            type: 'value',
            name: '钻头扭矩 (kN·m)',
            axisLine: {
              onZero: false
            },
            position: 'left',
            inverse: true
        }, [
            {
            name: '时间 (s)',
            axisLine: {
              onZero: false
            },
            type: 'value',
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '钻头扭矩 (kN·m)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'time', y: 'drill_m' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: false
        }
    ],)
    const option2 = Option(chartData,
        {
            type: 'value',
            name: '角速度 (rad/s)',
            axisLine: {
              onZero: false
            },
            position: 'left',
            inverse: true
        }, [
            {
            name: '时间 (s)',
            type: 'value',
            axisLine: {
              onZero: false
            },
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '角速度 (rad/s)',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'time', y: 'angle_v' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: false
        }
    ],)
    const option5 = Option(chartData,
        {
            type: 'value',
            name: '相对角速度 (rad/s)',
            axisLine: {
              onZero: false
            },
            position: 'left',
        }, [
            {
            name: '相对角位移（rad）',
            type: 'value',
            axisLine: {
              onZero: false
            },
            offset: 0,
            alignTicks: true,
            position: 'top',
        }
    ], [
        {
            name: '粘滑振动相轨迹',
            type: 'line',
            yAxisIndex: 0,
            encode: { x: 'relativex', y: 'relativey' },
            sampling: 'lttb',
            smooth: false,
            lineStyle: { width: 1.5 },
            showSymbol: false
        }
    ],)



    const [option, setOption] = useState(option1)
    const [curType, setCurType] = useState(typeOptions[0])

    useEffect(() => {
        const index = typeOptions.findIndex((item) => curType === item)
        if (index === 0) {
        setOption(option1);
        } else if (index === 1) {
        setOption(option2);
        } else if (index === 2) {
        setOption(option3);
        } else if (index === 3) {
        setOption(option4);
        } else if (index === 4) {
        setOption(option5);
        } else {
        console.error("当前类型没有对应的 option");
        }
    }, [chartData, curType])
    const tagList = (Object.entries({}).map(([key, value]) => {
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
        value={curType}
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
        <div style={{ height: '70%', display: 'flex', alignItems:'center' ,justifyContent: 'center' }}>
          {waiting == true ? '输入参数开始计算' :  <Spin size="30" tip='正在计算中......' /> }
        </div>
      )}
    </>
  )

}