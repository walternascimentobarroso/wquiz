<?php
namespace WQuiz\V1\Rest\Question;

class QuestionResourceFactory
{
    public function __invoke($services)
    {
        return new QuestionResource();
    }
}
