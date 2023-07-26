// 화면에 질문 그려주는 함수
export const printQuestion = async ($chatList, questionData, question) => {
  $chatList.innerHTML = "";

  if (question) {
    let li = document.createElement("li");
    li.classList.add("question");

    let span = document.createElement("span");
    span.innerText = "다음의 문장을 기반으로 알아보고 있어요: ";
    li.appendChild(span);

    questionData.map((el) => {
      let questionText = document.createElement("span");
      questionText.innerText = el.content;
      li.appendChild(questionText);
    });

    // 답변 표시
    $chatList.appendChild(li);
    questionData = [];
    question = false;
  }
};

// 화면에 답변 그려주는 함수
export const printAnswer = async ($chatList, answer, $form) => {
  $chatList.innerHTML = "";
  // 답변 표시
  let li = document.createElement("li");
  // transition effect to highlight the answer.
  li.classList.add("answer", "fade");
  li.innerText = answer;
  $chatList.appendChild(li);

  setTimeout(() => {
    li.classList.add("fadeIn");
  }, 500);

  // 클립보트로 복사 버튼
  let copyButton = document.createElement("button");
  copyButton.classList.add("copyButton");
  copyButton.innerText = "이 답변 내용을 복사합니다.";
  copyButton.type = "button";

  copyButton.addEventListener("click", (e) => {
    e.stopPropagation();
    // 클립보드에 해당 답변을 복사
    navigator.clipboard
      .writeText(answer)
      .then(() => {
        copyButton.innerText = "클립보드에 복사되었습니다!";
        console.log(
          "printAnswer -> copyButton, navigator : 클립보드 복사 성공"
        );
      })
      .catch((err) => {
        console.log("뭔가 잘못되었습니다. printAnswer -> copyButton", err);
      });
  });
  $chatList.appendChild(copyButton);

  // URL 링크 추가
  let link = document.createElement("a");
  link.href = "https://www.aladin.co.kr";
  link.textContent = "알라딘 온라인 서점";
  link.target = "_blank";
  link.id = "copyButton2";
  $chatList.appendChild(link);

  // 새로고침 버튼
  let resetButton = document.createElement("button");
  resetButton.setAttribute("type", "button");
  resetButton.classList.add("resetButton");
  resetButton.innerText = "Reset";
  resetButton.addEventListener("click", () => {
    $form.reset();
    location.reload();
  });
  $chatList.appendChild(resetButton);
};

export const showLoadingSvg = () => {
  document.getElementById("loadingSvg").style.display = "block";
};

export const hideLoadingSvg = () => {
  document.getElementById("loadingSvg").style.display = "none";
};
