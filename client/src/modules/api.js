const axios = window.axios;

// !!!주의: 향후 실제 서비스 시, 백엔드 프록시 서버 또는 aws 로 처리 필수.
const url = `http://localhost:8000/chatbot/api/chat/`;
// const url = `https://estsoft-openai-api.jejucodingcamp.workers.dev/`;

export const apiPost = async (data) => {
  const result = await axios({
    method: "post",
    maxBodyLength: Infinity,
    url: url,
    headers: {
      "Content-Type": "application/json",
    },
    data: JSON.stringify(data),
  });
  return result.data;
};
