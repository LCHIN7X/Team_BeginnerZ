const startQuizBtnEl = document.getElementById("start-quiz-btn-el");
const quizContainerEl = document.getElementById('quiz-container-el')

let currentQuestionIndex = 0
let questions = []
let score = 0

startQuizBtnEl.addEventListener("click", (e) => {
  e.preventDefault()
  fetch("/quiz/get-questions")
    .then((res) => res.json())
    .then((data) => {
      quizContainerEl.innerHTML = ''
      questions = data.questions;
      currentQuestionIndex = 0
      startQuiz()
    })
    .catch(error => console.error('Error fetching questions:', error));
});


function startQuiz() {
  // if (currentQuestionIndex < questions.length) {
  //   const question = questions[currentQuestionIndex]
  //   renderQuizQuestion(question)
  // }
  renderQuizQuestion()
}


function renderQuizQuestion() {
  if (currentQuestionIndex < questions.length) {
    const question = questions[currentQuestionIndex]
    quizContainerEl.innerHTML += `
    <div class="quiz-content">
        <h2>Question ${currentQuestionIndex + 1}</h2>
        <p>${question.question}</p>
        <button class='btn-primary btn' onclick="checkUserAnswer('${question.option_a}', '${question.answer}')">${question.option_a}</button>
        <button class='btn-primary btn' onclick="checkUserAnswer('${question.option_b}', '${question.answer}')">${question.option_b}</button>
        <button class='btn-primary btn' onclick="checkUserAnswer('${question.option_c}', '${question.answer}')">${question.option_c}</button>
    </div>
`;
  }
  else {
    quizContainerEl.innerHTML = `<h1>Quiz Complete!</h1>
    <h2>Your score: ${score}/${questions.length}</h2>`
  }
}


function checkUserAnswer(userSelection, correctAnswer) {
  if (userSelection == correctAnswer) {
    score ++
    
    console.log('Hooray! That is correct!')
    console.log(score)
  }
  else {
    console.log(userSelection)
    console.log(correctAnswer)
    console.log("Oops! Wrong Answer!")
  }
  currentQuestionIndex ++
  renderQuizQuestion()
}