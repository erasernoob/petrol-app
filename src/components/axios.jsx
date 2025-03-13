import axios from "axios";

// 创建 Axios 实例
const instance = axios.create({
  baseURL: "http://localhost:8000", // 修改为你的 API 地址
  timeout: 10000000, // 超时时间
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 在请求发送前处理，例如添加 token
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    return response.data; // 直接返回 data，避免每次取 response.data
  },
  (error) => {
    if (error.response) {
      // 服务器返回错误信息
      console.error("请求错误:", error.response.data);
    } else if (error.request) {
      // 请求已发出，但无响应
      console.error("无响应:", error.request);
    } else {
      // 其他错误
      console.error("请求失败:", error.message);
    }
    return Promise.reject(error);
  }
);

// 封装 GET 请求
export const get = (url, params = {}, config = {}) => {
  return instance.get(url, { params, ...config });
};

// 封装 POST 请求
export const post = (url, data = {}, config = {}) => {
  console.log(data)
  return instance.post(url, data, config);
};

// 封装 PUT 请求
export const put = (url, data = {}, config = {}) => {
  return instance.put(url, data, config);
};

// 封装 DELETE 请求
export const del = (url, config = {}) => {
  return instance.delete(url, config);
};

export default instance;
