const hydro = [
  {
    fundamental: {
      pailiang: { name: "排量 (L/min)", value: 1500 },
      Dw: { name: "井眼直径 (m)", value: 0.2159 },
      Rzz: { name: "钻柱外径 (m)", value: 0.127 },
      rzz: { name: "钻柱内径 (m)", value: 0.1086 },
      Lzz: { name: "钻柱长度 (m)", value: 4190 },
      Rzt: { name: "钻铤外径 (m)", value: 0.15875 },
      rzt: { name: "钻铤内径 (m)", value: 0.07144 },
      Lzt: { name: "钻铤长度 (m)", value: 10 },
    }
  },
  {
    fluid: {
      lbmx: { name: "流变模式 (1=宾汉, 2=幂律, 3=赫巴)", value: 1 },
      fluidden: { name: "钻井液密度 (kg/m³)", value: 1170 },
      n: { name: "流性指数", value: 0.48 },
      K: { name: "稠度系数 (Pa·s^n)", value: 1.09 },
      miu: { name: "塑性粘度 (Pa·s)", value: 0.021 },
      taof: { name: "屈服值 (Pa)", value: 14 },
    }
  },
  {
    drill_pressure: {
      A1: { name: "喷嘴1尺寸 (mm)", value: 16 },
      C1: { name: "喷嘴1个数", value: 7 },
      A2: { name: "喷嘴2尺寸 (mm)", value: 0 },
      C2: { name: "喷嘴2个数", value: 0 },
      A3: { name: "喷嘴3尺寸 (mm)", value: 0 },
      C3: { name: "喷嘴3个数", value: 0 },
    }
  },
  {
    drill_joint: {
      Lp: { name: "单根钻杆长度 (m)", value: 10 },
      Li: { name: "接头长度 (m)", value: 0.3 },
      rzzjt: { name: "接头内径 (m)", value: 0.0953 },
    }
  },
  {
    ground_pipe: {
      L1: { name: "地面高压管线长度 (m)", value: 30 },
      d1: { name: "地面高压管线内径 (m)", value: 0.1086 },
      L2: { name: "立管长度 (m)", value: 30 },
      d2: { name: "立管内径 (m)", value: 0.1086 },
      L3: { name: "水龙带长度 (m)", value: 30 },
      d3: { name: "水龙带内径 (m)", value: 0.1086 },
      L4: { name: "方钻杆长度 (m)", value: 11.4 },
      d4: { name: "方钻杆内径 (m)", value: 0.0826 },
    }
  },
  {
    rock_cuttings: {
      yx: { name: "是否考虑岩屑 (0=不考虑, 1=考虑)", value: 0 },
      yxmd: { name: "岩屑密度 (kg/m³)", value: 2500 },
      H: { name: "岩屑床高度 (%)", value: 10 },
    }
  }
];


export { hydro } 
