const axios = window.axios;

// !!!주의: 향후 실제 서비스 시, 백엔드 프록시 서버 또는 aws 로 처리 필수.
const url = `http://localhost:8000/chatbot/api/chat/`;
// const url = `https://estsoft-openai-api.jejucodingcamp.workers.dev/`;

export const apiPost = async (data) => {
  const startTime = Date.now();

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  const endTime = Date.now();
  console.log(`API 요청 처리 시간: ${endTime - startTime} ms`);

  return result;
};



// export const apiPost = async (data) => {
//   const response = await fetch("http://localhost:8000/chatbot/api/chat/", { // URL 수정
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(data),
//   });
//   console.log(response); // 응답 출력
//   return response.json();
// };
