import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
// next.config.js

module.exports = {
  images: {
    domains: ['s1.locimg.com', 'localhost', '127.0.0.1'], // 添加允许的图像域名
  },
}