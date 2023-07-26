const form = document.getElementById("questionnaire");
const inputs = form.querySelectorAll("input");
const submitBtn = document.getElementById("submitBtn");
const buttonMessage = document.getElementById("buttonMessage");

// 상태 변화 추적용 (isDirty)
let buttonClicked = false;

// Set the loading state of the button
const setLoadingState = (isLoading) => {
  submitBtn.disabled = isLoading;
  buttonMessage.textContent = isLoading ? "잠시만 기다려주세요..." : "";
};

// validation
const checkInputs = () => {
  // if button clicked, 아무것도 체크하지 않음.
  if (buttonClicked) return;

  let isValid = true;
  inputs.forEach((input) => {
    if (input.value.trim() === "") isValid = false;
  });
  submitBtn.disabled = !isValid;
  buttonMessage.textContent = isValid
    ? ""
    : "모든 칸의 내용을 채워 주셔야 합니다!";
};

inputs.forEach((input) => {
  input.addEventListener("input", checkInputs);
});

form.addEventListener("submit", (e) => {
  e.preventDefault();

  // If the button is in the loading state, prevent further submission
  if (submitBtn.disabled) return;


  // if isDirty is true, then checkInputs
  buttonClicked = true;
  setLoadingState(true);
  
  setTimeout(() => {
    checkInputs();

    if (!submitBtn.disabled) {
      buttonMessage.textContent = "잠시만 기다려주세요...";
      inputs.forEach((input) => (input.value = ""));
    }
  // if form submit is done, then reset the status.
  buttonClicked = false;
  }, 0);
});
