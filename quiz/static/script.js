const startQuizBtnEl = document.getElementById("start-quiz-btn-el");
const quizContainerEl = document.getElementById('quiz-container-el')
const quizAnswerContainerEl = document.getElementById('quiz-answer-container-el')

let currentQuestionIndex = 0
let questions = []
let score = 0
let moneyEarned = 0


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
  renderQuizQuestion()
}


function renderQuizQuestion() {
  if (currentQuestionIndex < questions.length) {
    const question = questions[currentQuestionIndex];
    const questionText = question.question;
    const optionA = question.option_a.replace(/'/g, "\\'");
    const optionB = question.option_b.replace(/'/g, "\\'");
    const optionC = question.option_c.replace(/'/g, "\\'");
    const correctAnswer = question.answer.replace(/'/g, "\\'");

    quizContainerEl.innerHTML = `
      <div class="quiz-content">
        <h2>Question ${currentQuestionIndex + 1}</h2>
        <p>${questionText}</p>
        <button class='btn-primary btn' onclick="checkUserAnswer('${optionA}', '${correctAnswer}')">${optionA}</button>
        <button class='btn-primary btn' onclick="checkUserAnswer('${optionB}', '${correctAnswer}')">${optionB}</button>
        <button class='btn-primary btn' onclick="checkUserAnswer('${optionC}', '${correctAnswer}')">${optionC}</button>
      </div>
    `;
  } else {
    quizContainerEl.innerHTML = `<h1>Quiz Complete!</h1>
    <h2>Your score: ${score}/${questions.length}</h2>
    <h3>You earned $${moneyEarned}!</h3>`;
  }
}


function checkUserAnswer(userSelection, correctAnswer) {
  let isCorrect
  if (userSelection == correctAnswer) {
    score ++
    console.log('Hooray! That is correct!')
    console.log(score)
    moneyEarned += 5
    isCorrect = true
  }
  else {
    console.log(userSelection)
    console.log(correctAnswer)
    console.log("Oops! Wrong Answer!")
    isCorrect = false
  }
  renderQuestionResult(userSelection, correctAnswer, isCorrect)
  currentQuestionIndex ++
  renderQuizQuestion()
}


function renderQuestionResult(userSelection, correctAnswer, isCorrect) {
  if (isCorrect) {
    quizAnswerContainerEl.innerHTML = 
    `<h3>Hooray! Correct!</h3>
    <h5>Your answer: ${userSelection}</h5>
    <h5>Correct answer: ${correctAnswer}</h5>
    <p>You Earned $${moneyEarned}! Keep it up!</p>
    `
  }
  else {
    quizAnswerContainerEl.innerHTML = 
    `<h3>Oh darn! Wrong Answer.</h3>
    <h5>Your answer: ${userSelection}</h5>
    <h5>Correct answer: ${correctAnswer}</h5>
    <p>Better luck next time!</p>
    `
  }
}