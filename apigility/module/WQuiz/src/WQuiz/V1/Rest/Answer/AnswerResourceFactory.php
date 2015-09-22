<?php
namespace WQuiz\V1\Rest\Answer;

class AnswerResourceFactory
{
    public function __invoke($services)
    {
        return new AnswerResource();
    }
}
