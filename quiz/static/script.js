const startQuizBtnEl = document.getElementById("start-quiz-btn-el");
const quizContainerEl = document.getElementById('quiz-container-el');
const quizAnswerContainerEl = document.getElementById('quiz-answer-container-el');
const nextQuestionBtnEl = document.getElementById('next-question-btn-el');
const reviewContainerEl = document.getElementById('review-container-el');
const reviewContentEl = document.getElementById('review-content-el');
const backToQuizBtnEl = document.getElementById('back-to-quiz-btn-el');

let currentQuestionIndex = 0;
let questions = [];
let score = 0;
let moneyEarned = 0;
let userAnswers = [];

startQuizBtnEl.addEventListener("click", (e) => {
  e.preventDefault();
  fetch("/quiz/get-questions")
    .then((res) => res.json())
    .then((data) => {
      quizContainerEl.innerHTML = '';
      questions = data.questions;
      currentQuestionIndex = 0;
      userAnswers = [];
      startQuiz();
    })
    .catch(error => console.error('Error fetching questions:', error));
});

nextQuestionBtnEl.addEventListener("click", (e) => {
  e.preventDefault();
  currentQuestionIndex++;
  renderQuizQuestion();
  quizAnswerContainerEl.innerHTML = ''; // Clear previous answer result
  nextQuestionBtnEl.classList.add('hidden');
});


backToQuizBtnEl.addEventListener("click", (e) => {
  e.preventDefault();
  reviewContainerEl.classList.add('hidden');
  quizContainerEl.classList.remove('hidden');
  location.reload()
});

function startQuiz() {
  renderQuizQuestion();
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
    showReviewSection();
  }
}


function checkUserAnswer(userSelection, correctAnswer) {
  let isCorrect;

  if (userSelection == correctAnswer) {
    score++;
    moneyEarned += 5;
    isCorrect = true;
  } else {
    isCorrect = false;
  }
  userAnswers.push({ question: questions[currentQuestionIndex], userSelection, correctAnswer, isCorrect });
  renderQuestionResult(userSelection, correctAnswer, isCorrect);
}


function renderQuestionResult(userSelection, correctAnswer, isCorrect) {
  nextQuestionBtnEl.classList.remove('hidden');

  if (isCorrect) {
    incrementUserCash()
    quizAnswerContainerEl.innerHTML = 
    `<h3>Hooray! Correct!</h3>
    <h5>Your answer: ${userSelection}</h5>
    <h5>Correct answer: ${correctAnswer}</h5>
    <p>You Earned $${moneyEarned}! Keep it up!</p>`;

  } 
  else {
    quizAnswerContainerEl.innerHTML = 
    `<h3>Oh darn! Wrong Answer.</h3>
    <h5>Your answer: ${userSelection}</h5>
    <h5>Correct answer: ${correctAnswer}</h5>
    <p>Better luck next time!</p>`;
  }
}

function showReviewSection() {
  quizContainerEl.classList.add('hidden');
  reviewContainerEl.classList.remove('hidden');
  reviewContentEl.innerHTML = '';

  userAnswers.forEach((answer, index) => {
    reviewContentEl.innerHTML += `
      <div class="review-item">
        <h4>Question ${index + 1}</h4>
        <p>${answer.question.question}</p>
        <p>Your answer: ${answer.userSelection}</p>
        <p>Correct answer: ${answer.correctAnswer}</p>
        <p>${answer.isCorrect ? 'Correct' : 'Wrong'}</p>
      </div>
    `;
  });
}

function incrementUserCash() {
  fetch('/quiz/increment-cash')
       .then(res => res.json())
       .then(data => console.log(data))
       .catch(err => console.log(err))
}