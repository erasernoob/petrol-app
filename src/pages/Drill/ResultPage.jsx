import { Radio, Button, Message } from '@arco-design/web-react'
import { Empty } from '@arco-design/web-react'
import ReactECharts from 'echarts-for-react'
import { useSelector } from 'react-redux'
import { useEffect, useMemo, useState } from 'react'
import { Tag } from '@arco-design/web-react'
import { saveAtFrontend } from '../utils/utils'
import 'echarts-gl';
import { Spin } from '@arco-design/web-react'
import Option from '../option'
import { save2Data, saveData } from '../utils/utils'

const RadioGroup = Radio.Group

export default function ResultPage({typeOptions = [], chartOptions = [], chartData = [], extraData = {}, loading, waiting }) {

        const option1 = Option(chartData,
        {
            type: 'value',
            name: '角位移 (rad)',
            nameLocation:"start",
            axisLine: {
              onZero: false
            },
            position: 'left',
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
            nameLocation:"start",
            axisLine: {
              onZero: false
            },
            position: 'left',
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
            nameLocation:"start",
            position: 'left',
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
            nameLocation:"start",
            position: 'left',
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
            nameLocation:"start",
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
            name: '相轨迹',
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
    const [SSI, setSSI] = useState(0)
    const [riskLevel, setRiskLevel] = useState({level: '', color: ''})

    const handleExport = async () => {
      const index = typeOptions.findIndex((item) => curType === item)
      switch (index) {
        case 0:
          await saveAtFrontend(chartData.map(value => value.angle_a), `角加速度`)
          break;
        case 1:
          await saveAtFrontend(chartData.map(value => value.angle_v), `角速度`)
          break;
        case 2:
          await saveAtFrontend(chartData.map(value => value.angel_v), `角位移`)
          break;
        case 3:
          await saveAtFrontend(chartData.map(value => value.drill_m), `钻头扭矩`)
          break;
        case 4:
          await saveAtFrontend(chartData.map(value => value.relativex), `钻头粘滑振动相轨迹`, chartData.map(value => value.relativey))
          break;
        default:
          break;
      }
  }
    const exportButton = <Button type='primary' onClick={handleExport} style={{ marginLeft: '22px' }}>导出数据</Button>




    const handleRiskLevel = () => {
      let res = {level: '', color: ''}
      switch (true) {
        case SSI < 0.5:
          res = {level: '安全', color: 'green'}
          break;
        case SSI < 1.0:
          res = {level: '低风险', color: 'yellow'}
          break;
        case SSI < 1.5:
          res = {level: '中风险', color: 'orange'}
          break;
        case SSI >= 1.5:
          res = {level: '高风险', color: 'red'}
          break;
        default:
          res = {level: '', color: ''}
          break;
      }
      console.log(res)
      setRiskLevel(res)
    }
    useEffect(() => {
      handleRiskLevel()
    }, [SSI]) 
    
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
        if (chartData.length !== 0 && chartData[0].SSI) {
          setSSI((chartData[0].SSI).toFixed(3))
        }
    }, [chartData, curType])

    const tagList = (
      <>
       <span style={{marginLeft: '100px'}}>粘滑振动等级（SSI）</span>
         <Tag size='large'>{SSI}</Tag>
       <span style={{marginLeft: '100px', marginRight: '20px'}}>风险等级</span>
         <Tag size='large' style={{color: riskLevel.color }}>{riskLevel.level}</Tag>
       </>
    )

  return (
    <>
      <div style={{display: 'flex', justifyContent: '', alignItems: 'center' , gap: '0px'}}>
      </div>

      {chartData.length > 0 && loading === false && waiting === false ? (
        <>
      <RadioGroup
        type='button'
        style={{
          marginLeft: '20px'
        }}
        size='large'
        name='chart'
        value={curType}
        onChange={(value) => {
          setCurType(value)
        }}
        options={typeOptions}
        >
      </RadioGroup>
      { chartData.length > 0 && loading === false && waiting === false &&  tagList}
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
            {exportButton}
          </div>
        </>
      ) : (
        <div style={{ height: '70%', display: 'flex', alignItems:'center' ,justifyContent: 'center' }}>
          {waiting == true ? <Empty description="输入参数开始计算"></Empty> :  <Spin size="30" tip='正在计算中......' /> }
        </div>
      )}
    </>
  )

}