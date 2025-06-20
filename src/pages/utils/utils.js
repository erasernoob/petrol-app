// import { open } from '@tauri-apps/plugin-shell';
import { Message } from '@arco-design/web-react';
import * as path from '@tauri-apps/api/path';
import { open as openNer, save } from '@tauri-apps/plugin-dialog';
import { BaseDirectory, writeFile } from '@tauri-apps/plugin-fs';
import Big from 'big.js';
import * as XLSX from "xlsx";

const handleTheError = (error) => {
  if (!error.response) {
    Message.error("系统内部计算出现问题，请检查输入参数！")
  }
  const code = error.status
  if (code === 422) {
    Message.error("输入参数出现问题,请检查输入参数！")
  } else if (code === 500) {
    Message.error("系统内部计算出现问题，请检查！")
  }
}

const saveData = async (data = [], name) => {
  data = data.map((value, index) => ({ value }))
  const worksheet = XLSX.utils.json_to_sheet(data, { skipHeader: true });
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "sheet1");
  const res = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
  if (res) {
    await writeFile(name, res, {
      baseDir: BaseDirectory.Download,
    });
    Message.success(`${name}数据导出成功！`)
    // 获取用户的下载文件夹路径
    const downloadPath = await path.downloadDir()
    // 打开下载文件夹
    await open(await path.join(downloadPath, ''));
  }
}

const saveCurveFile = async (file, name) => {
  const filePath = await save({
    title: "导出数据到本地",
    defaultPath: `${name}.xlsx`,
    filters: [{ name: "xlsx Files", extensions: ["xlsx"] }]
  });

  if (!filePath) return

  // 1. 将 CSV 字符串解析为 workbook
  const workbook = XLSX.read(file, { type: "string" })

  // 2. 将 workbook 写成 xlsx 二进制数据（Uint8Array）
  const res = XLSX.write(workbook, { bookType: "xlsx", type: "array" })
  if (filePath) {
    await writeFile(filePath, res, {
      baseDir: filePath
    })
    Message.success(`${name}数据导出成功！`)
  }

}

// data as the first column
const saveAtFrontend = async (data = [], name, data2 = []) => {
  if (data2.length == 0) {
    data = data.map((value, index) => ({ value }))
  } else {
    data = data.map((value, index) => ({
      c1: value,
      c2: data2[index],
    }))
  }

  const worksheet = XLSX.utils.json_to_sheet(data, { skipHeader: true });
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "sheet1");
  const res = XLSX.write(workbook, { bookType: "xlsx", type: "array" });

  const filePath = await save({
    title: "导出数据到本地",
    defaultPath: `${name}.xlsx`,
    filters: [{ name: "xlsx Files", extensions: ["xlsx"] }]
  });
  if (filePath) {
    await writeFile(filePath, res, {
      baseDir: filePath
    })
    Message.success(`${name}数据导出成功！`)
  }
}

// 直接打开下载文件夹
const save2Data = async (data = [], name) => {
  if (true) {
    setTimeout(async () => {
      Message.success(`数据导出成功！`)
      const downloadPath = await path.downloadDir()
      // 打开下载文件夹
      await open(await path.join(downloadPath, ''));
    }, 200)
  }
}

// Handle UPLOAD FOR HYDRA
const handleUpload = async (id) => {
  const filePath = await openNer({
    name: "导入文件",
    multiple: false,
    filters: [{ extensions: ['xlsx'], name: '' }],
  })
  if (filePath) {
    const filename = await basename(filePath)
    setFile(() => ({ name: filename, path: filePath }))
    Message.success(`${filename}上传成功！`)
    setOrbit((prev) => !prev)
  } else {
    Message.info('文件上传失败,请重新上传')
  }
}

// 单位换算
const dealWithTheDataUnit = (data, idx) => {
  // for Hydra
  if (idx == 1) {
    data.Dw = new Big(data.Dw).div(1000).toNumber()
    data.Rzz = new Big(data.Rzz).div(1000).toNumber()
    data.rzz = new Big(data.rzz).div(1000).toNumber()
    data.Rzt = new Big(data.Rzt).div(1000).toNumber()
    data.rzt = new Big(data.rzt).div(1000).toNumber()
    data.miu = new Big(data.miu).div(1000).toNumber()
  } else if (idx == 2) {
    data.v = new Big(data.v).div(3600).toNumber()
    data.omega = new Big(data.omega).div(30).mul(Math.PI).toNumber()
    data.T0 = new Big(data.T0 ? data.T0 : 0).mul(1000).toNumber()
    data.Dw = new Big(data.Dw).div(1000).toNumber()
  } else if (idx == 3) {
    // curve 
    data.Holedia = new Big(data.Holedia).div(1000).toNumber()
  } else if (idx == 4) {
    // vibration
    data.Db = new Big(data.Db).div(1000).toNumber()
    data.Dp = new Big(data.Dp).div(1000).toNumber()
    data.dp = new Big(data.dp).div(1000).toNumber()
    data.Dpw = new Big(data.Dpw).div(1000).toNumber()
    data.dc = new Big(data.dc).div(1000).toNumber()
    data.Dc = new Big(data.Dc).div(1000).toNumber()
    data.dpw = new Big(data.dpw).div(1000).toNumber()

  }
}


const useTheInitialValue = true


export { dealWithTheDataUnit, handleTheError, handleUpload, save2Data, saveAtFrontend, saveCurveFile, saveData, useTheInitialValue };

