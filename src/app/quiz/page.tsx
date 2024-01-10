"use client";
import React, { useState } from "react";
import { quiz } from "../data";
import { Button } from "@/components/ui/button";
import { ResultQuiz } from "@/components/ResultQuiz";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const Page = () => {
  const [activeQuestion, setActiveQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(false);
  const [checked, setChecked] = useState(false);
  const [selectedAnswerIndex, setSelectedAnswerIndex] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [result, setResult] = useState({
    score: 0,
    correctAnswers: 0,
    wrongAnswers: 0,
  });

  const { questions } = quiz;
  const { question, answers, correctAnswer } = questions[activeQuestion];

  //   Select and check answer
  const onAnswerSelected = (answer: any, idx: any) => {
    setChecked(true);
    setSelectedAnswerIndex(idx);
    setSelectedAnswer(answer === correctAnswer);
  };

  // Calculate score and increment to next question
  const nextQuestion = () => {
    setResult((prev) => ({
      ...prev,
      score: selectedAnswer ? prev.score + 5 : prev.score,
      correctAnswers: selectedAnswer
        ? prev.correctAnswers + 1
        : prev.correctAnswers,
      wrongAnswers: selectedAnswer ? prev.wrongAnswers : prev.wrongAnswers + 1,
    }));

    setActiveQuestion((prev) =>
      activeQuestion !== questions.length - 1 ? prev + 1 : 0
    );
    setShowResult(activeQuestion === questions.length - 1);
    setChecked(false);
    setSelectedAnswerIndex(null);
  };

  if (showResult) return <ResultQuiz result={result} total={question.length} />;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Quiz Page</CardTitle>
        <h2>
          Question: {activeQuestion + 1}
          <span>/{questions.length}</span>
        </h2>
      </CardHeader>
      <CardContent className="grid gap-6">
        <h3>{questions[activeQuestion].question}</h3>
        {answers.map((answer, idx) => (
          <Label
            key={idx}
            onClick={() => onAnswerSelected(answer, idx)}
            className={selectedAnswerIndex === idx ? "border-primary" : ""}
          >
            {answer}
          </Label>
        ))}
      </CardContent>
      <CardFooter>
        <Button onClick={nextQuestion} className="w-full" disabled={!checked}>
          {activeQuestion === question.length - 1 ? "Finish" : "Next"}
        </Button>
      </CardFooter>
    </Card>
  );
};

export default Page;
