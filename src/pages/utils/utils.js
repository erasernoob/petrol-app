import { open } from '@tauri-apps/plugin-shell';
import { Message } from '@arco-design/web-react'
import * as XLSX from "xlsx";
import { writeFile, BaseDirectory } from '@tauri-apps/plugin-fs';
import * as path from '@tauri-apps/api/path';

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

export { saveData }