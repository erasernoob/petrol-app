// import { open } from '@tauri-apps/plugin-shell';
import { open as openNer } from '@tauri-apps/plugin-dialog';
import { Message } from '@arco-design/web-react'
import * as XLSX from "xlsx";
import { writeFile, BaseDirectory } from '@tauri-apps/plugin-fs';
import * as path from '@tauri-apps/api/path';
import { save } from '@tauri-apps/plugin-dialog';

const saveData = async (data=[], name) => {
  data = data.map((value, index) => ({value}))
  const worksheet = XLSX.utils.json_to_sheet(data, {skipHeader: true});
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

// data as the first column
const saveAtFrontend = async (data=[], name, data2=[]) => {
  if (data2.length == 0) {
    data = data.map((value, index) => ({value}))
  } else {
    data = data.map((value, index) => ({
      c1: value,
      c2: data2[index],
    }))
  }
  
  const worksheet = XLSX.utils.json_to_sheet(data, {skipHeader: true});
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "sheet1");
  const res = XLSX.write(workbook, { bookType: "xlsx", type: "array" });

  const filePath = await save({
      title: "导出数据到本地",
      defaultPath: name + ".xlsx",
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
const save2Data = async (data=[], name) => {
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
       filters: [{extensions: ['xlsx'], name: ''}],
    })
    if (filePath) {
      const filename = await basename(filePath)
      setFile(() => ({name: filename, path: filePath}))
      Message.success(`${filename}上传成功！`)
      setOrbit((prev) => !prev)
    } else {
      Message.info('文件上传失败,请重新上传')
    }
  }


export { saveData, save2Data, saveAtFrontend, handleUpload }