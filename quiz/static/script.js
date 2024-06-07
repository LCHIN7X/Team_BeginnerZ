const startQuizBtnEl = document.getElementById("start-quiz-btn-el");
const quizContainerEl = document.getElementById('quiz-container-el')

startQuizBtnEl.addEventListener("click", () => {
  fetch("/quiz/get-questions")
    .then((res) => res.json())
    .then((data) => {
      const questions = data.questions;
      questions.forEach((question, index) => {
        renderQuizQuestion(question, index);
      });
    })
    .catch(error => console.error('Error fetching questions:', error));
});


function renderQuizQuestion(question, index) {
    quizContainerEl.innerHTML += `
    <div class="quiz-content">
        <h2>Question ${index + 1}</h2>
        <p>${question.question}</p>
        <p>${question.option_a}</p>
        <p>${question.option_b}</p>
        <p>${question.option_c}</p>
        
        <p>Answer: ${question.answer}</p>
    </div>
`;
}