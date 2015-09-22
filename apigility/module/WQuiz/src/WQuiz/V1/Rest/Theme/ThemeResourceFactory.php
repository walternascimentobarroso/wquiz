<?php
namespace WQuiz\V1\Rest\Theme;

class ThemeResourceFactory
{
    public function __invoke($services)
    {
        return new ThemeResource();
    }
}
