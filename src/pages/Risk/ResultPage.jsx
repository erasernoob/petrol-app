import { Button, Grid, Radio, Spin } from '@arco-design/web-react';
import ReactECharts from 'echarts-for-react';
import { useEffect, useState } from 'react';

const RadioGroup = Radio.Group
const { Row, Col } = Grid;

export default function ResultPage({ chartData = [], data = {}, loading = false, waiting = true, warningData = {}, predictData = {} }) {

  const [curValue, setCurValue] = useState('泥浆池体积预测')


  const getOption1 = () => {
    if (Object.keys(predictData).length == 0) {
      return {}
    }
    const { x, tva_data, peaks, valleys, danger_zones } = predictData;

    // Create mark points for peaks and valleys
    const markPoints = [];
    peaks.forEach(idx => {
      markPoints.push({
        coord: [x[idx], tva_data[idx]],
        symbol: "triangle",
        symbolSize: 14,
        itemStyle: { color: "red" },
        label: { show: true, formatter: `阈值: ${tva_data[idx].toFixed(2)}`, position: "top" }
      });
    });

    valleys.forEach(idx => {
      markPoints.push({
        coord: [x[idx], tva_data[idx]],
        symbol: "triangle",
        symbolRotate: 180,
        symbolSize: 14,
        itemStyle: { color: "green" },
        label: { show: false }
      });
    });

    // Create separate series for each danger zone to get proper legend items
    const dangerSeries = [];
    const dangerLegendName = []
    const dangerLegendItems = new Set(); // To track unique legend items

    danger_zones.forEach(zone => {
      const legendName = `危险等级 ${zone.level}`;
      if (!dangerLegendName.includes(legendName)) {
        dangerLegendName.push(legendName)
      }
      dangerLegendItems.add(legendName);

      // Create a separate series for each danger zone
      dangerSeries.push({
        name: legendName,
        type: 'line',
        data: Array.from({ length: zone.end - zone.start + 1 }, (_, i) => {
          const idx = zone.start + i;
          return [x[idx], tva_data[idx]];
        }),
        symbol: 'none',
        lineStyle: { opacity: 0 },
        areaStyle: {
          color: zone.color,
          opacity: 0.3
        },
        stack: 'danger'
      });

      // Add annotation for threshold
      const midPoint = Math.floor((zone.start + zone.end) / 2);
      const maxValue = Math.max(...tva_data.slice(zone.start, zone.end + 1));
      markPoints.push({
        coord: [x[midPoint], maxValue + 5],
        symbol: 'pin',
        symbolSize: 0,
        label: {
          show: true,
          formatter: `阈值: ${zone.threshold.toFixed(2)}`,
          backgroundColor: '#fff',
          padding: 5,
          borderRadius: 3,
          position: 'top'
        }
      });
    });

    // Ensure fixed legend items for both danger levels
    const legendData = ["TVA值", ...dangerLegendName, "波峰", "波谷"];

    return {
      title: { text: "TVA 趋势分析图", left: "center" },
      tooltip: { trigger: "axis" },
      legend: {
        data: legendData,
        top: 25,
        itemGap: 10,
        textStyle: { fontSize: 12 }
      },
      grid: {
        left: '5%',
        right: '5%',
        bottom: '10%',
        top: '15%',
        containLabel: true
      },
      xAxis: {
        type: "category",
        data: x,
        name: "时间(s)",
        nameLocation: "middle",
        nameGap: 30,
        splitLine: { show: true, lineStyle: { type: 'dashed', opacity: 0.5 } }
      },
      yAxis: {
        type: "value",
        name: "TVA (m³)",
        nameLocation: "middle",
        nameGap: 50,
        splitLine: { show: true, lineStyle: { type: 'dashed', opacity: 0.5 } }
      },
      dataZoom: [{ type: "slider", start: 0, end: 100 }],
      series: [
        {
          name: "TVA值",
          type: "line",
          data: tva_data,
          smooth: true,
          symbol: 'none',
          lineStyle: { color: 'blue', width: 2 },
          markPoint: {
            symbolSize: 0,
            data: markPoints,
            label: {
              position: 'top'
            }
          }
        },
        ...dangerSeries,
        {
          name: "波峰",
          type: "scatter",
          data: peaks.map(idx => [x[idx], tva_data[idx]]),
          symbol: 'triangle',
          symbolSize: 14,
          itemStyle: { color: 'red' }
        },
        {
          name: "波谷",
          type: "scatter",
          data: valleys.map(idx => [x[idx], tva_data[idx]]),
          symbol: 'triangle',
          symbolRotate: 180,
          symbolSize: 14,
          itemStyle: { color: 'green' }
        }
      ]
    };

  }

  const getOption2 = () => {
    // 检查 warningData 是否存在并且包含所需字段
    console.log(warningData)
    if (Object.keys(warningData).length === 0) {
      return {
        title: {
          text: "TVA预测值 (无数据)",
          left: "center"
        },
        xAxis: { type: "category", data: [] },
        yAxis: { type: "value" },
        series: [{ type: "line", data: [] }]
      };
    }

    const { x, TVA } = warningData;

    // 确保数据格式正确
    const safeX = Array.isArray(x) ? x : [];
    const safeTVA = Array.isArray(TVA) ? TVA : [];

    return {
      title: {
        text: "TVA预测值",
        left: "center"
      },
      tooltip: {
        trigger: "axis",
        formatter: function (params) {
          if (params[0] && params[0].value !== undefined) {
            const value = typeof params[0].value === 'number'
              ? params[0].value.toFixed(2)
              : Array.isArray(params[0].value) && params[0].value[1] !== undefined
                ? params[0].value[1].toFixed(2)
                : '未知';
            return `时间: ${params[0].dataIndex}<br/>TVA: ${value} m³`;
          }
          return '';
        }
      },
      grid: {
        left: '5%',
        right: '5%',
        bottom: '10%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: "category",
        data: safeX,
        name: "时间(s)",
        nameLocation: "middle",
        nameGap: 30,
        splitLine: { show: true, lineStyle: { type: 'dashed', opacity: 0.5 } }
      },
      yAxis: {
        type: "value",
        name: "TVA (m³)",
        nameLocation: "middle",
        nameGap: 50,
        splitLine: { show: true, lineStyle: { type: 'dashed', opacity: 0.5 } }
      },
      dataZoom: [{ type: "slider", start: 0, end: 100 }],
      series: [
        {
          name: "TVA预测曲线",
          type: "line",
          data: safeTVA,
          smooth: true,
          symbol: 'none',
          lineStyle: { color: 'red', width: 2 },
        }
      ],
      legend: {
        data: ["TVA预测曲线"],
        top: 25,
        textStyle: { fontSize: 12 }
      }
    };
  };

  // Initialize with empty option
  const [option, setOption] = useState({});

  // Initial load and data update handler
  useEffect(() => {
    // Reset to first chart whenever predictData or warningData changes
    setCurValue('泥浆池体积预测');
    const newOption = getOption1();
    setOption(newOption);
  }, [predictData, warningData]);

  // Handle tab switching
  useEffect(() => {
    const newOption = curValue === '泥浆池体积预测' ? getOption1() : getOption2();
    setOption(newOption);
  }, [curValue]);

  const handleExport = async () => {

  }

  const exportButton = <Button type='primary' onClick={handleExport} style={{ marginLeft: '22px' }}>导出数据</Button>


  return (
    <>
      {Object.keys(warningData).length > 0 && loading === false && waiting === false ? (
        <>
          <Row justify="center" align="start" style={{ height: '2vh' }}>
            <Col span={24}>
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
                options={['泥浆池体积预测', '井漏风险预警结果']}
              >
              </RadioGroup>
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