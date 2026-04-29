// 这个文件的存在可以帮助Cloudflare识别这是一个有效的部署项目
// 仅在需要Worker功能时才使用此文件
export default {
  async fetch(request, env) {
    // 对于静态Vue应用，通常不需要Worker
    // 此文件仅用于确保Cloudflare正确识别项目类型
    return new Response('Not Found', { status: 404 });
  }
};