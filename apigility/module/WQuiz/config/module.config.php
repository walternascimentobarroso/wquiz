<?php
return array(
    'service_manager' => array(
        'factories' => array(
            'WQuiz\\V1\\Rest\\Theme\\ThemeResource' => 'WQuiz\\V1\\Rest\\Theme\\ThemeResourceFactory',
            'WQuiz\\V1\\Rest\\Question\\QuestionResource' => 'WQuiz\\V1\\Rest\\Question\\QuestionResourceFactory',
            'WQuiz\\V1\\Rest\\Answer\\AnswerResource' => 'WQuiz\\V1\\Rest\\Answer\\AnswerResourceFactory',
        ),
    ),
    'router' => array(
        'routes' => array(
            'w-quiz.rest.theme' => array(
                'type' => 'Segment',
                'options' => array(
                    'route' => '/theme[/:theme_id]',
                    'defaults' => array(
                        'controller' => 'WQuiz\\V1\\Rest\\Theme\\Controller',
                    ),
                ),
            ),
            'w-quiz.rest.question' => array(
                'type' => 'Segment',
                'options' => array(
                    'route' => '/question[/:question_id]',
                    'defaults' => array(
                        'controller' => 'WQuiz\\V1\\Rest\\Question\\Controller',
                    ),
                ),
            ),
            'w-quiz.rest.answer' => array(
                'type' => 'Segment',
                'options' => array(
                    'route' => '/answer[/:answer_id]',
                    'defaults' => array(
                        'controller' => 'WQuiz\\V1\\Rest\\Answer\\Controller',
                    ),
                ),
            ),
        ),
    ),
    'zf-versioning' => array(
        'uri' => array(
            0 => 'w-quiz.rest.theme',
            1 => 'w-quiz.rest.question',
            2 => 'w-quiz.rest.answer',
        ),
    ),
    'zf-rest' => array(
        'WQuiz\\V1\\Rest\\Theme\\Controller' => array(
            'listener' => 'WQuiz\\V1\\Rest\\Theme\\ThemeResource',
            'route_name' => 'w-quiz.rest.theme',
            'route_identifier_name' => 'theme_id',
            'collection_name' => 'theme',
            'entity_http_methods' => array(
                0 => 'GET',
                1 => 'PATCH',
                2 => 'PUT',
                3 => 'DELETE',
            ),
            'collection_http_methods' => array(
                0 => 'GET',
                1 => 'POST',
            ),
            'collection_query_whitelist' => array(),
            'page_size' => 25,
            'page_size_param' => null,
            'entity_class' => 'WQuiz\\V1\\Rest\\Theme\\ThemeEntity',
            'collection_class' => 'WQuiz\\V1\\Rest\\Theme\\ThemeCollection',
            'service_name' => 'theme',
        ),
        'WQuiz\\V1\\Rest\\Question\\Controller' => array(
            'listener' => 'WQuiz\\V1\\Rest\\Question\\QuestionResource',
            'route_name' => 'w-quiz.rest.question',
            'route_identifier_name' => 'question_id',
            'collection_name' => 'question',
            'entity_http_methods' => array(
                0 => 'GET',
                1 => 'PATCH',
                2 => 'PUT',
                3 => 'DELETE',
            ),
            'collection_http_methods' => array(
                0 => 'GET',
                1 => 'POST',
            ),
            'collection_query_whitelist' => array(),
            'page_size' => 25,
            'page_size_param' => null,
            'entity_class' => 'WQuiz\\V1\\Rest\\Question\\QuestionEntity',
            'collection_class' => 'WQuiz\\V1\\Rest\\Question\\QuestionCollection',
            'service_name' => 'question',
        ),
        'WQuiz\\V1\\Rest\\Answer\\Controller' => array(
            'listener' => 'WQuiz\\V1\\Rest\\Answer\\AnswerResource',
            'route_name' => 'w-quiz.rest.answer',
            'route_identifier_name' => 'answer_id',
            'collection_name' => 'answer',
            'entity_http_methods' => array(
                0 => 'GET',
                1 => 'PATCH',
                2 => 'PUT',
                3 => 'DELETE',
            ),
            'collection_http_methods' => array(
                0 => 'GET',
                1 => 'POST',
            ),
            'collection_query_whitelist' => array(),
            'page_size' => 25,
            'page_size_param' => null,
            'entity_class' => 'WQuiz\\V1\\Rest\\Answer\\AnswerEntity',
            'collection_class' => 'WQuiz\\V1\\Rest\\Answer\\AnswerCollection',
            'service_name' => 'answer',
        ),
    ),
    'zf-content-negotiation' => array(
        'controllers' => array(
            'WQuiz\\V1\\Rest\\Theme\\Controller' => 'HalJson',
            'WQuiz\\V1\\Rest\\Question\\Controller' => 'HalJson',
            'WQuiz\\V1\\Rest\\Answer\\Controller' => 'HalJson',
        ),
        'accept_whitelist' => array(
            'WQuiz\\V1\\Rest\\Theme\\Controller' => array(
                0 => 'application/vnd.w-quiz.v1+json',
                1 => 'application/hal+json',
                2 => 'application/json',
            ),
            'WQuiz\\V1\\Rest\\Question\\Controller' => array(
                0 => 'application/vnd.w-quiz.v1+json',
                1 => 'application/hal+json',
                2 => 'application/json',
            ),
            'WQuiz\\V1\\Rest\\Answer\\Controller' => array(
                0 => 'application/vnd.w-quiz.v1+json',
                1 => 'application/hal+json',
                2 => 'application/json',
            ),
        ),
        'content_type_whitelist' => array(
            'WQuiz\\V1\\Rest\\Theme\\Controller' => array(
                0 => 'application/vnd.w-quiz.v1+json',
                1 => 'application/json',
            ),
            'WQuiz\\V1\\Rest\\Question\\Controller' => array(
                0 => 'application/vnd.w-quiz.v1+json',
                1 => 'application/json',
            ),
            'WQuiz\\V1\\Rest\\Answer\\Controller' => array(
                0 => 'application/vnd.w-quiz.v1+json',
                1 => 'application/json',
            ),
        ),
    ),
    'zf-hal' => array(
        'metadata_map' => array(
            'WQuiz\\V1\\Rest\\Theme\\ThemeEntity' => array(
                'entity_identifier_name' => 'id',
                'route_name' => 'w-quiz.rest.theme',
                'route_identifier_name' => 'theme_id',
                'hydrator' => 'Zend\\Stdlib\\Hydrator\\ArraySerializable',
            ),
            'WQuiz\\V1\\Rest\\Theme\\ThemeCollection' => array(
                'entity_identifier_name' => 'id',
                'route_name' => 'w-quiz.rest.theme',
                'route_identifier_name' => 'theme_id',
                'is_collection' => true,
            ),
            'WQuiz\\V1\\Rest\\Question\\QuestionEntity' => array(
                'entity_identifier_name' => 'id',
                'route_name' => 'w-quiz.rest.question',
                'route_identifier_name' => 'question_id',
                'hydrator' => 'Zend\\Stdlib\\Hydrator\\ArraySerializable',
            ),
            'WQuiz\\V1\\Rest\\Question\\QuestionCollection' => array(
                'entity_identifier_name' => 'id',
                'route_name' => 'w-quiz.rest.question',
                'route_identifier_name' => 'question_id',
                'is_collection' => true,
            ),
            'WQuiz\\V1\\Rest\\Answer\\AnswerEntity' => array(
                'entity_identifier_name' => 'id',
                'route_name' => 'w-quiz.rest.answer',
                'route_identifier_name' => 'answer_id',
                'hydrator' => 'Zend\\Stdlib\\Hydrator\\ArraySerializable',
            ),
            'WQuiz\\V1\\Rest\\Answer\\AnswerCollection' => array(
                'entity_identifier_name' => 'id',
                'route_name' => 'w-quiz.rest.answer',
                'route_identifier_name' => 'answer_id',
                'is_collection' => true,
            ),
        ),
    ),
);
