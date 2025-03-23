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
    },
  },
  {
    fluid: {
      // (1=宾汉, 2=幂律, 3=赫巴)
      lbmx: {
        name: "流变模式",
        value: 1,
        option: [
          { label: "宾汉流体", value: 1 },
          { label: "幂律流体", value: 2 },
          { label: "赫巴流体", value: 3 },
        ],
      },
      fluidden: { name: "钻井液密度 (kg/m³)", value: 1170 },
      n: { name: "流性指数", value: 0.48 },
      K: { name: "稠度系数 (Pa·s^n)", value: 1.09 },
      miu: { name: "塑性粘度 (Pa·s)", value: 0.021 },
      taof: { name: "屈服值 (Pa)", value: 14 },
    },
  },
  {
    drill_pressure: {
      A1: { name: "喷嘴1尺寸 (mm)", value: 16 },
      C1: { name: "喷嘴1个数", value: 7 },
      A2: { name: "喷嘴2尺寸 (mm)", value: 0 },
      C2: { name: "喷嘴2个数", value: 0 },
      A3: { name: "喷嘴3尺寸 (mm)", value: 0 },
      C3: { name: "喷嘴3个数", value: 0 },
    },
  },
  {
    drill_joint: {
      Lp: { name: "单根钻杆长度 (m)", value: 10 },
      Li: { name: "接头长度 (m)", value: 0.3 },
      rzzjt: { name: "接头内径 (m)", value: 0.0953 },
    },
  },
  {
    ground_pipe: {
      L1: { name: "地面高压管线长度 (m)", value: 30 },
      d1: { name: "地面高压管线内径 (m)", value: 0.1086 },
      L2: { name: "立管长度 (m)", value: 30 },
      d2: { name: "立管内径 (m)", value: 0.1086 },
      L3: { name: "水龙带长度 (m)", value: 30 },
      d3: { name: "水龙带内径 (m)", value: 0.1086 },
      L4: { name: "方钻杆长度 (m)", value: 11.4},
      d4: { name: "方钻杆内径 (m)", value: 0.0826 },
    },
  },
  {
    rock_cuttings: {
      // (0=不考虑, 1=考虑)
      yx: { name: "是否考虑岩屑 ", value: 0 },
      yxmd: { name: "岩屑密度 (kg/m³)", value: 2500 },
      H: { name: "岩屑床高度 (%)", value: 10 },
    },
  },
  // to distinguish the limit and the hyra
  {
    flag: "1"
  }
];

// v=0.00714;               %钻进速度，m/s（仅用于工况1,5：工况5名为上提速度）
// omega=5*pi/3;            %转速，rad/s（仅用于工况1,5）
const torque = {
  work_condition: {
    wc: {
      name: "工况选择",
      value: 1,
      option: [
        { label: "旋转钻进", value: 1 },
        { label: "滑动钻进", value: 2 },
        { label: "起钻", value: 3 },
        { label: "下钻", value: 4 },
        { label: "倒划眼", value: 5 },
      ],
    },
    v: { name: "钻进速度 (m/s)", value: 0.00714 },
    omega: { name: "转速 (rad/s)", value: (5 * Math.PI) / 3 },
    T0: { name: "钻压 (N)", value: 58900 },
    rhoi: { name: "钻井液密度 (kg/m³)", value: 1170 },
    Dw: { name: "井眼直径 (m)", value: 0.2159 },
    tgxs: { name: "套管下深 (m)", value: 3500 },
    miua11: { name: "套管段摩阻系数", value: 0.15 },
    miua22: { name: "裸眼段摩阻系数", value: 0.2 },
    js: { name: "计算井深 (m)", value: 4200 },
  },
};

const limit_eye = [
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
    },
  },
  {
    fluid: {
      // (1=宾汉, 2=幂律, 3=赫巴)
      lbmx: {
        name: "流变模式",
        value: 1,
        option: [
          { label: "宾汉流体", value: 1 },
          { label: "幂律流体", value: 2 },
          { label: "赫巴流体", value: 3 },
        ],
      },
      fluidden: { name: "钻井液密度 (kg/m³)", value: 1170 },
      n: { name: "流性指数", value: 0.48 },
      K: { name: "稠度系数 (Pa·s^n)", value: 1.09 },
      miu: { name: "塑性粘度 (Pa·s)", value: 0.021 },
      taof: { name: "屈服值 (Pa)", value: 14 },
    },
  },
  {
    rock_cuttings: {
      // (0=不考虑, 1=考虑)
      y: { name: "是否考虑岩屑 ", value: 0 },
      yxmd: { name: "岩屑密度 (kg/m³)", value: 2500 },
      H: { name: "岩屑床高度 (%)", value: 10 },
    },
  },
  {
    flag: "0",
  }
];

const limit_hydro = [
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
      jsjg: { name: "井深计算间隔 (m)", value: 500 },
    },
  },
  {
    fluid: {
      lbmx: {
        name: "流变模式",
        value: 1,
        option: [
          { label: "宾汉流体", value: 1 },
          { label: "幂律流体", value: 2 },
          { label: "赫巴流体", value: 3 },
        ],
      },
      fluidden: { name: "钻井液密度 (kg/m³)", value: 1170 },
      n: { name: "幂律指数", value: 0.48 },
      K: { name: "稠度系数 (Pa·s^n)", value: 1.09 },
      miu: { name: "塑性粘度 (Pa·s)", value: 0.021 },
      taof: { name: "屈服值 (Pa)", value: 14 },
    },
  },
  {
    drill_pressure: {
      A1: { name: "喷嘴1尺寸 (mm)", value: 16 },
      C1: { name: "喷嘴1个数", value: 7 },
      A2: { name: "喷嘴2尺寸 (mm)", value: 0 },
      C2: { name: "喷嘴2个数", value: 0 },
      A3: { name: "喷嘴3尺寸 (mm)", value: 0 },
      C3: { name: "喷嘴3个数", value: 0 },
    },
  },
  {
    drill_joint: {
      Lp: { name: "单根钻杆长度 (m)", value: 10 },
      Li: { name: "接头长度 (m)", value: 0.3 },
      rzzjt: { name: "接头内径 (m)", value: 0.0953 },
    },
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
    },
  },
  {
    rock_cuttings: {
      y: { name: "是否考虑岩屑 ", value: 0 },
      yxmd: { name: "岩屑密度 (kg/m³)", value: 2500 },
      H: { name: "岩屑床高度 (%)", value: 10 },
    },
  },
  {
    flag: "0",
  }
];

// v=0.00714;               %钻进速度，m/s（仅用于工况1,5：工况5名为上提速度）
// omega=5*pi/3;            %转速，rad/s（仅用于工况1,5）
const limit_mechanism = {
  work_condition: {
    wc: {
      name: "工况选择",
      value: 1,
      option: [
        { label: "旋转钻进", value: 1 },
        { label: "滑动钻进", value: 2 },
        { label: "起钻", value: 3 },
        { label: "下钻", value: 4 },
        { label: "倒划眼", value: 5 },
      ],
    },
    v: { name: "钻进速度 (m/s)", value: 0.00714 },
    omega: { name: "转速 (rad/s)", value: (5 * Math.PI) / 3 },
    T0: { name: "钻压 (N)", value: 58900 },
    rhoi: { name: "钻井液密度 (kg/m³)", value: 1170 },
    Dw: { name: "井眼直径 (m)", value: 0.2159 },
    tgxs: { name: "套管下深 (m)", value: 3500 },
    miua11: { name: "套管段摩阻系数", value: 0.15 },
    miua22: { name: "裸眼段摩阻系数", value: 0.2 },
    qfqd: { name: "钻柱屈服强度 (MPa)", value: 931 },
    jsjg: { name: "井深计算间隔 (m)", value: 500 },
  },
};

const limit_curve = {
  Holedia: { name: "井眼直径 (m)", value: 0.2159 },
  ml: { name: "钻柱弹性模量 (MPa)", value: 2.1e5 },
  js: { name: "计算井深 (m)", value: 6000 },
};

const drill_vibration = [
  {
    drill_parameters: {
      Lb: { name: "钻头长度 (m)", value: 0.24 },
      Db: { name: "钻头直径 (m)", value: 0.2159 },
      Lp: { name: "钻杆长度 (m)", value: 5765.26 },
      p1: { name: "钻杆密度 (kg/m³)", value: 8629 },
      Dp: { name: "钻杆外径 (m)", value: 0.127 },
      dp: { name: "钻杆内径 (m)", value: 0.1086 },
      Lpw: { name: "加重钻杆长度 (m)", value: 47.26 },
      p3: { name: "加重钻杆密度 (kg/m³)", value: 9058 },
      Dpw: { name: "加重钻杆外径 (m)", value: 0.127 },
      dc: { name: "加重钻杆内径 (m)", value: 0.0572 },
      Lc: { name: "钻铤长度 (m)", value: 6.89 },
      p2: { name: "钻铤密度 (kg/m³)", value: 8518 },
      Dc: { name: "钻铤外径 (m)", value: 0.1715 },
      dpw: { name: "钻铤内径 (m)", value: 0.0762 },
    },
  },
  {
    fluid_parameters: {
      uf: { name: "钻井液塑性粘度 (mPa.s)", value: 67 },
      sita3: { name: "旋转粘度计读数（3转）", value: 7 },
      sita100: { name: "旋转粘度计读数（100转）", value: 41 },
      sita200: { name: "旋转粘度计读数（200转）", value: 69 },
    },
  },
  {
    calculation_parameters: {
      wob: { name: "钻压 (kN)", value: 100 },
      V: { name: "转速 (RPM)", value: 90 },
      miusb: { name: "静摩擦系数", value: 0.8 },
      miucb: { name: "动摩擦系数", value: 0.5 },
      Lv: { name: "垂直段长度 (m)", value: 3306 },
      dl: { name: "质量块长度 (m)", value: 500 },
      TIME: { name: "计算时长 (s)", value: 50 },
      Dt: { name: "时间步长 (s)", value: 0.01 },
    },
  },
  {
    "flag": '1'
  }
];

export {
  hydro,
  torque,
  limit_curve,
  limit_eye,
  limit_mechanism,
  limit_hydro,
  drill_vibration,
};
